import cv2
from matplotlib import pyplot as plt
filename = 'img1'
in_img = cv2.imread('images/'+filename+'.jpg')
# 灰度图
# cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
# 彩色图
# cv2.cvtColor(in_img, cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)

# 创建0~255的灰度值像素点数
gray = [0]*256
tot  = 0
for i in range(0,len(image)):
    for j in range(0,len(image[0])):
        # 直接将image[i][j]点的灰度像素值加到我们的gray上
        gray[image[i][j]] += 1
        tot += 1
# 建立具体比例，存入y中
y = [i*1.0/tot for i in gray]
#print(y)
plt.bar(x=range(0,256,1),height=y,width=1)
#color参数传入颜色列表，可以在一幅图中显示不同颜色
# plot = plt.bar(x=range(0,256,1),height=y,width=0.2)#color参数传入颜色列表，可以在一幅图中显示不同颜色
# for rect in plot:
#     height = rect.get_height()
#     plt.text(rect.get_x() + rect.get_width() / 2, height,  '%f'%height, ha="center", va="bottom")
# plt.hist(hist, bins=3)
plt.title('Gray image of '+filename)
plt.savefig(filename+'gray.png')
plt.show()




# 如果只要求颜色分布的曲线（而不是柱状图），可参照以下代码
# color = ['blue','springgreen','red']
# for i in [0,1,2]:
#     hist = cv2.calcHist([image],[i], None, [256], [0.0,255.0])   #彩色图有三个通道，通道b:0,g:1,r:2
#     plt.plot(hist, color[i])
# plt.title('Histrogram of Color image')
# plt.savefig('chart.png')
# plt.show()





# print(len(image))
# print(len(image[0]))
# print(len(image[0][0]))
# 0<=x<len(image)
# 0<=y<len(image[0])
# Opencv2:
# B:0   G:1     R:2
# Simple graph:
# R:0   G:1     B:2