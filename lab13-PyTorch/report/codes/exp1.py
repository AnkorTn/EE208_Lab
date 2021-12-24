# SJTU EE208

'''Fit a curve with PyTorch.'''
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import torch

from models import Naive_NN

# 点集数目
NUM_TRAIN_SAMPLES = 200
# 训练轮次
NUM_TRAIN_EPOCHS = 3500  # try: 100, 1000, 10000, 50000
# 学习率（LR）
LEARNING_RATE = 0.001

# 在神经网络中，参数默认是进行随机初始化的。
# 不同的初始化参数往往会导致不同的结果，当得到比较好的结果时我们通常希望这个结果是可以复现的
# 在pytorch中，通过设置随机数种子也可以达到这么目的。
# torch.manual_seed(2019)
torch.manual_seed(208)


# 计算具体函数值
def f(x):
    """Actual function (ground truth)."""
    return x**2 + x + 1 + np.sin(x**2+1) - np.log(x**2+1)
    # return x**2 + 2 * np.sin(x) + np.cos(x - 1) - 5

# Create dataset


class MyDataset(torch.utils.data.Dataset):
    def __init__(self):
        super(MyDataset, self).__init__()
        self.x, self.y = self.generate_data(NUM_TRAIN_SAMPLES)

    # 随意读入一个Batch的数据，将其输入模型得到预测数据
    def generate_data(self, num):
        # Generate num training data disturbed by noise.
        x = (torch.rand([num, 1]) - 0.5) * 10.0
        y_noise = f(x) + torch.randn([num, 1]) * 3
        return x, y_noise

    # 获取全部数据
    def get_all_data(self):
        return self.x.detach(), self.y.detach()

    # 获取长度
    def __len__(self):
        return NUM_TRAIN_SAMPLES

    # 获取具体下标的具体数值
    def __getitem__(self, index):
        return self.x[index], self.y[index]

# 创建朴素贝叶斯模型
model = Naive_NN()
# 创建数据集
dataset = MyDataset()
# 导入数据，确定batch的大小
dataloader = torch.utils.data.DataLoader(dataset, batch_size=200, shuffle=True)
# 为了使用torch.optim，需先构造一个优化器对象Optimizer，用来保存当前的状态，并能够根据计算得到的梯度来更新参数。
# 你必须给它一个可进行迭代优化的包含了所有参数（所有的参数必须是变量s）的列表。
# 然后，您可以指定程序优化特定的选项，例如学习速率，权重衰减等。
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# train
model.train()
for epoch in range(NUM_TRAIN_EPOCHS):
    # 计算损失函数
    loss_avg = []
    for x, target_y in dataloader:
        # Reset gradients
        model.zero_grad()
        # Forward pass
        predicted_y = model(x)
        # Calc loss (mean squared error)
        mse = (predicted_y - target_y)**2
        # 返回误差的平均值作为loss
        loss = torch.mean(mse)
        # Backward pass (determine the weights' updating direction)
        loss.backward()
        # Apply weight updating with certain learning rate
        optimizer.step()
        # Monitor loss
        loss_avg.append(torch.sum(mse).detach())
    # print('Epoch [%d/%d], Loss=%f' %
    #       (epoch + 1, NUM_TRAIN_EPOCHS, sum(loss_avg) / len(dataset)))

# save model
torch.save(model.state_dict(), 'model.pth')

# test curve
# 训练完train_datasets之后，model要来测试样本了。在model(test_datasets)之前，需要加上model.eval(). 
# 否则的话，有输入数据，即使不训练，它也会改变权值。这是model中含有batch normalization层所带来的的性质。
model.eval()
# torch.no_grad() 是一个上下文管理器，被该语句 wrap 起来的部分将不会track 梯度。
with torch.no_grad():
    x = torch.linspace(-5, 5, 50).reshape([50, 1])
    y = model(x)
    plt.plot(x, y, color='y', label='learnt curve')  # learnt curve
    plt.plot(x, f(x), color='r', label='ground-truth curve')  # ground-truth curve
    plt.scatter(*(dataset.get_all_data()), label='training set')  # training set
    # plt.legend( )函数，给图像加上图例。
    plt.legend()

    plt.savefig('Self.png')

    plt.show()