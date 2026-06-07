import json
import math
import argparse
import torch
from reasoning_from_scratch.ch02 import get_device

def bradley_terry_torch(vote_pairs, device):
    models = sorted({m for winner, loser in vote_pairs for m in (winner, loser)})
    n = len(models)
    idx = {m: i for i, m in enumerate(models)}
    winners = torch.tensor([idx[winner] for winner, _ in vote_pairs], dtype=torch.long)
    losers = torch.tensor([idx[loser] for _, loser in vote_pairs], dtype=torch.long)
    theta = torch.nn.Parameter(torch.zeros(n - 1, device=device))
    optimizer = torch.optim.Adam([theta], lr=0.01, weight_decay=0.0001)

    def scores():
        return torch.cat([theta, torch.zeros(1, device=device)])
    for epoch in range(500):
        s = scores()
        delta = s[winners] - s[losers]
        loss = -torch.nn.functional.logsigmoid(delta).mean()
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        s = scores()
        scale = 400.0 / math.log(10.0)
        R = s * scale
        R -= R.mean()
        R += 1000.0
    return {m: float(r) for m, r in zip(models, R.cpu().tolist())}

def main():
    parser = argparse.ArgumentParser(description='Bradley-Terry leaderboard.')
    parser.add_argument('--path', type=str, help='Path to votes JSON')
    args = parser.parse_args()
    with open(args.path, 'r', encoding='utf-8') as f:
        votes = json.load(f)
    device = get_device()
    ratings = bradley_terry_torch(votes, device)
    leaderboard = sorted(ratings.items(), key=lambda x: -x[1])
    print('\nLeaderboard (Bradley-Terry)')
    print('-----------------------------')
    for i, (model, score) in enumerate(leaderboard, 1):
        print(f'{i:>2}. {model:<10} {score:7.1f}')
    print()
if __name__ == '__main__':
    main()