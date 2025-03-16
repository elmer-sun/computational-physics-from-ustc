import numpy as np
import matplotlib.pyplot as plt
import time

def seed_time():#获取时间，作为种子
    t = time.localtime(time.time())
    localtime = time.asctime( t )
    print ("localtime :", localtime,"\par")
    return t.tm_year-2000 + 70*(t.tm_mon+12*(t.tm_mday+31*(t.tm_hour+23*(t.tm_min+59*t.tm_sec))))
class Schrage16807(object):#祖传生成器，一直用这个生成随机数
    def __init__(self,seed):
        self.__seed = seed
        self.__M = 2147483647
        self.__a = 16807

    def __rand1(self, i_n):#随机数迭代-iteration，取模
        a = self.__a
        m = self.__M
        q = m//a
        r = m%a
        i_next = a * (i_n % q) - r * (i_n // q)
        if i_next < 0:
            return i_next + m
        else:
            return i_next

    def rand1(self):#取成0到1
        self.__seed = self.__rand1(self.__seed)
        return self.__seed/self.__M
    
    def creat_arry(self,N):#输出一个长度为N的列表
        data = [self.rand1() for i in range(N)] 
        return data
if __name__=='__main__':
    PI = np.pi  
    gauss = lambda x: np.exp(-(x**2)/2)#并未归一化的函数，最大值是一，刚好和y配合。
    gauss_1=lambda x: np.exp(-(x**2)/2)*(1+x**2/2)
    gauss_2=lambda x: 1/(1+x**2/2)
    N = 10**6
    l =5
    L=1000#理论上高斯分布x定义域为整条实轴，为简单起见认为x属于[-L,L]，画图也不可能无限长
    seed = seed_time()
    r = Schrage16807(seed)
    x=np.array(r.creat_arry(int(N+l)))
    x_1=np.sqrt(2)*np.tan(PI* (x[0:N]-1/2))
    y_1=x[l:N+l]
    #对x_result gauss分布进行舍选，利用乘分布
    x_result = []
    for i in range(N):
        if y_1[i]<gauss_1(x_1[i]):
            x_result.append(x_1[i])

    sample_rate = len(x_result)/len(x_1)

    #输出采样效率
    print(" rate of sampling：",sample_rate)
    #绘制直方图与概率密度分布图像
    fig, ax = plt.subplots()
    bin=np.linspace(-4, 4, 101)
    #直方图，已归一化
    ax.hist(x_result, bin, density=True, color="hotpink",label='histogram of data')
    #高斯分布，已归一化
    A=np.sqrt(1/(2*PI))
    y = np.array([A*gauss(x_i) for x_i in bin])
    ax.plot(bin, y, '--',label="Gauss")
    ax.set_xlabel('X')
    ax.set_ylabel('Probability density')
    #画在一张图
    ax.legend()
    fig.tight_layout()
    plt.show()


