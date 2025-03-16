from Schrage_16807 import*
import matplotlib.pyplot as plt
def _int1(x):#蒙特卡洛积分I1
    integral1=lambda a:5*np.sqrt(a**2+2*np.sqrt(a))
    n=len(x)
    sum=0
    for i in range(n):
        sum+=integral1(5*x[i])
    return(sum/n)

def _int2(x,y,z,u,v):#蒙特卡洛积分I2
    integral2=lambda a,b,c,d,e:(5+a**2-b**2+3*a*b-c**2+d**3-e**3)*(7*4*9*2*13)/(10*7*10*11)
    n=len(x)
    sum=0
    for i in range(n):
        a=7*x[i]/10
        b=4*y[i]/7
        c=9*z[i]/10
        d=2*u[i]
        e=13*v[i]/11
        sum+=integral2(a,b,c,d,e)
    return sum/n

if __name__ == "__main__":
    print("本实验时间有一点点长，请稍等或直接退出。")
    average1=[]
    average2=[]
    sd1=[]
    sd2=[]
    l=5
    M=400
    axis_x=[]
    for j in range(0,8):#不同样本规模，研究精确度。
        N=(50*(j+3))**2
        s=seed_time()
        t=Schrage16807(s)
        T_seed=t.creat_arry2(M)#生成M种子，每个种子生成随机数
        I_1=[]
        I_2=[]    
        for i in range(M) :#相同N下算M次，统计样本方差
            r=Schrage16807(T_seed[i])
            x=r.creat_arry1(N+4*l)
            y=x[l:N+l]
            z=x[2*l:N+2*l]
            u=x[3*l:N+3*l]
            v=x[4*l:N+4*l]
            x=x[0:N]
            I_1.append(_int1(x))
            I_2.append(_int2(x,y,z,u,v))
        #标准差
        sd1.append(np.sqrt(np.var(I_1,ddof=1)))
        sd2.append(np.sqrt(np.var(I_2,ddof=1)))
        #均值，即积分结果
        average1.append(np.mean(I_1))
        average2.append(np.mean(I_2))
        print("N=%d,I1=%f,s-d=%f,I2=%f,s-d=%f \par"%(N,average1[j],sd1[j],average2[j],sd2[j]))
        axis_x.append(np.sqrt(N))
    #画图
    plt.plot(axis_x, sd1, color='deepskyblue', linestyle='-', marker='o', label='I_1')
    sd1_y=sd1[0]/np.array(axis_x)*axis_x[0]
    plt.plot(axis_x, sd1_y, color='hotpink', linestyle='-', marker='o', label='O(1/sqrt(N))')
    plt.title('The relation between I_1 error and N')
    plt.xlabel('sqrt(N)')
    plt.ylabel('Standard deviation')
    plt.legend()
    plt.show()
    plt.plot(axis_x, sd2, color='deepskyblue', linestyle='-', marker='o', label='I_2')
    sd2_y=sd2[0]/np.array(axis_x)*axis_x[0]
    plt.plot(axis_x, sd2_y, color='hotpink', linestyle='-', marker='o', label='O(1/sqrt(N))')
    plt.title('The relation between I_2 error and N')
    plt.xlabel('sqrt(N)')
    plt.ylabel('Standard deviation')
    plt.legend()
    plt.show()
