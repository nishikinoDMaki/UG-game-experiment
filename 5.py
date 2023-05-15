import random
import numpy as np
import matplotlib.pyplot as plt

# 参与者数目
N = 2000
# 报价数组
p_range = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
# 接受价格数组
q_range = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
# 每组参与者数目
M = 7
# 回应者数目
K = 6

# 初始化策略
proposer_strategy = p_range.copy()
responder_strategy = q_range.copy()

# 记录每轮实验的结果
results = []

# 进行1000轮实验
for _ in range(10000):
    # 随机选择一个提议者
    proposer_index = random.randint(0, M-1)
    proposer_offer = proposer_strategy[proposer_index]

    # 随机选择 K 个回应者
    num_responders = min(K, N-M, len(responder_strategy))
    responder_indices = []
    while len(responder_indices) < num_responders:
        i = random.randint(M, N-1)
        if i not in responder_indices and i < len(responder_strategy):
            responder_indices.append(i)

    # 检查回应者的反应
    all_accepted = True
    for i in responder_indices:
        responder_price = responder_strategy[i]
        if responder_price < proposer_offer:
            all_accepted = False
            break

    # 根据反应更新策略
    if all_accepted:
        proposer_payoff = 3 - 3 * proposer_offer
        responder_payoff = proposer_offer
        best_responder_index = responder_indices[np.argmax(responder_strategy[responder_indices])]
        responder_strategy[best_responder_index] = max(responder_strategy)
        proposer_strategy[proposer_index] = max(proposer_strategy)
        for i in responder_indices:
            if i != best_responder_index:
                responder_strategy[i] = max(responder_strategy)
    else:
        proposer_payoff = 0
        responder_payoff = 0

    # 记录结果
    results.append(proposer_payoff + responder_payoff)

# 画出提议者的最后状态分布直方图
plt.hist(proposer_strategy, bins=9)
plt.xlabel('Offer')
plt.ylabel('Number of players')
plt.title('Proposer final strategy distribution')
plt.show()

# 画出回应者的最后状态分布直方图
plt.hist(responder_strategy, bins=9)
plt.xlabel('Acceptance price')
plt.ylabel('Number of players')
plt.title('Responder final strategy distribution')
plt.show()
