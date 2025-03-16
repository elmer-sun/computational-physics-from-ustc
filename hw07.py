from Schrage_16807 import*
import matplotlib.pyplot as plt

def read_file_to_arrays(file_path):
    array1 = []
    array2 = []
    
    with open(file_path, 'r') as file:
        file.readline()#第一行表头不读
        for line in file:
            # 移除行尾的换行符并分割每行的数据
            values = line.strip().split()
            if len(values) == 2:  # 确保每行有两个值
                array1.append(float(values[0]))  # 将第一个值转换为浮点数并添加到第一个数组
                array2.append(float(values[1]))  # 将第二个值转换为浮点数并添加到第二个数组
    
    return array1, array2

def sum_array(array,n):#离散版的求给出的累计函数
    a=[]
    for j in range(n):
        a.append(np.sum(array[0:j]))
    return a
    
def find_indice(x,b,n):#离散版的求解反函数，返回索引
    for i in range(n-1):
        if(b[i]<=x and b[i+1]>x):
            return i
    else:
            return n-1    
def direct_select(x_1,intensity,energy):#直接抽样，返回抽样结果
    r=[]
    intensity_accumulate=sum_array(intensity,len(intensity))
    for i in range(N):
        a=find_indice(x_1[i],intensity_accumulate,len(intensity_accumulate))
        r.append(energy[a])
    r=np.array(r)
    print(r)
    return r
def choose_select(x_1,y_1,intensity,energy):#舍选法抽样，返回抽样结果
    n=len(intensity)
    n_1=len(x_1)
    def F_x(x):#取比较函数
        if 0<x<2993:
            return p_1
        else:
            return p_2
    p_1_normalized=p_1/(p_1*93+p_2*20)   
    p_2_normalized=p_2/(p_1*93+p_2*20) 
    ant_1=lambda x: x/p_1_normalized+2900
    ant_2=lambda x: (x-p_1_normalized*93)/p_2_normalized+2993
    x_1_=[]#直接抽样，满足比较函数分布，范围在(2900,3013)
    for i in range(n_1):
        if x_1[i]<=93*p_1_normalized:
            x_1_.append(ant_1(x_1[i]))
        else:
            x_1_.append(ant_2(x_1[i]))
    x_left=[]#剩下的
    counter=0
    for i in range(n_1):
        a=int((x_1_[i]-2900)//1)
        if F_x(x_1_[i])*y_1[i]<intensity[a]:
            x_left.append(x_1_[i])
            counter+=1
    print(x_left)
    print("sample rate=%.3f"%(counter/n_1 ))
    return x_left





if __name__=="__main__":
    #从txt读数
    file_path = file_path = r'D:\physics\computational physics\homework\7\data.txt'  
    energy, intensity = read_file_to_arrays(file_path)
    intensity=np.array(intensity)
    sum_n = np.sum(intensity)#归一化
    intensity = intensity/sum_n
    #生成随机数
    N=10**6
    l=5
    s=seed_time()
    r=Schrage16807(s)
    x_1=r.creat_arry(N+l)
    y_1=x_1[l:N+l]
    x_1=x_1[0:N]
    #
    #直接抽样与舍选
    r_d=direct_select(x_1,intensity,energy)
    p_1=np.max(intensity[0:94])
    p_2=np.max(intensity[94:len(intensity)])
    r_s=choose_select(x_1,y_1,intensity,energy)
    #绘制直方图与概率密度分布图像

    #绘制直接抽样法得到的图像
    fig, ax = plt.subplots()
    #直方图
    num_bins=len(intensity)-1
    ax.hist(r_d, num_bins, density=True, color='hotpink',label='Direct sampling data')
    #已知分布
    ax.plot(energy, intensity, '--',color='black', label="Best fit")
    ax.set_xlabel('Energy(eV)')
    ax.set_ylabel('Probability density')
    ax.legend()
    fig.tight_layout()
    plt.figure(1)
    #绘制舍选法得到的图像

    fig, ax = plt.subplots()

    #直方图
    n, bins, patches = ax.hist(r_s, num_bins, density=True, color='hotpink',label='Selection sampling data')

    #已知分布
    ax.plot(energy, intensity, '--',color='black', label="Best fit")
    x_plot=[2900,2993,2993,3013,3014]
    y_plot=[p_1,p_1,p_2,p_2,0]
    ax.plot(x_plot, y_plot, '--',color='turquoise', label="Compare")
    ax.set_xlabel('Energy(eV)')
    ax.set_ylabel('Probability density')
    ax.legend()
    fig.tight_layout()
    plt.figure(2)
    plt.show()







    
    
