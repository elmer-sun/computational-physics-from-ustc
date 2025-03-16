import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
# 模拟区域参数
Nx = 300
Ny = 300
dx = 0.03
dy = 0.03

# 时间积分参数
nstep = 1000
dtime = 2.0e-4

# 材料特定参数
tau = 0.0003
epsilonb = 0.01
mu = 1.0
kappa = 2.0
delta = 0.02
aniso = 4.0
alpha = 0.9
gamma = 10.0
teq = 1.0
theta0 = 0
seed = 3.0
a=0.01
def nucleus(Nx, Ny, seed):
    phi = np.zeros((Nx, Ny))
    tempr = np.zeros((Nx, Ny))
    for i in range(Nx):
        for j in range(Ny):
            if ((i - Nx / 2) ** 2 + (j - Ny / 2) ** 2 < seed ** 2):
                phi[i, j] = 1.0
    return phi, tempr
def dendritic(Nx, Ny):
    phi = np.zeros((Nx, Ny))
    tempr = np.zeros((Nx, Ny))
    phi[-1, int(Nx/2)]=1
    return phi, tempr
def stimulation(phi, tempr,name):
    def calculate_derivatives(phi, tempr):
        lap_phi = np.zeros_like(phi)
        lap_tempr = np.zeros_like(tempr)
        phidx = np.zeros_like(phi)
        phidy = np.zeros_like(phi)
        epsilon = np.zeros_like(phi)
        epsilon_deriv = np.zeros_like(phi)

        for i in range(1, Nx - 1):
            for j in range(1, Ny - 1):
                # 计算拉普拉斯算子
                lap_phi[i, j] = (phi[i + 1, j] + phi[i - 1, j] + 
                    phi[i, j + 1] + phi[i, j - 1] - 4 * phi[i, j]) / (dx * dy)
                lap_tempr[i, j] = (tempr[i + 1, j] + tempr[i - 1, j] +
                    tempr[i, j + 1] + tempr[i, j - 1] - 4 * tempr[i, j]) / (dx * dy)

                # 计算笛卡尔导数
                phidx[i, j] = (phi[i + 1, j] - phi[i - 1, j]) / (2 * dx)
                phidy[i, j] = (phi[i, j + 1] - phi[i, j - 1]) / (2 * dy)

                # 计算角度
                theta = np.arctan2(phidy[i, j], phidx[i, j])

                # 计算epsilon及其导数
                epsilon[i, j] = epsilonb * (1.0 + delta * np.cos(aniso * (theta - theta0)))
                epsilon_deriv[i, j] = -epsilonb * aniso * delta * np.sin(
                    aniso * (theta - theta0))

        # 处理边界条件
        lap_phi[0, :] = lap_phi[1, :]
        lap_phi[-1, :] = lap_phi[-2, :]
        lap_phi[:, 0] = lap_phi[:, 1]
        lap_phi[:, -1] = lap_phi[:, -2] 
        lap_tempr[0, :] = lap_tempr[1, :]
        lap_tempr[-1, :] = lap_tempr[-2, :]
        lap_tempr[:, 0] = lap_tempr[:, 1]
        lap_tempr[:, -1] = lap_tempr[:, -2]

        # 处理边界点的phidx和phidy
        phidx[0, :] = (phi[1, :] - phi[0, :]) / dx
        phidx[-1, :] = (phi[-1, :] - phi[-2, :]) / dx
        phidy[:, 0] = (phi[:, 1] - phi[:, 0]) / dy
        phidy[:, -1] = (phi[:, -1] - phi[:, -2]) / dy

        epsilon[0, :] = epsilon[1, :]
        epsilon[-1, :] = epsilon[-2, :]
        epsilon[:, 0] = epsilon[:, 1]
        epsilon[:, -1] = epsilon[:, -2]
        epsilon_deriv[0, :] = epsilon_deriv[1, :]
        epsilon_deriv[-1, :] = epsilon_deriv[-2, :]
        epsilon_deriv[:, 0] = epsilon_deriv[:, 1]
        epsilon_deriv[:, -1] = epsilon_deriv[:, -2]

        term1 = np.zeros_like(phi)
        for i in range(1, Nx - 1):
            for j in range(1, Ny - 1):
                term1[i, j] = (epsilon[i, j + 1] * epsilon_deriv[i, j + 1] * phidx[i, j + 1] -
                epsilon[i, j - 1] * epsilon_deriv[i, j - 1] * phidx[i, j - 1])/(2 * dy)

        term2 = np.zeros_like(phi)
        for i in range(1, Nx - 1):
            for j in range(1, Ny - 1):
                term2[i, j] = -(epsilon[i + 1, j] * epsilon_deriv[i + 1, j] * phidy[i + 1, j] -
                epsilon[i - 1, j] * epsilon_deriv[i - 1, j] * phidy[i - 1, j]) / (2 * dx)

        return lap_phi, lap_tempr, term1, term2, epsilon

    # 记录开始时间
    time0 = time.time()
    # 时间演化循环
    for istep in range(1, nstep + 1):
        # 计算拉普拉斯算子和epsilon及其导数
        lap_phi, lap_tempr, term1, term2, epsilon= calculate_derivatives(phi, tempr)

        # 计算m
        m = alpha / np.pi * np.arctan(gamma * (teq - tempr))

        # 相场时间演化
        phi_old=phi
        phi = phi + (dtime / tau) * (
            term1 + term2 + epsilon**2* lap_phi + phi * (1 - phi) * ((phi - 0.5 + m)+
                a*np.random.choice([-0.5, 0.5], size=(Nx, Ny))))

        # 温度场时间演化
        tempr = tempr + dtime * lap_tempr + kappa * (phi - phi_old)

        print(f"done step: {istep}")
    # 计算计算时间
    compute_time = time.time() - time0
    print(f"Compute Time: {compute_time}")


    df = pd.DataFrame(phi)
    file_path = r'D:\physics\computational physics\homework\18\phi_{}.csv'.format(name)
    df.to_csv(file_path, index=False, header=False)
    # 绘制结果
    plt.imshow(phi, cmap='viridis')
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    # 使用原始字符串或者双反斜杠
    save_path = r'D:\physics\computational physics\homework\18\phi_{}.png'.format(name)
    plt.savefig(save_path,dpi=300)
    plt.clf()



phi, tempr = dendritic(Nx, Ny)
delta=0.01
stimulation(phi,tempr,'dendritic growth---0.0')
phi, tempr = dendritic(Nx, Ny)
delta=0.02
stimulation(phi,tempr,'dendritic growth---0.02')
phi, tempr = dendritic(Nx, Ny)
delta=0.05
stimulation(phi,tempr,'dendritic growth---0.05')

aniso = 6
delta=0.04
phi, tempr = nucleus(Nx, Ny, seed)
kappa=1.0
stimulation(phi,tempr,'ice dendrites--1.0')
phi, tempr = nucleus(Nx, Ny, seed)
kappa=1.5
stimulation(phi,tempr,'ice dendrites--1.5')
phi, tempr = nucleus(Nx, Ny, seed)
kappa=2.0
stimulation(phi,tempr,'ice dendrites--2.0')