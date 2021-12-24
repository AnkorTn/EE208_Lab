import cv2
from matplotlib import pyplot as plt
filename = 'img1'
in_img = cv2.imread('images/'+filename+'.jpg')
# 灰度图
# cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
# 彩色图
# cv2.cvtColor(in_img, cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(in_img, cv2.COLOR_BGR2RGB)

# 记0
blue, green, red = 0, 0, 0
# 宽len(image),长len(image[0])
for i in range(0,len(image)):
    for j in range(0,len(image[0])):
        # 读入的图片按照r,g,b的顺序
        blue += image[i][j][2]
        green+= image[i][j][1]
        red  += image[i][j][0]
# 将最后的总量相加
tot = blue + green + red
# 将具体比例存入y向量中
y = [blue*1.0/tot, green*1.0/tot, red*1.0/tot]
# print(y)
# 画出柱状图，其中横坐标为b,g,r，纵坐标为b,g,r所占的比例
plot = plt.bar(x=['blue','green','red'],height=y,width=1.0,color=['b','g','r'])#color参数传入颜色列表，可以在一幅图中显示不同颜色
for rect in plot:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height,  '%f'%height, ha="center", va="bottom")
plt.title('Color image of '+filename)
# plt.hist(hist, bins=3)
# 保存图片
plt.savefig(filename+'.png')
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