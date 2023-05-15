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
    

# 对比较策略更新过程
def compare_process(fitness_list, num_iterations):
    for t in range(num_iterations):
        parent_index = np.random.choice(range(len(fitness_list)))
        child_index = np.random.choice(range(len(fitness_list)))
        if fitness_list[child_index] > fitness_list[parent_index]:
            fitness_list[parent_index] = fitness_list[child_index]
    return fitness_list
    

# 模拟一次随机性演化博弈动力学多人最后通牒博弈
def simulate_game(num_iterations=1000, num_rounds=10000):
    # 初始化参数
    p_values = np.zeros(num_iterations)  # 记录每次迭代中的平均p值
    q_values = np.zeros(num_iterations)  # 记录每次迭代中的平均q值
    fitness_values = np.zeros((num_rounds, len(p_values)))  # 记录每次实验中每个p值的回应者收益

    # 开始模拟
    for t in range(num_iterations):
        # 进行一次实验并记录数据
        p_values[t] = np.random.uniform()  # 随机初始化一个p值
        for j in range(num_rounds):
            proposer_payoff, responder_payoff = play_game(p_values[t])
            fitness_values[j][t] = responder_payoff

        # 对比较策略更新过程
        fitness_values[:, t] = compare_process(fitness_values[:, t], num_iterations)

        # 更新q值
        total_responder_payoff = np.sum(fitness_values[:, t])
        avg_responder_payoff = total_responder_payoff / len(fitness_values[:, t])
        q_values[t] = avg_responder_payoff

    # 绘制 p 和 q 的分布辩护图
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(range(num_iterations), p_values, label='Average p')
    ax.plot(range(num_iterations), q_values, label='Average q')
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Distribution of p and q over Time')
    plt.show()


simulate_game()
