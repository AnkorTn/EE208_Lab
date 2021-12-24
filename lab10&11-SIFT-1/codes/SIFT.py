import cv2
import math
from matplotlib import pyplot as plt
import numpy as np
import random
PI = math.pi
# 基本照搬实验8的梯度图代码，返回梯度值以及所获得的的角度angle
def gradient(img):
    Ix, Iy = np.zeros((len(img),len(img[0]))), np.zeros((len(img),len(img[0])))
    M, angle = np.zeros((len(img),len(img[0]))), np.zeros((len(img),len(img[0])))
    for i in range(1,len(img)-1):
        for j in range(1,len(img[0])-1):
            # Ix是x方向的梯度，Iy即y方向的
            Ix[i][j] = int(img[i+1][j])-int(img[i-1][j])
            Iy[i][j] = int(img[i][j+1])-int(img[i][j-1])
            # M为梯度强度
            M[i][j] = (Ix[i][j]**2+Iy[i][j]**2)**0.5
            angle[i][j] = np.arctan2(Ix[i][j],Iy[i][j])
    return M, angle

def sift(img):
    row, column = np.shape(img)
    
    # 计算角点，并且计算其长度
    corners, cnt = [], 0
    for i in cv2.goodFeaturesToTrack(img,300,0.01,10):
        corners.append([int(i[0][0]),int(i[0][1])])
        cnt += 1

    # 对其进行高斯模糊化处理
    # 高斯矩阵的长宽为5*5，标准差取1
    img = cv2.GaussianBlur(img, (5, 5), 1)

    # 获取梯度图、角图
    grad, angle = gradient(img)
    
    # 平均分成36个bins，每个像素以m(x, y)为权值为其所在的bin投票。
    # 最终权重最大的方向定位该关键点的主方向(实验中只考虑highest peak)。
    direction = []
    # 确定往不同方向拓展的最大尺度bins（最好满足能限制于36等分的区域内）
    # 适当大一些也无伤大雅
    bins = (row + column) // 80
    for corner in corners:
        # 获取角点坐标
        y, x = corner
        # 对每一个大块进行分块、计数
        # 实际上0这个维度基本是用不到的，因为我们有+1的操作
        ccnt = [0] * 37
        # 防止数组越界，通过max、min函数进行修饰
        for i in range(max(x-bins,0),min(x+bins+1,row)):
            for j in range(max(y-bins,0),min(y+bins+1,column)):
                # 梯度方向为360度
                # （注意atan函数返回值为0-180，需要根据Ix Iy的符号换算)
                weight = int((angle[i][j]+PI)*1.0/(PI/18)+1)
                # 超出边界则进行修正，由于限定在36以内所以乘上系数18再+1
                if(weight>36):
                    weight = 36
                # 分别计算每块区域的加权和，并且记录最大的那个加权和位置
                ccnt[weight] += grad[i][j]
        # 记录最大的加权和位置，并保存
        maxn = 1
        for i in range(36):
            if ccnt[i]>ccnt[maxn]:
                maxn = i
        # 注意需要将角度转化为弧度
        direction.append((maxn*1.0/18-1-1.0/36)*PI)
    # 以此获取最佳方向

    # 下面对描述子进行生成
    # SIFT描述子的统计在相对物体坐标系以关键点为中心的16×16的领域内
    # 统计，先把之前计算的梯度方向由图像坐标系换算到物体坐标系，即
    # θ’是相对物体坐标系的梯度方向， 
    # θ是相对图像坐标系的梯度方向， θ0是关键点的主方向。
    def Featurelize(point, θ):
        def θ_(x, y):
            if (x < 0 or x >= row) or (y < 0 or y >= column):
                return 0
            tmp = angle[x][y] - θ
            if tmp > 0:
                return tmp
            return tmp + 2 * PI
        
        # 物体坐标系上的每一个整数点对应的图像坐标系可能不是整数，
        # 可采用最邻近插值，即图像坐标系上和它最接近的一个点：
        # θ_(x',y')=θ_(int(x),int(y))
        # 或更精确地，可采用双线性插值：
        # 从而周围的四个点的值都对目标点有贡献，贡献大小与距离成正比。
        def Bilinear_Interpolation(x_1, y_1):
            # 首先找到x_1、y_1周围的最小整数点x,y并且以此为基础进行处理
            x, y = int(x_1), int(y_1)
            dx1, dy1 = x_1-x, y_1-y
            dx2, dy2 = 1-dx1, 1-dy1
            θθ = θ_(x,y)*dx2*dy2 + θ_(x+1,y)*dx1*dy2 + θ_(x,y+1)*dx2*dy1 + θ_(x+1,y+1)*dx1*dy1
            return θθ

        # 物体坐标系16*16的邻域分成4*4个块，每个块4*4个像素。
        # 在每个块内按照求主方向的方式把360度分成8个bins，统计梯度方向直方图，
        # 最终每个块可生成8维的直方图向量，每个关键点可生成4*4*8=128维的SIFT描述子。
        # 以特征点为中心，取领域内16*16大小的区域，
        # 并把这个区域分成4*4个大小为4*4的小区域，每个小区域内计算加权梯度直方图，
        # 该权值分为2部分，其一是该点的梯度大小，
        # 其二是改点离特征点的距离(二维高斯的关系)，每个小区域直方图分为8个bin，
        # 所以一个特征点的维数=4*4*8=128维。
        # 因此，根据SIFT算法详解的文章，应构造旋转变换的邻域
        # 即(x',y')^T=([cosθ,-sinθ],[sinθ,cosθ])(x,y)^T
        y0, x0 = point
        Horizon = np.array([np.cos(θ), np.sin(θ)])
        Vertical = np.array([-np.sin(θ),np.cos(θ)])
        # 并且统计其具体某个方向上（此时为8个方向）的梯度，再次计算

        def cnt(x1, x2, y1, y2, signx, signy):
            count = [0] * 9
            for x in range(x1, x2):
                for y in range(y1, y2):
                    # 找到具体的x,y（区分正负半轴）
                    dp = [x * signx, y * signy]
                    # 矩阵乘法，获得变换后的坐标
                    p = Horizon * dp[0] + Vertical * dp[1]
                    # 获取这个方向上的点理论上所在的方向（根据1~8进行划分）
                    weig = int((Bilinear_Interpolation(p[0]+x0, p[1]+y0))//(PI/4) + 1)
                    if weig > 8:
                        weig = 8
                    # 满足条件，计数
                    count[weig] += 1
            # 最后返回一个直方图数据，表示8个方向各个出现的次数，从而决定主方向
            return count[1:]

        vector = []
        # 确定往不同方向拓展的最大尺度bins（最好满足能限制于36等分的区域内）
        # 适当大一些也无伤大雅
        bins = (row + column) // 150
        # 最终每个块可生成8维的直方图向量，每个关键点可生成4*4*8=128维的SIFT描述子。
        # 记录16次的8维分布情况并返回
        for xsign in [-1,1]:
            for ysign in [-1,1]:
                vector += cnt(0, bins, 0, bins, xsign, ysign)
                vector += cnt(bins, bins*2, 0, bins, xsign, ysign)
                vector += cnt(bins, bins*2, bins, bins*2, xsign, ysign)
                vector += cnt(0, bins, bins, bins*2, xsign, ysign)
        return vector
    
    # 通过特征提取获取每个角点的主方向
    feature = []
    # print(cnt)
    for i in range(cnt):
        des = Featurelize(corners[i], direction[i])
        # 对该直方图向量进行归一化处理（即描述子）
        norm = sum(k * k for k in des) ** 0.5
        l = [k*1.0 / norm for k in des]
        # 最后对128维SIFT描述子f0归一化得到最终的结果：
        feature.append(l)
    # 因此两个SIFT描述子f1和f2之间的相似度可表示为:s(f1,f2)=f1*f2
    return feature, corners, cnt

def Merge(img1, img2):
    # 为小一点的图像补充空间，为大一点的图像适配小一点的图像的对等大小
    # 获取图片的性质，其中只有h是有意义的，其他在本处是无意义的
    h1, w1 ,a= np.shape(img1)
    h2, w2 ,a= np.shape(img2)
    # 图一规模较小则补全图一
    if h1 < h2:
        extra = np.array([[[0,0,0] for i in range(w1)] for ii in range(h2-h1)])
        img1 = np.vstack([img1, extra])
    # 图二规模较小则补全图二
    elif h1 > h2:
        extra = np.array([[[0,0,0] for i in range(w2)] for ii in range(h1-h2)])
        img2 = np.vstack([img2, extra])
    # 处理完毕之后自然是相同规模，可以直接水平方向拼接
    return np.hstack([img1,img2])

if __name__ == "__main__":

    # 首先进行目标图片以及待匹配图片的读取
    target0 = cv2.imread('data3.jpg')
    imgpkp0 = cv2.imread('dataset/5.jpg')
    # print(np.shape(target0))
    # 获取图片的大小等参数， 并且将目标图片进行适当的放大
    # r0, c0, a0=np.shape(target0)
    # times=1.0
    # 将目标图片放大至待匹配图片的等大小规模
    # resized_target0=cv2.resize(target0,(int(r0*times),int(c0*times)))
    # 灰度化处理图像
    target = cv2.cvtColor(target0, cv2.COLOR_BGR2GRAY)
    imgpkp = cv2.cvtColor(imgpkp0, cv2.COLOR_BGR2GRAY)

    # sift函数对图像进行处理，返回相似度的关系feature, 角点corners, 大小cnt
    feature_target, corners_target, cnt_target = sift(target)
    feature_img, corners_img, cnt_img = sift(imgpkp)

    # 这个是不同图片之间的位置向量，以此来对两点之间进行连线
    w = np.shape(target)[1]

    merge_graph = [Merge(target0, imgpkp0)]
    # merge_graph = [Merge(target0, imgpkp0)]
    # print("All Original Pics Processed!")
    
    # 开始进行匹配并划线
    x = []
    # 判断关键点的匹配数目
    # 如果超过6个则可视为一个合理匹配方式，否则不是
    cnt = 0
    for i in range(cnt_target):
        tmp = []
        for j in range(cnt_img):
            # 两个SIFT描述子f1和f2之间的相似度可表示为s(f1,f2)=f1·f2=inner(f1,f2)
            similar_rate = np.inner(np.array(feature_target[i]), np.array(feature_img[j]))
            tmp.append(similar_rate)
        x.append([tmp.index(max(tmp)), max(tmp)])
    # Traceback (most recent call last):
    #   File "SIFT.py", line 256, in <module>
    #     cv2.line(merge_graph[0], tuple(ct[a]), tuple([c[b][0] + w,c[b][1]]), color, 1)
    # TypeError: Expected Ptr<cv::UMat> for argument 'img'
    # 为了解决这个报错，需要利用转码改为uint8
    merge_graph[0] = np.array(merge_graph[0], dtype="uint8")
    for i in range(len(x)):
        j, rate = x[i]
        # 如果匹配率较低，说明这并不是我们想要的点
        if rate < 0.65:
            continue
        cnt += 1
        # 对于划线过程，进行颜色的随机设定
        color = ((random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
        # print("\n----------------")
        # print(corners_target[a])
        # print(corners_img[b])
        # print(merge_graph[0])
        cv2.line(merge_graph[0], tuple(corners_target[i]), tuple([corners_img[j][0] + w,corners_img[j][1]]), color, 1)
    cv2.imwrite("match5with%d.jpg"%cnt, merge_graph[0])