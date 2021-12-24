# SJTU EE208

'''Train CIFAR-10 with PyTorch.'''
import os

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from models import resnet20

start_epoch = 0
end_epoch = 4
lr = 0.1

# Data pre-processing, DO NOT MODIFY

# PyTorch在做一般的深度学习图像处理任务时，先使用dataset类和dataloader类读入图片
# 在读入的时候需要做transform变换，其中transform一般都需要ToTensor()操作
# 将dataset类中__getitem__()方法内读入的PIL或CV的图像数据转换为torch.FloatTensor。
# Flip and Rotation 依概率p水平翻转
# Normalize归一化函数
print('==> Preparing data..')
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])


# 生成cifar10数据集
trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True)

testset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=False)


# 不同类型的图片
classes = ("airplane", "automobile", "bird", "cat",
           "deer", "dog", "frog", "horse", "ship", "truck")

# Model
print('==> Building model..')
# 生成ResNet20模型进行测试
model = resnet20()
# If you want to restore training (instead of training from beginning),
# you can continue training based on previously-saved models
# by uncommenting the following two lines.
# Do not forget to modify start_epoch and end_epoch.
# restore_model_path = 'pretrained/ckpt_4_acc_63.320000.pth'
# model.load_state_dict(torch.load(restore_model_path)['net'])

# A better method to calculate loss
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=lr, weight_decay=5e-4)

# Epoch：训练轮次。深度学习需要对training set遍历多遍，每一遍叫做一个训练轮次。
def train(epoch):
    # 训练模型
    model.train()
    train_loss = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(trainloader):
        # optimizer.zero_grad()：优化器进行初始化
        optimizer.zero_grad()
        # inputs是x，model是function，outputs是f(x)
        outputs = model(inputs)
        # The outputs are of size [128x10].
        # 128 is the number of images fed into the model 
        # (yes, we feed a certain number of images into the model at the same time, 
        # instead of one by one)
        # For each image, its output is of length 10.
        # Index i of the highest number suggests that the prediction is classes[i].
        # 损失（loss）：神经网络输出和目标之间的距离
        loss = criterion(outputs, targets)
        # 返回损失值
        loss.backward()
        # optimizer.step()：优化器的步长，更新你的情况 
        optimizer.step()
        # train_loss是每次测试的损失
        train_loss += loss.item()
        # 记录输出的最大值（最好的匹配结果）
        _, predicted = outputs.max(1)
        # 记录目标总数
        total += targets.size(0)
        # 记录目标正确匹配数
        correct += predicted.eq(targets).sum().item()
        with open('result.txt', 'a') as f:
            f.write('Epoch [%d] Batch [%d/%d] Loss: %.3f | Traininig Acc: %.3f%% (%d/%d)\n'% (epoch, batch_idx + 1, len(trainloader), train_loss / (batch_idx + 1), 100. * correct / total, correct, total))
            # print('Epoch [%d] Batch [%d/%d] Loss: %.3f | Traininig Acc: %.3f%% (%d/%d)'% (epoch, batch_idx + 1, len(trainloader), train_loss / (batch_idx + 1), 100. * correct / total, correct, total))


def test(epoch):
    print('==> Testing...')
    # 确保不能修改参数
    model.eval()
    with torch.no_grad():
        ##### TODO: calc the test accuracy #####
        # Hint: You do not have to update model parameters.
        #       Just get the outputs and count the correct predictions.
        #       You can turn to `train` function for help.
        train_loss = 0
        correct = 0
        total = 0
        for batch_idx, (inputs, targets) in enumerate(testloader):
            # optimizer.zero_grad()：优化器进行初始化
            optimizer.zero_grad()
            # inputs是x，model是function，outputs是f(x)
            outputs = model(inputs)
            # 损失（loss）：神经网络输出和目标之间的距离
            loss = criterion(outputs, targets)
            # train_loss是每次测试的损失
            train_loss += loss.item()
            # 记录输出的最大值（最好的匹配结果）
            _, predicted = outputs.max(1)
            # 记录目标总数
            total += targets.size(0)
            # 记录目标正确匹配数
            correct += predicted.eq(targets).sum().item()
            with open('result.txt', 'a') as f:
                f.write('TEST::Epoch [%d] Batch [%d/%d] Loss: %.3f | Traininig Acc: %.3f%% (%d/%d)\n'% (epoch, batch_idx + 1, len(testloader), train_loss / (batch_idx + 1), 100. * correct / total, correct, total))
                # print('TEST::Epoch [%d] Batch [%d/%d] Loss: %.3f | Traininig Acc: %.3f%% (%d/%d)'% (epoch, batch_idx + 1, len(testloader), train_loss / (batch_idx + 1), 100. * correct / total, correct, total))
        acc = 1.0 * correct / total
        ########################################
    # Save checkpoint.
    with open('result.txt', 'a') as f:
        f.write('Test Acc: %f\n' % acc)
        # print('Test Acc: %f' % acc)
    print('Saving..')
    # 训练集批次的状态记录
    state = {
        'net': model.state_dict(),
        'acc': acc,
        'epoch': epoch,
    }
    # 将其记录为一个成功的训练集model.pth
    if not os.path.isdir('checkpoint'):
        os.mkdir('checkpoint')
    torch.save(state, './checkpoint/ckpt_%d_acc_%f.pth' % (epoch, acc))

for epoch in range(start_epoch, end_epoch + 1):
    train(epoch)
    test(epoch)


start_epoch = 5
end_epoch = 9
lr = 0.01
optimizer = optim.SGD(model.parameters(), lr=lr, weight_decay=5e-4)
for epoch in range(start_epoch, end_epoch + 1):
    train(epoch)
    test(epoch)