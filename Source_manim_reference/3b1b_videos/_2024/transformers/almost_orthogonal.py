import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
num_vectors = 10000
vector_len = 100
big_matrix = torch.randn(num_vectors, vector_len)
big_matrix /= big_matrix.norm(p=2, dim=1, keepdim=True)
big_matrix.requires_grad_(True)
optimizer = torch.optim.Adam([big_matrix], lr=0.01)
num_steps = 250
losses = []
dot_diff_cutoff = 0.01
big_id = torch.eye(num_vectors, num_vectors)
for step_num in tqdm(range(num_steps)):
    optimizer.zero_grad()
    dot_products = big_matrix @ big_matrix.T
    diff = dot_products - big_id
    loss = (diff.abs() - dot_diff_cutoff).relu().sum()
    loss += num_vectors * diff.diag().pow(2).sum()
    loss.backward()
    optimizer.step()
    losses.append(loss.item())
plt.plot(losses)
plt.grid(1)
plt.show()
dot_products = big_matrix @ big_matrix.T
norms = torch.sqrt(torch.diag(dot_products))
normed_dot_products = dot_products / torch.outer(norms, norms)
angles_degrees = torch.rad2deg(torch.acos(normed_dot_products.detach()))
self_orthogonality_mask = ~torch.eye(num_vectors, num_vectors).bool()
plt.hist(angles_degrees[self_orthogonality_mask].numpy().ravel(), bins=1000, range=(80, 100))
plt.grid(1)
plt.show()