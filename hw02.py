import numpy as np
import time
#16807产生器，沿用作业1的代码
class Schrage16807(object):
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
#Fibonacci延迟产生器
class LaggedFibonacci(object):
    def __init__(self,seed):
        self.__seed = seed
    def __make_number43(self):#使用16807随机生成前43个数
        q=[]
        s = self.__seed
        test = Schrage16807(s)
        for j in range(44):  
            q.append(test.rand1()) 
        return q
    def rand2(self,N):#使用前43个数生成包含N个随机数的列表
        data2=self.__make_number43()
        for j in range(43,N):
            I_n=data2[j-22]-data2[j-43]
            if I_n<0:
                I_n+=2**32-6
            data2.append(I_n)
        return data2
 

def decision(list):#判断是否满足大小关系的计数器
    if list[0]>list[2] and list[2]>list[1]:
        return 1
    else:
        return 0
    
def seed_time():#获取时间，作为种子
    t = time.localtime(time.time())
    localtime = time.asctime( t )
    print ("localtime :", localtime,"\par")
    return t.tm_year-2000 + 70*(t.tm_mon+12*(t.tm_mday+31*(t.tm_hour+23*(t.tm_min+59*t.tm_sec))))
        
if __name__ == "__main__":
    N = 10**6#数组个数N-1
    max=10#循环次数
    #记录每次的占比
    per_16807=[0]*max
    per_fib=[0]*max
    for i in range(max):
        s = seed_time()
        test1 = Schrage16807(s)
        data1 = [test1.rand1() for i in range(N)] 
        data1 = np.array(data1)
        test2 = LaggedFibonacci(s)
        data2 = test2.rand2(N)
        data2=np.array(data2)#注意到并未对data2归一化，因为只需要比大小
        N_16807 = 0
        N_fib = 0
        for j in range(1,N-1):
            N_16807 += decision(data1[j-1:j+2])
            N_fib += decision(data2[j-1:j+2])        
        per_16807[i] = N_16807/(N-2)
        per_fib[i] = N_fib/(N-2)
        print("Seed = %d, Schrage 16807: %.6f, Fibonacci: %.6f\par" %( s, per_16807[i], per_fib[i]))
        #\par为了在latex中更方便写
        time.sleep(2)
    per_16807=np.array(per_16807)
    per_fib=np.array(per_fib)
    print("Averarge of Schrage 16807 : %.6f, Average of Fibonacci: %.6f\par" %( per_16807.mean(), per_fib.mean()))



