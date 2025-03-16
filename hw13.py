# import matplotlib.pyplot as plt
from Schrage_16807 import*
from scipy.stats import gamma#避免手动算gamma分布

def func_q(x,g):
    return -1/g*np.exp(-x/g)

def q_sample(xi,g):
    return -g*np.log(1-xi)

def Metropolis_Hasting(g,func_p,seed,t):
    c=0
    x=np.zeros(t)
    x[0]=1
    for i in range(1,t):
        xi,seed=creat_array_seed_0_1(seed,1)
        x[i]=q_sample(xi,g)[0]
        a=func_p(x[i])*func_q(x[i-1],g)/(func_p(x[i-1])*func_q(x[i],g))
        alpha=min(1,a)
        xi,seed=creat_array_seed_0_1(seed,1)
        if xi>alpha:
             x[i]=x[i-1]
             c+=1
    return x,seed,(1-c/t)
alpha=2
beta=3
def p1(x):
    return gamma.pdf(x, alpha, scale=beta)

def p2(x):
    return gamma.pdf(x, alpha, scale=beta)*(x-alpha*beta)**2

# def draw_p1(x,g):
#     fig,ax=plt.subplots()
#     ax.hist(x[M:N], bins=100, alpha=0.9, color='hotpink',density=True )
#     ax.set_title('P1 Distribution(gamma=%d)'%g)
#     ax.set_xlabel('Value')
#     x1=np.linspace(0,40,100)
#     y1=p1(x1)
#     ax.plot(x1, y1, label="p1", color='blue', linestyle='--')
#     ax.legend()
#     plt.xlim(0, 40)
#     plt.show()

# def draw_p2(x,g):
#     fig,ax=plt.subplots()
#     ax.hist(x[M:N], bins=100, alpha=0.9, color='hotpink',density=True )
#     ax.set_title('P2 Distribution(gamma=%d)'%g)
#     ax.set_xlabel('Value')
#     x1=np.linspace(0,40,100)
#     y1=p2(x1)
#     ax.plot(x1, y1, label="p2", color='blue', linestyle='--')
#     ax.legend()
#     plt.xlim(0, 40)
#     plt.show()

if __name__ == '__main__': 
    seed=seed_time()
    N=10**4
    M=int(N*0.1)
    K=10
    I=np.zeros(K)
    accept=np.zeros(K)
    #p1：
    print("p1")
    for g in [2,3,4,5,6,7,8]:
        for j in range(K):
            x,seed,accept[j]=Metropolis_Hasting(g,p1,seed,N)
            for i in range(M,N):
                I[j]+=(x[i]-alpha*beta)**2
            I[j]=I[j]/(N-M)
        accept_rate=np.average(accept)
        I0=np.average(I)
        error=abs(I0-alpha*beta**2)/(alpha*beta**2)
        print("gamma:%d,accept_rate:%.3f,integral:%.3f,error:%.3f"%(g,accept_rate,I0,error))
    #p2:
    print("p2")    
    delta=0.4
    L=int(40/delta)
    x0=np.linspace(0,40,L)+delta/2
    pdf_p2=p2(x0)
    for g in range(5,15):
        for j in range(K):
            pdf=np.zeros(L)
            x,seed,accept[j]=Metropolis_Hasting(g,p2,seed,N)
            for i in range(M,N):
                p=int(x[i]//delta)
                if p>L-1:
                    p=L-1
                pdf[p]+=1/(N-M)/delta
            c=0
            I[j]=0
            for p in range(L):
                if pdf[p]>0.01:
                    c+=1
                    I[j]+=pdf_p2[p]/pdf[p]
            I[j]=I[j]/(c)
        accept_rate=np.average(accept)
        I0=np.average(I)
        error=abs(I0-alpha*beta**2)/(alpha*beta**2)
        print("gamma:%d,accept_rate:%.3f,integral:%.3f,error:%.3f,select:%.3f"%(g,accept_rate,I0,error,c/L))

        # N=10**5
        # g=6       
        # x,seed,accept[j]=Metropolis_Hasting(g,p1,seed,N)
        # draw_p1(x,g)
        # g=11
        # x,seed,accept[j]=Metropolis_Hasting(g,p2,seed,N)
        # draw_p2(x,g)