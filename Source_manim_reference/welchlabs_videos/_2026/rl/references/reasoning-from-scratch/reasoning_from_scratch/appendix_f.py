from reasoning_from_scratch.ch02 import generate_text_basic_stream_cache

def predict_choice(model, tokenizer, prompt_fmt, max_new_tokens=8):
    pred = None
    for t in generate_text_basic_stream_cache(model=model, token_ids=prompt_fmt, max_new_tokens=max_new_tokens, eos_token_id=tokenizer.eos_token_id):
        answer = tokenizer.decode(t.squeeze(0).tolist())
        for letter in answer:
            letter = letter.upper()
            if letter in 'ABCD':
                pred = letter
                break
        if pred:
            break
    return pred

def elo_ratings(vote_pairs, k_factor=32, initial_rating=1000):
    ratings = {model: initial_rating for pair in vote_pairs for model in pair}
    for winner, loser in vote_pairs:
        rating_winner, rating_loser = (ratings[winner], ratings[loser])
        expected_winner = 1.0 / (1.0 + 10 ** ((rating_loser - rating_winner) / 400.0))
        ratings[winner] = rating_winner + k_factor * (1 - expected_winner)
        ratings[loser] = rating_loser + k_factor * (0 - (1 - expected_winner))
    return ratings