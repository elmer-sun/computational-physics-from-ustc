import matplotlib.pyplot as plt
import numpy as np
import time
def seed_time():#获取时间，作为种子
    t = time.localtime(time.time())
    localtime = time.asctime( t )
    print ("localtime :", localtime,"\par")
    return t.tm_year-2000 + 70*(t.tm_mon+12*(t.tm_mday+31*(t.tm_hour+23*(t.tm_min+59*t.tm_sec))))
class Schrage16807(object):#用的是之前已写过class来生成随机数
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

if __name__ == "__main__":
    seed = seed_time()
    #生成10000个随机数，一半用于生成θ，一半用于生成Φ
    N=int(10000)
    test1 = Schrage16807(seed)
    data=test1.creat_arry(N) 
    #prime是随机分布的（均匀）
    theta_prime=np.array(data[0:int(N/2)])
    phi_prime=np.array(data[int(N/2):N])
    #直接抽样
    theta = np.arccos(1-theta_prime)
    phi = phi_prime*2*np.pi
    #三维表示
    x = np.sin(theta)*np.cos(phi)
    y = np.sin(theta)*np.sin(phi)
    z = np.cos(theta)
    #开始画图
    fig = plt.figure() 
    ax = plt.axes(projection ="3d")
    ax.scatter3D(x, y, z,s = 0.5,c='pink')
    plt.title("Evenly distributed on the upper hemisphere")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")   
    plt.show()
    for i in range(N):
        print("x=%.3f,y=%.3f,z=%.3f \par"%(x[i],y[i],z[i]))
