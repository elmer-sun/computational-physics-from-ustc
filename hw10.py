from Schrage_16807 import*
import matplotlib.pyplot as plt
import math
def v_next_100_t0(v,t,A,t_0=10**(-7)):#速度按照郎之万方程迭代
    def v_next(v,t,A):
        a=-v/tau+A+B*math.sin(w*t)
        v=v+a*t_0
        return v,t+t_0
    for i in range(100):
        v,t=v_next(v,t,A[i])
    return v,t
def self_correlation_function(v):
    scf=[]
    for i in range(N+1):
        scf.append(np.average(v[:,0]*v[:,i]))
    return scf
def test():#给出参数后即可自行生成随机数模拟布朗运动并画图
    v_0=V0*(2*creat_array_timeseed_0_1(M)-1)
    A_seed=creat_array_timeseed_0_max(M)
    v_array = np.zeros((M, N+1))
    for i in range(M):
         f=A_0*(2*creat_array_seed_0_1(A_seed[i],10000)-1)
         t=0
         v=v_0[i]
         v_array[i,0]=v
         for j in range(0,N):
             v,t=v_next_100_t0(v,t,f[100*j:100*(j+1)])
             v_array[i,j+1]=v
    scf=self_correlation_function(v_array)
    # print("自相关函数取值如下：")   
    # print(scf)
    print("v_0的平均值：")
    print(np.average(v_0))

    #画图
    fig, ax = plt.subplots()
    x=np.linspace(0,10**-3,N+1)
    ax.plot(x,scf,color='hotpink',ls='-',alpha=0.8,label='self-correlation-function')
    y=scf[0]*np.exp(-x/tau)
    ax.plot(x,y,color='dodgerblue',ls='--',alpha=0.8,label='theoretical prediction')
    ax.set_title('Brownian movement')
    ax.set_xlabel('t')
    ax.set_ylabel('C_vx')
    ax.legend()
    plt.show()

if __name__=="__main__":
    #测试M个粒子，每个粒子截取N个时间点的速度，w是电场振荡频率
    M=100
    N=100    
    w=10**(-5)   
    V0=10
    #A表示随机力大小，B表示电场强弱，tau和阻力有关

    #阻力较弱
    A_0=10**7
    B=10**8
    tau=10**(-5)
    test()
    #阻力很强
    A_0=10**7
    B=10**8
    tau=10**(-7)
    test()
