import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
def lsm(x,y):#最小二乘法
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x * x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    n = len(x)
    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    numerator = np.sum((x - mean_x) * (y - mean_y))
    denominator = np.sqrt(np.sum((x - mean_x)**2)) * np.sqrt(np.sum((y - mean_y)**2))
    r = numerator / denominator
    b=mean_y-a*mean_x
    return a,b,r
def draw_picture(a,b):#画dla的图
    fig, ax = plt.subplots(1, 1)
    ax.imshow(a,cmap='Greys', interpolation='none')
    ax.axis('off')
    ax.set_title(b)
    ax.set_xlim([300, 700])
    ax.set_ylim([300, 700])
    filename = r'D:\physics\computational physics\homework\17\{}.png'.format(b)
    fig.savefig(filename, dpi=300)
def find_log_relation(x,y,name,N=8):#画对数图，找斜率
    l=len(x)
    a=np.log(x)
    b=np.log(y)
    record_g=[]
    record_r=[]
    record_b=[]
    for i in range(l-N+1):
        gradient,b_line,r=lsm(a[i:i+N],b[i:i+N])
        record_g.append(gradient)
        record_r.append(r)
        record_b.append(b_line)
    j=0
    for i in range(1,l-N+1):
        if abs(record_r[i])>abs(record_r[j]):
            j=i
    # 画图
    b_=record_g[j]*a[j:j+N]+record_b[j]
    fig, ax1 = plt.subplots(1, 1)
    ax1.plot(a,b, 'r--',marker='o',markersize=5) 
    ax1.plot(a[j:j+N],b_, ls='--',c='green',marker='o',markersize=3,label='liner part',alpha=0.8)   
    ax1.set_title('logarithmic graph {}'.format(name))  
    ax1.set_xlabel('log(x)') 
    ax1.set_ylabel('log(y)')  
    ax1.legend()
    filename = r'D:\physics\computational physics\homework\17\{}.png'.format(name)
    fig.savefig(filename, dpi=300)
    return record_g[j],abs(record_r[j])

def sand_box(array):
    l=len(array)
    center=int((l+1)/2)
    k=1
    list1=[]
    list2=[]
    while(1):
        length=int(1.5**k)
        if length>=l/2:
            break
        list1.append(length)
        count=0
        for i in range(center-length,center+length):
            for j in range(center-length,center+length):
                if array[i][j]==1:
                    count+=1
        list2.append(count)
        print("radius:%.0f,number:%.0f \\par"%(length,count))
        k+=1
    return list1,list2

def box_counting(array):
    l=len(array)
    k=1
    list1=[]
    list2=[]
    while(1):
        epsilon=int(1.5**k)
        if epsilon>=l:
            break
        num=math.ceil((l+1)/epsilon)
        grid=np.zeros((num,num))
        for i in range(l):
            for j in range(l):
                if array[i][j]==1:
                    a=math.ceil((i+1)/epsilon)-1
                    b=math.ceil((j+1)/epsilon)-1
                    grid[a][b]=1
        count=0
        for i in range(num):
            for j in range(num):
                if grid[i][j]==1:
                    count+=1
        print("length:%.0f,number:%.0f \\par"%(epsilon,count))
        list1.append(epsilon)
        list2.append(count)
        k+=1
    return np.array(list1),np.array(list2)
#从上个程序产生的文件中读取数据，存进数组
file_path = r'D:\physics\computational physics\homework\17\output-dla.csv'
df = pd.read_csv(file_path)
array = df.values

#盒子计数法
print('box count:\\par')
l1_box,l2_box=box_counting(array)
a_box,r_box=find_log_relation(l1_box,l2_box,'box_count')
print('fractal dimension:%.3f,pearson correlation coefficient:%.5f\\par'%(-a_box,r_box))
#sandbox法
print('sand box:\\par')
l1_sandbox,l2_sandbox=sand_box(array)
a_sandbox,r_sandbox=find_log_relation(l1_sandbox,l2_sandbox,'sand_box')
print('fractal dimension:%.3f,pearson correlation coefficient:%.5f'%(a_sandbox,r_sandbox))
#画图
draw_picture(array,"DLA")