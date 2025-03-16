#第一题
import time
import statistics
from scipy.stats import chi2 #调用卡方分布
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

#Schrahe16807类
#随机输入初始值，反复调用rand(),得到随机数列
class Schrage16807(object):
    def __init__(self,seed):
        self.__seed = seed
        self.__M = 2147483647
        self.__a = 16807

    def __iter_rand(self, i_n):#随机数迭代-iteration，取模
        a = self.__a
        m = self.__M
        q = m//a
        r = m%a
        i_next = a * (i_n % q) - r * (i_n // q)
        if i_next < 0:
            return i_next + m
        else:
            return i_next

    def rand(self):#取成0到1
        self.__seed = self.__iter_rand(self.__seed)
        return self.__seed/self.__M

#取计算机时间为种子值
def seed_time():
    t = time.localtime(time.time())
    return t.tm_year-2000 + 70*(t.tm_mon+12*(t.tm_mday+31*(t.tm_hour+23*(t.tm_min+59*t.tm_sec))))


#计算随机数一致性，求渐近Chi2的统计检验量
def uniformity(data, k = 10):#分成k个均匀区间
    lp = np.linspace(0,1,k+1)
    nk = [0] * k
    size = len(data)
    for i in range(size):
        j =int((data[i]*k)//1)#判断列表中每个元素在什么区间
        nk[j] = nk[j] + 1
        
    mk = size/k
    c = 0
    for i in range(k):
        c += ((nk[i]-mk)**2)/mk
    return c

#计算随机数相关性
def covariance2(data, l=2):
    x = np.array(data[:-l])
    y = np.array(data[l:])
    d = np.array(data)

    rcl = (x*y).mean()
    r1 = (d.mean())**2 
    r2 = (d*d).mean()

    return (rcl - r1)/(r2 - r1)


if __name__ == "__main__":#开始执行
    s = seed_time()
    test = Schrage16807(s)
    localtime = time.asctime( time.localtime(time.time()) )
    print ("本地时间为 :", localtime)
    data = [test.rand() for i in range(10000001)] 
    data = np.array(data)#生成10e7个随机数，存入数组

    # 绘图，散点图
    x = data[0:10000]
    y = data[3:10003]
    plt.scatter(x,y, s=1, c='g')
    plt.title("plane distribution of 10000 points--interval=3")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    #检验均匀性（k阶矩），取不同N和k
    print("k阶矩检验均匀性:\n")
    error = []
    for k in range(3,7):
        for i in range(1,8):        
            xk = data[:int(10**i)]**k
            print("N:%.2e, k:%d, k%d阶矩:%.5f, 期望:%.5f" %(10**i, k,k, xk.mean(), 1/(k+1)))
            if k==6:
                error.append(abs(xk.mean()-1/(k+1)))
        print("\n")
    for i in range(7):
         print("N:%.2e, k:6, error:%.5f" %(10**i,error[i]))
    print("\n")

    #绘图--误差和N关系，验证中心极限率
    x = np.linspace(1,7,1001)
    y = error[0]*np.sqrt(10)/(np.sqrt(10**x))
    plt.plot(range(1,8),error,'o-',color = 'g',label="error")#误差
    plt.plot(x,y,'--',color='b',label=r'$O(\frac{1}{\sqrt{N}})$')#根号下n分之一
    plt.xlabel("lg(N)")
    plt.ylabel("error")
    plt.title("relation between N and error")
    plt.legend()
    plt.show()

    #检验均匀性(卡方分布)，取不同N，和不同区间数k
    print("卡方分布检验均匀性:\n")
    alpha = 0.05 #置信度0.95
    for i in range(4,8):
        for k in range(2,11):
            c2= uniformity(data[:int(10**i)],k)
            percent_point = chi2.ppf(1-alpha,k-1) 
            print("N:%.2e, k:%d, Statistics:%.5f, Percent_point:%.5f"%(10**i,k,c2,percent_point))
            
        print("\n")

    #检验关联性，取不同间隔l
    print("检验关联性:\n")
    for i in range(1,10):
        covar2 = covariance2(data=data,l=i)    
        print("l = %d, C(l) = %.10f"%(i,covar2))

    print("实验完毕")



