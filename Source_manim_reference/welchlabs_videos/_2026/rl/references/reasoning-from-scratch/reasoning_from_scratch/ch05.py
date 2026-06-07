from .ch03 import extract_final_candidate, render_prompt
from .ch04 import generate_text_stream_concat_flex, generate_text_top_p_stream_cache
import math
import torch

def heuristic_score(answer, prompt=None, brevity_bonus=500.0, boxed_bonus=2.0, extract_bonus=1.0, fulltext_bonus=0.0):
    score = 0.0
    cand = extract_final_candidate(answer, fallback='none')
    if cand:
        score += boxed_bonus
    else:
        cand = extract_final_candidate(answer, fallback='number_only')
        if cand:
            score += extract_bonus
        else:
            cand = extract_final_candidate(answer, fallback='number_then_full')
            if cand:
                score += fulltext_bonus
    score += 1.5 * math.exp(-len(answer) / brevity_bonus)
    return score

@torch.inference_mode()
def calc_next_token_probas(model, tokenizer, prompt, device):
    token_ids = torch.tensor(tokenizer.encode(prompt), device=device)
    logits = model(token_ids.unsqueeze(0)).squeeze(0)
    all_probas = torch.softmax(logits, dim=-1)
    t_idx = torch.arange(0, token_ids.shape[0] - 1, device=device)
    next_ids = token_ids[1:]
    next_token_probas = all_probas[t_idx, next_ids]
    print('Next-token probabilities:', [p.item() for p in next_token_probas])
    print('Joint probability:', torch.prod(next_token_probas))

@torch.inference_mode()
def calc_next_token_logprobas(model, tokenizer, prompt, device):
    token_ids = torch.tensor(tokenizer.encode(prompt), device=device)
    logits = model(token_ids.unsqueeze(0)).squeeze(0)
    all_logprobas = torch.log_softmax(logits, dim=-1)
    t_idx = torch.arange(0, token_ids.shape[0] - 1, device=device)
    next_ids = token_ids[1:]
    next_token_logprobas = all_logprobas[t_idx, next_ids]
    print('Next-token log-probabilities:', [p.item() for p in next_token_logprobas])
    print('Joint log-probability:', torch.sum(next_token_logprobas))

@torch.inference_mode()
def avg_logprob_answer(model, tokenizer, prompt, answer, device='cpu'):
    prompt_ids = tokenizer.encode(prompt)
    answer_ids = tokenizer.encode(answer)
    full_ids = torch.tensor(prompt_ids + answer_ids, device=device)
    logits = model(full_ids.unsqueeze(0)).squeeze(0)
    logprobs = torch.log_softmax(logits, dim=-1)
    start = len(prompt_ids) - 1
    end = full_ids.shape[0] - 1
    t_idx = torch.arange(start, end, device=device)
    next_tokens = full_ids[start + 1:end + 1]
    next_token_logps = logprobs[t_idx, next_tokens]
    return torch.mean(next_token_logps).item()

def make_critique_prompt(raw_prompt, draft):
    return f'You are a meticulous reviewer. Identify logical errors, missing steps, or arithmetic mistakes. If the answer seems correct, say so briefly. Then propose a concise plan to fix issues.\n\nQuestion:\n{raw_prompt}\n\nDraft answer:\n{draft}\n\nWrite a short critique and bullet-point fix plan (under ~120 words).\nCritique:'

def make_refine_prompt(raw_prompt, draft, critique):
    return f'Revise the answer using the critique. Keep it concise and end with a final boxed result: \\boxed{{ANSWER}}\n\nQuestion:\n{raw_prompt}\n\nPrevious answer:\n{draft}\n\nCritique:\n{critique}\n\nRevised answer:'

def self_refinement_loop(model, tokenizer, raw_prompt, device, iterations=2, max_response_tokens=2048, max_critique_tokens=256, score_fn=None, prompt_renderer=render_prompt, prompt_suffix='', verbose=False, temperature=0.7, top_p=0.9):
    steps = []
    prompt = prompt_renderer(raw_prompt) + prompt_suffix
    current_full = generate_text_stream_concat_flex(model=model, tokenizer=tokenizer, prompt=prompt, device=device, max_new_tokens=max_response_tokens, verbose=False, generate_func=generate_text_top_p_stream_cache, temperature=temperature, top_p=top_p)
    current_extracted = extract_final_candidate(current_full, fallback='number_then_full')
    if score_fn:
        current_score = score_fn(answer=current_full, prompt=prompt)
    else:
        current_score = 0.0
    for it in range(iterations):
        draft_before_full = current_full
        draft_before_extracted = current_extracted
        score_before = current_score
        critique_prompt = make_critique_prompt(raw_prompt, draft_before_full)
        critique_full = generate_text_stream_concat_flex(model=model, tokenizer=tokenizer, prompt=critique_prompt, device=device, max_new_tokens=max_critique_tokens, verbose=False, generate_func=generate_text_top_p_stream_cache, temperature=temperature, top_p=top_p)
        refine_prompt = make_refine_prompt(raw_prompt, draft_before_full, critique_full)
        revised_full = generate_text_stream_concat_flex(model=model, tokenizer=tokenizer, prompt=refine_prompt, device=device, max_new_tokens=max_response_tokens, verbose=False, generate_func=generate_text_top_p_stream_cache, temperature=temperature, top_p=top_p)
        revised_extracted = extract_final_candidate(revised_full, fallback='number_then_full')
        if score_fn:
            revised_score = score_fn(answer=revised_full, prompt=prompt)
        else:
            revised_score = 0.0
        step = {'iteration': it + 1, 'draft_full': draft_before_full, 'draft_extracted': draft_before_extracted, 'critique': critique_full, 'revised_full': revised_full, 'revised_extracted': revised_extracted, 'score_before': score_before, 'score_after': revised_score}
        steps.append(step)
        if verbose:
            print(f'[Refinement {it + 1}/{iterations}]\nCurrent: {draft_before_extracted}\nRevised: {revised_extracted}\nScore before: {score_before:.3f}\nScore after: {revised_score:.3f}\n{'=' * 25}')
        if revised_score >= current_score:
            current_full = revised_full
            current_extracted = revised_extracted
            current_score = revised_score
    return {'final_full': current_full, 'final_extracted': current_extracted, 'steps': steps}