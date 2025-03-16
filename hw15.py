import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from Schrage_16807 import*


# 定义能量函数
def H(x, y):
    return -(x**2 + y**2) + 0.5 * (x**4 + y**4) + (x - y)**4 / 3

# 定义Metropolis抽样
def metropolis_sampling(beta, steps, initial_state):
    seed=seed_time()
    x, y = initial_state
    acceptance_count = 0
    x_values=[]
    y_values=[]

    for _ in range(steps):
        # 随机选择新状态
        x_new,seed = rand_x_to_y(seed,-1, 1)
        x_new+=x
        y_new,seed = rand_x_to_y(seed,-1, 1)
        y_new+=y
        # 计算能量变化
        delta_E = H(x_new, y_new) - H(x, y)

        # 根据Metropolis准则决定是否接受新状态
        rand,seed=creat_array_seed_0_1(seed,1)
        if delta_E < 0 or rand < np.exp(-beta * delta_E):
            x, y = x_new, y_new
            acceptance_count += 1
        x_values.append(x)
        y_values.append(y)
    # 计算期望值
    a=np.array(x_values)
    b=np.array(y_values)
    x_square_avg = np.mean(a**2)
    y_square_avg = np.mean(b**2)
    xy_square_avg = x_square_avg + y_square_avg
    print(f"For beta = {beta}:\\par")
    print(f"  \\(<x^2>\\) = {x_square_avg:.6f}\\par")
    print(f"  \\(<y^2>\\) = {y_square_avg:.6f}\\par")
    print(f"  \\(<x^2 + y^2>\\) = {xy_square_avg:.6f}\\par")
    print(f"  Acceptance rate = {acceptance_count/steps}\\par")
    print()

    return x_values,y_values

# 可视化Markov链点分布
def plot_markov_chain(beta, x_values,y_values,num):
    xy = np.column_stack((x_values[:num], y_values[:num]))#计算密度
    kde = gaussian_kde(xy.T)  
    z = kde(xy.T)  
    plt.scatter(x_values[:num], y_values[:num], c=z,s=1,cmap='viridis')
    plt.xlim(-3, 3)  
    plt.ylim(-3, 3)
    plt.title(f"Markov Chain for beta = {beta}")
    plt.colorbar(label='Density',ticks=[])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
# 画出概率密度函数的热度图
def draw_Px(beta):
    x = np.linspace(-3, 3, 600)
    y = np.linspace(-3, 3, 600)
    X, Y = np.meshgrid(x, y)

    # 在网格上评估函数
    Z = np.exp(-beta * H(X,Y))

    # 绘制热度图
    plt.pcolormesh(X, Y, Z, cmap='viridis')
    plt.colorbar(label='density',ticks=[])
    plt.title('Heatmap for beta=%s'%(beta))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


if __name__=="__main__":
    # 参数设置
    beta_values = [0.2, 1, 5]
    steps = 10**6
    initial_state = (0, 0)

    # 进行Metropolis抽样
    x=[]
    y=[]
    for beta in beta_values:
        x_values,y_values = metropolis_sampling(beta, steps, initial_state)
        x.append(x_values)
        y.append(y_values)
    #画图
    # for i in range(len(beta_values)):
    #     plot_markov_chain(beta_values[i], x[i],y[i],10**4)
    # for beta in beta_values:
    #     draw_Px(beta)