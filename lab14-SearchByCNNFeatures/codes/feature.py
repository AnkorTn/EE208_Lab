# SJTU EE208

import time
import os
import sys
import numpy as np
import torch
from pathlib import Path
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader


# 导入ResNet50模型，并加载预训练参数，定义处理图片的归一化操作和预处理方式。
print('Load model: ResNet50')
model = torch.hub.load('pytorch/vision', 'resnet50', pretrained=True)
# 这里的model是resnet50模型
# print(model)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
trans = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize,
])

# 定义函数features()用来提取图像的特征。正常调用模型model(input_image)，
# 则会返回ResNet50模型在ImageNet数据集上的最终分类结果。
# 通常来讲，我们可以把模型最终分类的前一层当作模型学习到的图像特征，并用这种特征来完成我们的图像检索任务。
# 所以我们需要重新定义一个函数features()来提取模型倒数第二层的输出结果。
# 请同学们结合最开始print的模型信息思考函数features()为什么要这么写。如果换成其他的模型又该怎么完成features()这个函数。
'''
ResNet(
  (conv1): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
  (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (relu): ReLU(inplace=True)
  (maxpool): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
  (layer1): Sequential(...)
  (layer2): Sequential(...)
  (layer3): Sequential(...)
  (layer4): Sequential(...)
  (avgpool): AdaptiveAvgPool2d(output_size=(1, 1))
  (fc): Linear(in_features=2048, out_features=1000, bias=True)
)
'''
def features(x):
    x = model.conv1(x)
    x = model.bn1(x)
    x = model.relu(x)
    x = model.maxpool(x)
    x = model.layer1(x)
    x = model.layer2(x)
    x = model.layer3(x)
    x = model.layer4(x)
    x = model.avgpool(x)

    return x





# 读入图片，并使用之前定义好的处理方式(trans)处理图片，为送入模型提特征做准备。
print('Prepare image data!')
test_image = default_loader('103.jpg')
# 获取PIL图
input_image = trans(test_image)
input_image = torch.unsqueeze(input_image, 0)


print('Extract features!')
start = time.time()
# 提取图片的feature特征
image_feature = features(input_image)
# 并且利用numpy模式存储
image_feature = image_feature.detach().numpy()
print('Time for extracting features: {:.2f}'.format(time.time() - start))

# image_feature是待测图片的特征向量
print('Save features!')
# 存储特征
np.save('features.npy', image_feature)

def dist(feature1,feature2):
    # 需要归一化，否则容易过大
    dis, t1, t2 = 0, 0, 0
    for i in feature1[0]:
        t1 += i[0][0]**2
    t1 = t1**0.5
    feature11 = [i[0][0]*1.0/t1 for i in feature1[0]]
    for i in feature2[0]:
        t2 += i[0][0]**2
    t2 = t2**0.5
    feature22 = [i[0][0]*1.0/t2 for i in feature2[0]]
    for i in range(len(feature11)):
        dis += (feature11[i]-feature22[i])**2
    dis = dis**0.5
    return dis

def angle(feature1,feature2):
    # cosθ=
    # x·y=|x||y|cosθ
    cnt, t1, t2 = 0, 0, 0
    for i in feature1[0]:
        t1 += i[0][0]**2
    t1 = t1**0.5
    feature11 = [i[0][0] for i in feature1[0]]
    for i in feature2[0]:
        t2 += i[0][0]**2
    t2 = t2**0.5
    feature22 = [i[0][0]for i in feature2[0]]
    for i in range(len(feature22)):
        cnt += feature11[i]*feature22[i]
    cnt /= t1
    cnt /= t2
    return cnt


distance = []
# 调用函数去计算不同的欧氏距离情况比较
start = time.time()
for i in range(1,570):
    # try:
    filename = str(i) + '.jpg'
    print('Prepare image data:  '+ filename + "  !")
    # os.path.join('testpic',str(i) + '.jpg')
    # temp_image = default_loader("testpic\\%s.jpg"%i)
    # print(i)
    # 此处读入i.jpg的图片，然后进行与前面待匹配图像一样的操作，故可略
    temp_image = default_loader(os.path.join('testpic',filename))
    test_image = trans(temp_image)
    test_image = torch.unsqueeze(test_image, 0)

    # print('Extract features!')
    test_feature = features(test_image)
    test_feature = test_feature.detach().numpy()    

    # 欧氏距离内存下的为具体数值以及文件名
    # distance.append([dist(image_feature,test_feature),filename])
    # 角度下的为具体数值及文件名
    distance.append([angle(image_feature,test_feature),filename])
    # image_feature是待测图片的特征向量
    # print('Save features:  '+ filename + "  !")
    # np.save('testpic/'+str(i)+'features.npy', test_feature)
    # except Exception as e:
    #     print("Failed in indexDocs:", e)

print('Time for extracting features: {:.2f}'.format(time.time() - start))
# print(distance)

for i in range(len(distance)):
    for j in range(len(distance)):
        # 如果是角度 则为>，如果是dist， 则为<
        if(distance[i][0]>distance[j][0]):
            distance[i], distance[j] = distance[j], distance[i]
for i in range(5):
    print(distance[i])