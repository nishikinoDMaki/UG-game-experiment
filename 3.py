import numpy as np
import matplotlib.pyplot as plt

# 定义参与方数量
num_proposers = 1
num_responders = 3


# 最后通牒博弈的策略
def strategy(last_offer, p):
    # 如果上一次提议者的报价比p小，则所有回应者都拒绝
    if last_offer < p:
        return np.zeros(num_responders)
    # 否则所有回应者都同意，并按比例分配收益
    else:
        offer = (3 - 3 * p) / num_responders
        return np.ones(num_responders) * offer


# 最后通牒博弈的单次对局
def play_game(p):
    offer = np.random.uniform(0, 1)  # 提议者随机报价
    responses = strategy(offer, p)  # 回应者根据报价及 p 值做出决策
    acceptance = np.all(responses >= p)  # 判断是否所有回应者都同意
    proposer_payoff = 3 - 3 * p if acceptance else 0  # 提议者的收益
    responder_payoff = p if acceptance else 0  # 回应者的收益
    return proposer_payoff, responder_payoff
    

# Moran策略更新过程
def moran_process(fitness_list, num_iterations):
    for t in range(num_iterations):
        total_fitness = np.sum(fitness_list)
        probabilities = fitness_list / total_fitness
        parent_index = np.random.choice(range(len(fitness_list)), p=probabilities)
        child_index = np.random.choice(range(len(fitness_list)))
        fitness_list[child_index] = fitness_list[parent_index]
    return fitness_list
    

# 模拟一次随机性演化博弈动力学多人最后通牒博弈
def simulate_game():
    # 初始化参数
    p_values = np.linspace(0, 1, 51)  # 将p分成50个间隔
    q_values = np.zeros(len(p_values))

    # 进行一次实验并记录数据
    fitness_values = np.zeros(len(p_values))
    for j in range(len(p_values)):
        p = p_values[j]
        proposer_payoff, responder_payoff = play_game(p)
        fitness_values[j] = responder_payoff

    # Moran策略更新过程
    fitness_values = moran_process(fitness_values, 1)

    # 更新q值
    total_responder_payoff = np.sum(fitness_values)
    avg_responder_payoff = total_responder_payoff / len(fitness_values)
    q_values = np.ones(len(p_values)) * avg_responder_payoff

    # 绘制 p 和 q 的分布辩护图
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(p_values, p_values, 'k--', label='y=x')
    ax.plot(p_values, q_values, label='q(p)', color='C1')
    ax.legend()
    ax.set_xlabel('p')
    ax.set_ylabel('q')
    ax.set_title('Distribution of p and q')
    plt.show()


simulate_game()
