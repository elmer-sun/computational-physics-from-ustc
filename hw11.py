import matplotlib.pyplot as plt
from Schrage_16807 import*
# 初始化参数

grid_size = 100  # 网格大小
def radom_choose(A,seed):
    x,seed=creat_array_seed_0_M(seed,1)
    l=len(A)
    id=x%l
    return A[id],seed


def generate_particle(size,seed,particle_position):
    a,seed=creat_array_seed_0_1(seed,2)
    x,y=size*a

    while np.linalg.norm(np.array([x,y]) - np.array(particle_position)) < size/3:
        a,seed=creat_array_seed_0_1(seed,2)
        x,y=size*a
    return int(x),int(y),seed


# 定义DLA生长函数
def dla(grid, num_particles):
    seed=seed_time()
    # 粒子的初始位置（种子）
    grid = np.zeros((grid_size, grid_size))
    particle_position = (grid_size // 2, grid_size // 2)
    grid[particle_position] = 1
    
    for j in range(num_particles):
        # 随机生成一个粒子在边界上
        x,y,seed = generate_particle(grid_size,seed,particle_position)
        # 随机游走直到到达团簇
        x_next,y_next=x,y
        test=0
        while not grid[x_next, y_next]:  # 检查是否到达团簇
            test+=1
            x,y=x_next,y_next
            step,seed = radom_choose(np.arange(4),seed)  # 四个方向：上、下、左、右
            if step == 0:  # 上
                y_next=y-1
            elif step == 1:  # 下
                y_next=y+1
            elif step == 2:  # 左
                x_next=x-1
            elif step == 3:  # 右
                x_next=x+1
            
            # 周期性边界条件
            x_next = x_next % grid_size
            y_next = y_next % grid_size
        # 将粒子添加到团簇中
        grid[x, y] = 1
        print("particle_%d,x=%d,y=%d"%(j+1,x,y))
    return grid



#dbm生长函数
def dbm(grid, eta, num_particles):
    #随机行走方法计算电势，进而算出下一个击穿的位置的概率
    def calculate_electric_potential(grid,seed):
        M=100
        candidate = np.zeros((grid_size, grid_size))#候选粒子概率分布
        grid_phi=grid.copy()#电势分布
        for i in range(1,grid_size-1):
            for j in range(1,grid_size-1):
                if grid_phi[i,j]!=1 and (grid_phi[i+1,j]==1 or grid_phi[i-1,j]==1 or grid_phi[i,j+1]==1 or grid_phi[i,j-1]==1):
                    phi=0
                    for k in range(M):
                        x=i
                        y=j
                        while x!=0 and x!=grid_size-1 and y!=0 and y!=grid_size-1 and grid_phi[x, y]!=1 :  # 检查是否到达团簇
                            step,seed = radom_choose(np.arange(4),seed)  # 四个方向：上、下、左、右
                            if step == 0:  # 上
                                y=y-1
                            elif step == 1:  # 下
                                y=y+1
                            elif step == 2:  # 左
                                x=x-1
                            elif step == 3:  # 右
                                x=x+1
                        phi+=grid_phi[x,y]
                    grid_phi[i,j]=phi/M
                    candidate[i,j]=(1-grid_phi[i,j])**eta
        return candidate,seed
    #按照概率分布随机抽取下一个击穿的点位
    def next_point(grid,candidate,seed):
        choice,seed=creat_array_seed_0_1(seed,1)
        sum=0
        for i in range(grid_size):
            for j in range(grid_size):
                sum+=candidate[i,j]
        p=0
        p_next=candidate[0,0]/sum
        for i in range(grid_size):
            for j in range(grid_size):
                p+=candidate[i,j]/sum
                i_next=i+(j+1)//grid_size
                j_next=(j+1)%grid_size
                p_next+=candidate[i_next,j_next]/sum
                if choice<p_next-candidate[i_next,j_next]/sum and choice>=p-candidate[i,j]/sum :
                    grid[i,j]=1 
                    print("x=%d,y=%d"%(i,j))
                    return grid,seed
    #开始执行
    seed=seed_time()
    # 粒子的初始位置（种子）
    grid = np.zeros((grid_size, grid_size))
    particle_position = (grid_size // 2, grid_size // 2)
    grid[particle_position] = 1
    for i in range(num_particles):
        print("particle_%d:"%(i+1), end=" ")
        candidate,seed=calculate_electric_potential(grid,seed)
        grid,seed=next_point(grid,candidate,seed)
    return grid 


def draw_picture(a,b):
    plt.imshow(a,cmap='Greys', interpolation='none')
    plt.axis('off')
    plt.title(b)
    plt.show()

num_particles = 1000
# DLA
# 初始化网格
grid = np.zeros((grid_size, grid_size))
# 运行DLA模拟
dla_cluster = dla(grid, num_particles)
draw_picture(dla_cluster,"DLA")
grid = np.zeros((grid_size, grid_size))
# 运行介电击穿模型
num_particles = 100
eta=2
dbm_cluster=dbm(grid,eta,num_particles)
draw_picture(dbm_cluster,"DBM,eta=2")

eta=10
dbm_cluster=dbm(grid,eta,num_particles)
draw_picture(dbm_cluster,"DBM,eta=10")