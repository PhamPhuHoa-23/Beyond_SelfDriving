from datetime import timedelta
import json
import os
import shutil
import socket
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import torch
import torch.distributed as dist
import wandb
from datasets import Dataset
from deepspeed import DeepSpeedEngine
from transformers import AutoTokenizer, PreTrainedModel
from vllm import LLM, SamplingParams
DEFAULT_SYSTEM_MESSAGE = 'You are a helpful assistant. You first think about the reasoning process in the mind and then provide the user with the answer.'
DEFAULT_PROMPT_TEMPLATE = 'Using the numbers {numbers}, create an equation that equals {target}. You can use basic arithmetic operations (+, -, *, /) and each number can only be used once. Show your work in <think> </think> tags. And return the final equation and answer in <answer> </answer> tags, for example <answer>(1 + 2) / (3 * 5)</answer>.'

def create_prompt(numbers: List[int], target: int, tokenizer: AutoTokenizer, system_message: str=DEFAULT_SYSTEM_MESSAGE, prompt_template: str=DEFAULT_PROMPT_TEMPLATE) -> str:
    prefix = [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': prompt_template.format(numbers=numbers, target=target)}, {'role': 'assistant', 'content': 'Let me solve this step by step.\n<think>'}]
    return tokenizer.apply_chat_template(prefix, tokenize=False, continue_final_message=True)

def prepare_model_inputs(query_token_ids: List[List[int]], response_token_ids: List[List[int]], advantages: List[List[float]], device: torch.device) -> Dict[str, torch.Tensor]:
    max_seq_len = max((len(q) + len(r) for q, r in zip(query_token_ids, response_token_ids)))
    inputs = {'input_ids': [], 'attention_mask': [], 'labels': [], 'advantages': [], 'labels_mask': []}
    pad_token_id = 0
    ignore_index = -100
    for query, response, advantage in zip(query_token_ids, response_token_ids, advantages):
        combined_ids = query + response
        seq_len = len(combined_ids)
        input_ids = combined_ids + [pad_token_id] * (max_seq_len - seq_len)
        attention_mask = [1] * seq_len + [0] * (max_seq_len - seq_len)
        labels = [ignore_index] * len(query) + response + [ignore_index] * (max_seq_len - seq_len)
        labels_mask = [0] * len(query) + [1] * len(response) + [0] * (max_seq_len - seq_len)
        advantages_seq = [0.0] * len(query) + advantage + [0.0] * (max_seq_len - seq_len)
        assert len(input_ids) == max_seq_len
        assert len(attention_mask) == max_seq_len
        assert len(labels) == max_seq_len
        assert len(advantages_seq) == max_seq_len
        assert len(labels_mask) == max_seq_len
        inputs['input_ids'].append(input_ids)
        inputs['attention_mask'].append(attention_mask)
        inputs['labels'].append(labels)
        inputs['advantages'].append(advantages_seq)
        inputs['labels_mask'].append(labels_mask)
    return {k: torch.tensor(v, dtype=torch.long if k != 'advantages' else torch.float, device=device) for k, v in inputs.items()}

@torch.compile(dynamic=True)
def log_softmax_and_gather(logits: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
    logprobs = logits.log_softmax(dim=-1)
    return torch.gather(logprobs, dim=-1, index=index.unsqueeze(-1)).squeeze(-1)

def compute_token_log_probs(model: Union[DeepSpeedEngine, PreTrainedModel], inputs: Dict[str, torch.Tensor], temperature: float) -> torch.Tensor:
    outputs = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], return_dict=True, use_cache=False)
    logits = outputs.logits / temperature
    shift_logits = logits[..., :-1, :]
    shift_labels = inputs['labels'][..., 1:]
    shift_labels_mask = inputs['labels_mask'][..., 1:]
    shift_labels[~shift_labels_mask.bool()] = 0
    log_probs = log_softmax_and_gather(shift_logits, shift_labels)
    log_probs = log_probs * shift_labels_mask
    return log_probs

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def evaluate_on_test_set(inference_engine: LLM, test_dataset: Dataset, tokenizer: AutoTokenizer, eos_token: str, eval_sampling_params: SamplingParams, reward_func: Callable[[str, Dict[str, Any]], Tuple[float, Dict[str, float]]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    generations = inference_engine.generate(prompt_token_ids=test_dataset['input_ids'], sampling_params=eval_sampling_params)
    metrics = {'response_lengths': [], 'rewards': [], 'non_stop_rate': []}
    all_query_token_ids = []
    all_responses_token_ids = []
    for i, sample in enumerate(test_dataset):
        query_token_ids = sample['input_ids']
        response_token_ids = generations[i].outputs[0].token_ids
        finish_reason = generations[i].outputs[0].finish_reason
        response = tokenizer.decode(response_token_ids, skip_special_tokens=False)
        reward, reward_components = reward_func(response, sample)
        all_query_token_ids.append(query_token_ids)
        all_responses_token_ids.append(response_token_ids)
        metrics['rewards'].append(reward)
        metrics['non_stop_rate'].append(finish_reason != 'stop')
        metrics['response_lengths'].append(len(response_token_ids))
        for k, v in reward_components.items():
            metrics.setdefault(f'reward_metrics/{k}', []).append(v)
    episodes = {'all_query_token_ids': all_query_token_ids, 'all_response_token_ids': all_responses_token_ids}
    return (episodes, metrics)

def dump_episodes(episodes: Dict[str, Any], episodes_stats: Dict[str, Any], exp_dir: Path, tokenizer: AutoTokenizer, iteration: int, is_eval: bool=False, do_save: bool=True) -> wandb.Table:
    query_token_ids = episodes['all_query_token_ids']
    response_token_ids = episodes['all_response_token_ids']
    rewards = episodes_stats['rewards']
    response_lengths = episodes_stats['response_lengths']
    query_texts = tokenizer.batch_decode(query_token_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
    response_texts = tokenizer.batch_decode(response_token_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
    if dist.is_initialized():
        rank = dist.get_rank()
    else:
        rank = 0
    if not is_eval and rank == 0:
        print(f'########## Example 1 (Reward: {rewards[0]}, Response Length: {response_lengths[0]})')
        print(f'#### Query:\n`{query_texts[0]}`')
        print(f'#### Response:\n`{response_texts[0]}`\n\n')
        print(f'########## Example 2 (Reward: {rewards[1]}, Response Length: {response_lengths[1]})')
        print(f'#### Query:\n`{query_texts[1]}`')
        print(f'#### Response:\n`{response_texts[1]}`\n\n')
    if is_eval:
        episodes_dir = exp_dir / 'eval_episodes'
    else:
        episodes_dir = exp_dir / 'episodes'
    if dist.is_initialized():
        episodes_dir = episodes_dir / f'rank_{rank:02d}'
    episodes_dir.mkdir(parents=True, exist_ok=True)
    table = wandb.Table(columns=['query', 'response', 'reward', 'response_length'])
    for i in range(len(query_texts)):
        table.add_data(query_texts[i], response_texts[i], rewards[i], response_lengths[i])
    if not do_save:
        return table
    with open(episodes_dir / f'eps_{iteration:06d}.json', 'w') as f:
        json.dump([{'query': query_texts[i], 'response': response_texts[i], 'reward': rewards[i]} for i in range(len(query_texts))], f)
    return table

def find_last_checkpoint(exp_dir: Path) -> Tuple[Optional[Path], Optional[int]]:
    checkpoint_dir = exp_dir / 'checkpoints'
    checkpoints = list(checkpoint_dir.glob('ckpt_*'))
    checkpoints = [ckpt for ckpt in checkpoints if (ckpt / 'deepspeed').exists()]
    if not checkpoints:
        return (None, None)
    ckpt_path = max(checkpoints, key=lambda x: int(x.stem.split('_')[-1]))
    ckpt_iter = int(ckpt_path.stem.split('_')[-1])
    return (ckpt_path, ckpt_iter)

def load_model_into_vllm(model: Union[DeepSpeedEngine, PreTrainedModel], llm: LLM) -> None:
    state_dict = model.module.state_dict() if isinstance(model, DeepSpeedEngine) else model.state_dict()
    llm.llm_engine.model_executor.driver_worker.model_runner.model.load_weights(state_dict.items())

def initialize_training_process_group(rank: int, world_size: int):
    master_addr = 'localhost'
    master_training_port = 8237
    os.environ['LOCAL_RANK'] = str(rank)
    torch.cuda.set_device(rank)
    if rank == 0:
        print(f'{'#' * 80}\n# Initializing the training NCCL PG with\n# world_size={world_size} \n{'#' * 80}')
    dist.init_process_group(backend='nccl', init_method=f'tcp://{master_addr}:{master_training_port}', world_size=world_size, rank=rank, timeout=timedelta(hours=1))
    dist.barrier(device_ids=[rank])
    print(f'Rank{rank}: training NCCL PG initialized. (world_size={world_size}, local_rank={rank}, gpu_id={torch.cuda.current_device()})')

def clean_up_checkpoints(exp_dir: Path, keep_every_n_steps: Optional[int]=None, exclude: Optional[List[Path]]=None) -> None:
    if exclude is None:
        exclude = []
    checkpoint_dir = exp_dir / 'checkpoints'
    for ckpt in checkpoint_dir.glob('ckpt_*'):
        if keep_every_n_steps is None or ckpt in exclude:
            continue
        ckpt_iter = int(ckpt.stem.split('_')[-1])
        if ckpt_iter % keep_every_n_steps == 0:
            removed_files_and_dirs = []
            for file in ckpt.iterdir():
                if file.name not in ['hf_model']:
                    try:
                        removed_files_and_dirs.append(file.name)
                        if file.is_dir():
                            shutil.rmtree(file, ignore_errors=True)
                    except Exception as e:
                        print(f'Error removing {file}: {e}')
            if len(removed_files_and_dirs) > 0:
                print(f'Removed non-hf_model files and dirs: of checkpoint {ckpt.name}')
            continue
        print(f'Removing checkpoint {ckpt}')
        shutil.rmtree(ckpt)

def fix_oov_logits_processor(inference_engine: LLM):
    tokenizer_vocab_size = len(inference_engine.get_tokenizer().get_vocab())

    def fix_oov(token_ids, logits):
        logits[tokenizer_vocab_size:] = -float('inf')
        return logits
    return fix_oov

def close_to_zero(tensor: torch.Tensor, mask: torch.Tensor, threshold: float=1e-08) -> torch.Tensor:
    close_to_zero_mask = torch.abs(tensor) < threshold
    num_close_to_zero = (close_to_zero_mask * mask).sum()
    return num_close_to_zero