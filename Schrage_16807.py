import numpy as np
import time

def seed_time():#获取时间，作为种子
    t = time.localtime(time.time())
    localtime = time.asctime( t )
    return t.tm_year-2000 + 70*(t.tm_mon+12*(t.tm_mday+31*(t.tm_hour+23*(t.tm_min+59*t.tm_sec))))
class Schrage16807(object):#祖传生成器，一直用这个生成随机数
    def __init__(self,seed):
        self.seed = seed
        self.__M = 2147483647
        self.__a = 16807

    def __rand(self, i_n):#随机数迭代-iteration，取模
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
        self.seed = self.__rand(self.seed)
        return self.seed/self.__M
    
    def creat_array1(self,N):#输出一个长度为N的列表
        data = [self.rand1() for i in range(N)] 
        return data
    
    def rand2(self):#范围0-M
        self.seed = self.__rand(self.seed)
        return self.seed
    
    def creat_array2(self,N):#输出一个长度为N的列表
        data = [self.rand2() for i in range(N)] 
        return data

def creat_array_timeseed_0_1(M):
        seed=seed_time()
        t=Schrage16807(seed)
        return np.array(t.creat_array1(M))

def creat_array_timeseed_0_max(M):
        seed=seed_time()
        t=Schrage16807(seed)
        return np.array(t.creat_array2(M))
        
def creat_array_seed_0_1(seed,M):
        t=Schrage16807(seed)
        return np.array(t.creat_array1(M)),t.seed

def creat_array_seed_0_M(seed,M):
        t=Schrage16807(seed)
        return np.array(t.creat_array2(M)),t.seed

