import matplotlib.pyplot as plt
import pandas as pd
from Schrage_16807 import*
# 初始化参数
# 在作业11的基础上修改而来
grid_size = 1000  # 网格大小
def radom_choose(A,seed):
    x,seed=creat_array_seed_0_M(seed,1)
    l=len(A)
    id=x%l
    return A[id],seed


def generate_particle(size,seed,distance):
    def choose(x,l_0,l_1):
        if x<0.5:
            x=-l_0+(x-0.5)*2*(l_1-l_0)
        else:
            x=l_0+(x-0.5)*2*(l_1-l_0)
        return x+size//2
    a,seed=creat_array_seed_0_1(seed,2)
    l_0=min(1.5*distance,distance+50)
    l_1=min(distance*2,size//2,distance+100)
    x,y=a
    x=choose(x,l_0,l_1)
    y=choose(y,l_0,l_1)
    return int(x),int(y),seed


# 定义DLA生长函数
def dla(grid, num_particles):
    seed=seed_time()
    # 粒子的初始位置（种子）
    grid = np.zeros((grid_size, grid_size))
    particle_position = (grid_size // 2, grid_size // 2)
    grid[particle_position] = 1
    distance=5
    j=0
    while(j<num_particles):
        # 随机生成一个粒子在边界上
        x,y,seed = generate_particle(grid_size,seed,distance)
        # 随机游走直到到达团簇
        x_next,y_next=x,y
        c=0
        while not grid[x_next, y_next]:  # 检查是否到达团簇
            x,y=x_next,y_next
            step,seed = radom_choose(np.arange(4),seed)  # 四个方向：上、下、左、右
            if step == 0:  # 上
                y_next=(y-1)%grid_size
            elif step == 1:  # 下
                y_next=(y+1)%grid_size
            elif step == 2:  # 左
                x_next=(x-1)%grid_size
            elif step == 3:  # 右
                x_next=(x+1)%grid_size
            
            if np.linalg.norm(np.array([x,y]) - np.array(particle_position)) > 2.5*distance :
                c=1
                break
        if c:
            continue 
        # 将粒子添加到团簇中
        grid[x, y] = 1
        if np.linalg.norm(np.array([x,y]) - np.array(particle_position)) > distance:
            distance=np.linalg.norm(np.array([x,y]) - np.array(particle_position))
        print("particle_%d,x=%d,y=%d"%(j+1,x,y))
        j+=1
    return grid

def draw_picture(a,b):
    plt.imshow(a,cmap='Greys', interpolation='none')
    plt.axis('off')
    plt.title(b)
    plt.show()

num_particles = 10000
# DLA
# 初始化网格
grid = np.zeros((grid_size, grid_size))
# 运行DLA模拟
dla_cluster = dla(grid, num_particles)
# 将DataFrame写入CSV文件
df = pd.DataFrame(dla_cluster)
file_path = r'D:\physics\computational physics\homework\17\output-dla.csv' 
df.to_csv(file_path, index=False, header=False)


