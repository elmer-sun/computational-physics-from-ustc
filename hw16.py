import numpy as np
import matplotlib.pyplot as plt

# 迭代函数
def iterate(x, lambda_val):
    return lambda_val * np.sin(np.pi * x)

# 寻找稳定状态
def find_stable_states(lambda_val, initial=0.5, M=5000, N=1000,lim=1e-5):
    stable_states = []
    x=initial
    for _ in range(M):
        x = iterate(x, lambda_val)
    stable_states.append(x)
    for _ in range(1,N):
        x = iterate(x, lambda_val)
        a=1
        for j in range(len(stable_states)):
            if abs(x-stable_states[j])<lim:
                a=0
        if a==1:
            stable_states.append(x)
    return stable_states
#寻找分叉处λ值
def find_convert_point(lambda_list,stable_list,l):
    def compare(a,b):
        if abs(a-b)<(a+b)*0.005:
            return 0
        else:
            return 1
    result=[]
    a=len(lambda_list)
    for i in l:
        for j in range(1,a):
            if stable_list[j-1]==i and stable_list[j]==i and stable_list[j+1]!=i and stable_list[j+2]!=i :
                k=j+1
                while(compare(stable_list[k],2*i)):
                    k+=1
                x=(lambda_list[j]+lambda_list[k])/2
                result.append(x)
                break
    return result
#计算Feigenbaum 常数
def Feigenbaum(x):
    y=[]
    l=len(x)
    for i in range(2,l):
        a=(x[i-1]-x[i-2])/(x[i]-x[i-1])
        y.append(a)
    return y

if __name__=='__main__':
    # 参数范围和初始条件
    lambda_vals = np.linspace(0, 1, 1001)
    #lambda变化经历定值状态、倍周期分叉和混沌状态，步长0.001
    #找1，2，4
    l=[1,2]
    lambda_convert=[]
    all_stable_states = {}
    with open(r"D:\physics\computational physics\homework\16\output.txt", 'w') as f:
        for lambda_val in lambda_vals:
            v= find_stable_states(lambda_val)
            all_stable_states[lambda_val] = v
            print("lambda={:.3f}, period={}".format(lambda_val, len(v)))
            print("lambda={:.3f}, period={}".format(lambda_val, len(v)),end='\n', file=f)
    lambda_list = list(all_stable_states.keys())
    stable_list = list(all_stable_states.values())
    stable_list = [len(sublist) for sublist in stable_list]
    lambda_convert=lambda_convert+find_convert_point(lambda_list,stable_list,l)

    # #画图
    # x=[]
    # y=[]
    # for key,value in all_stable_states.items():
    #     for i in range(len(value)):
    #         x.append(key)
    #         y.append(value[i])
    # plt.scatter(x, y, color='black', s=0.1)
    # plt.xlabel('lambda ')
    # plt.ylabel('stable points')
    # plt.show()


    lambda_vals2 = np.linspace(0.858, 0.859, 101)
    lambda_vals3 = np.linspace(0.864, 0.866, 201)
    lambda_vals4 = np.linspace(0.86556, 0.86558,21)
    with open(r"D:\physics\computational physics\homework\16\output.txt", 'a') as f:

        #找4，8
        all_stable_states = {}
        l=[4]
        for lambda_val in lambda_vals2:
            v= find_stable_states(lambda_val,M=10000, N=2000,lim=2e-6)
            all_stable_states[lambda_val] = v
            print("lambda={:.5f}, period={}".format(lambda_val, len(v)))
            print("lambda={:.5f}, period={}".format(lambda_val, len(v)),end='\n', file=f)
        lambda_list = list(all_stable_states.keys())
        stable_list = list(all_stable_states.values())
        stable_list = [len(sublist) for sublist in stable_list]
        lambda_convert=lambda_convert+find_convert_point(lambda_list,stable_list,l)

        #找8，16，32，64
        all_stable_states = {}
        l=[8,16,32]
        for lambda_val in lambda_vals3:
            v= find_stable_states(lambda_val,M=10000, N=2000,lim=2e-6)
            all_stable_states[lambda_val] = v
            print("lambda={:.5f}, period={}".format(lambda_val, len(v)))
            print("lambda={:.5f}, period={}".format(lambda_val, len(v)),end='\n', file=f)
        lambda_list = list(all_stable_states.keys())
        stable_list = list(all_stable_states.values())
        stable_list = [len(sublist) for sublist in stable_list]
        lambda_convert=lambda_convert+find_convert_point(lambda_list,stable_list,l)

        #64，128，256，512
        all_stable_states = {}
        l=[64,128,256]
        for lambda_val in lambda_vals4:
            v= find_stable_states(lambda_val,M=10000, N=2000,lim=1e-7)
            all_stable_states[lambda_val] = v
            print("lambda={:.7f}, period={}".format(lambda_val, len(v)))
            print("lambda={:.7f}, period={}".format(lambda_val, len(v)),end='\n', file=f)
        lambda_list = list(all_stable_states.keys())
        stable_list = list(all_stable_states.values())
        stable_list = [len(sublist) for sublist in stable_list]
        lambda_convert=lambda_convert+find_convert_point(lambda_list,stable_list,l)
        print(lambda_convert,end='\n', file=f)
    Feigenbaum_c=Feigenbaum(lambda_convert)
    for i in range(len(lambda_convert)):
        print(" from {} to {}:lambda={:.7f}\\par".format(2**(i),2**(i+1),lambda_convert[i]))
    for i in range(len(Feigenbaum_c)):
        print(" Feigenbaum={:.3f}\\par".format(Feigenbaum_c[i]))
    print(" Feigenbaum-average={:.3f}".format(np.mean(Feigenbaum_c)))