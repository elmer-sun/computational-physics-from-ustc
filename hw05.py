import matplotlib.pyplot as plt
import time
import numpy as np
def seed_time():#获取时间，作为种子
    t = time.localtime(time.time())
    localtime = time.asctime( t )
    print ("localtime :", localtime,"\par")
    return t.tm_year-2000 + 70*(t.tm_mon+12*(t.tm_mday+31*(t.tm_hour+23*(t.tm_min+59*t.tm_sec))))
class Schrage16807(object):#用的是之前已写过的class来生成随机数
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
    s = seed_time()
    r = Schrage16807(s)
    N = 5000
    #直接抽样均匀分布的u，v。其实u和v不需要使用不同的随机数，间隔特定长度l也可以，因为自相关系数很小，可认为u，v仍然独立
    ar=np.array(r.creat_arry(N))
    ru=ar[0:int(N/2)]*2-1
    rv=ar[int(N/2):N]*2-1
    u1=[]
    v1=[]
    #舍去平方和大于一的
    for i in range (int(N/2)):
        if ru[i]**2+rv[i]**2<1:
            u1.append(ru[i])
            v1.append(rv[i])
    u=np.array(u1)
    v=np.array(v1)
    r2 = u**2+v**2
    x = 2*u*np.sqrt(1-r2)
    y = 2*v*np.sqrt(1-r2)
    z = 1-2*r2


    #绘图
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.scatter(x,y,z,s=0.5,c="pink")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D ")

    ax = fig.add_subplot(1, 2, 2)
    ax.scatter(x,y,marker='x',s=15,c="pink")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("2D ")

    plt.axis('equal')
    plt.show()
    

