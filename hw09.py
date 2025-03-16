from Schrage_16807 import*
import matplotlib.pyplot as plt
import math
def exponent_distributuon(x):
    n=len(x)
    r=[]
    for i in range(n):
        r.append(-np.log(1-x[i]))
        print(r[i])
    return (np.mean(r)-1)*np.sqrt(n)

def poisson_distribution(x):
    E=np.exp(1)
    def sum_poisson(m):
        s=0
        if m==-1:
            return 0
        for i in range(m+1):
            s+=1/math.factorial(i)/E
        return s
    def find_indice(y):
         j=0
         while(1):
              if sum_poisson(j-1)<=y<sum_poisson(j):
                   return j
              j+=1     
    n=len(x)
    r=[]
    for i in range(n):
        r.append(find_indice(x[i]))
        print(r[i])
    return (np.mean(r)-1)*np.sqrt(n)

def equality_distribution(x):
    n=len(x)
    for i in range(n):
        print(x[i])
    return (np.mean(x)-1/2)*np.sqrt(12*n)
def two_point_distribution(x):
    P=0.7
    n=len(x)
    r=[]
    for i in range(n):
        if x[i]<=1-P:
            r.append(0)
        else:
            r.append(1)
        print(r[i])
    return (np.mean(r)-P)*np.sqrt(n/(P-P**2))

if __name__=="__main__":
    M=5000
    N=[2,5,10,50]
    #分别有：指数分布，泊松分布，均匀分布，两点分布。
    #代码很乱，是按照面向过程的逻辑来写的。为了减少变量个数，抽样和画图，在一个循环里，变量名被反复利用。
    #指数分布
    fig, ax = plt.subplots(2,2)
    for j in range(4):
        exponent=[]
        s=seed_time()
        t=Schrage16807(s)
        T_seed=t.creat_arry2(M)
        for i in range(M) :#相同N下算M次
                r=Schrage16807(T_seed[i])
                x=r.creat_arry1(N[j])
                exponent.append(exponent_distributuon(x))
        bin=np.linspace(-5,5,101)
        ax[j//2,j%2].hist(exponent, bins=bin, color='hotpink',density=True,label='Sample')
        ax[j//2,j%2].plot(bin,np.exp(-bin**2/2)/np.sqrt(np.pi*2),color='deepskyblue', linestyle='--',label='Gauss')
        # 添加图例
        ax[j//2,j%2].legend()

        # 设置标题
        ax[j//2,j%2].set_title("N=%d"%(N[j]))

        # 设置x轴和y轴标签
        ax[j//2,j%2].set_xlabel('Value')
        ax[j//2,j%2].set_ylabel('Frequency')

        # 显示图形
    fig.suptitle("exponent_distributuon")
    plt.tight_layout()
    plt.show()
    
    #泊松分布
    fig, ax = plt.subplots(2,2)
    for j in range(4):
        poisson=[]
        s=seed_time()
        t=Schrage16807(s)
        T_seed=t.creat_arry2(M)
        for i in range(M) :#相同N下算M次
                r=Schrage16807(T_seed[i])
                x=r.creat_arry1(N[j])
                poisson.append(poisson_distribution(x))
        bin=np.linspace(-5,5,41)
        bin2=np.linspace(-5,5,11)
        ax[j//2,j%2].hist(poisson, bins=bin, color='hotpink',density=True,label='Sample')
        ax[j//2,j%2].plot(bin,np.exp(-bin**2/2)/np.sqrt(np.pi*2),color='deepskyblue', linestyle='--',label='Gauss')
        # 添加图例
        ax[j//2,j%2].legend()

        # 设置标题
        ax[j//2,j%2].set_title("N=%d"%(N[j]))

        # 设置x轴和y轴标签
        ax[j//2,j%2].set_xlabel('Value')
        ax[j//2,j%2].set_ylabel('Frequency')

        # 显示图形
    fig.suptitle("poisson_distribution")
    plt.tight_layout()
    plt.show()

    #平均分布
    fig, ax = plt.subplots(2,2)
    for j in range(4):
        equality=[]
        s=seed_time()
        t=Schrage16807(s)
        T_seed=t.creat_arry2(M)
        for i in range(M) :#相同N下算M次
                r=Schrage16807(T_seed[i])
                x=r.creat_arry1(N[j])
                equality.append(equality_distribution(x))
        bin=np.linspace(-5,5,101)
        ax[j//2,j%2].hist(equality, bins=bin, color='hotpink',density=True,label='Sample')
        ax[j//2,j%2].plot(bin,np.exp(-bin**2/2)/np.sqrt(np.pi*2),color='deepskyblue', linestyle='--',label='Gauss')
        # 添加图例
        ax[j//2,j%2].legend()

        # 设置标题
        ax[j//2,j%2].set_title("N=%d"%(N[j]))

        # 设置x轴和y轴标签
        ax[j//2,j%2].set_xlabel('Value')
        ax[j//2,j%2].set_ylabel('Frequency')

        # 显示图形
    fig.suptitle("equality_distribution")
    plt.tight_layout()
    plt.show()

        #两点分布
    fig, ax = plt.subplots(2,2)
    for j in range(4):
        two_point=[]
        s=seed_time()
        t=Schrage16807(s)
        T_seed=t.creat_arry2(M)
        for i in range(M) :#相同N下算M次
                r=Schrage16807(T_seed[i])
                x=r.creat_arry1(N[j])
                two_point.append(two_point_distribution(x))
        bin=np.linspace(-5,5,101)
        bin2=np.linspace(-5,5,21)
        ax[j//2,j%2].hist(two_point, bins=bin2, color='hotpink',density=True,label='Sample')
        ax[j//2,j%2].plot(bin,np.exp(-bin**2/2)/np.sqrt(np.pi*2),color='deepskyblue', linestyle='--',label='Gauss')
        # 添加图例
        ax[j//2,j%2].legend()

        # 设置标题
        ax[j//2,j%2].set_title("N=%d"%(N[j]))

        # 设置x轴和y轴标签
        ax[j//2,j%2].set_xlabel('Value')
        ax[j//2,j%2].set_ylabel('Frequency')

        # 显示图形
    fig.suptitle("two_point_distribution")
    plt.tight_layout()
    plt.show()
