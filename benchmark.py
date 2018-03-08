import time
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torchvision.models as models
from torch.autograd import Variable

class MobileNet(nn.Module):
    def __init__(self):
        super(MobileNet, self).__init__()

        def conv_bn(inp, oup, stride):
            return nn.Sequential(
                nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True)
            )

        def conv_dw(inp, oup, stride):
            return nn.Sequential(
                nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
                nn.BatchNorm2d(inp),
                nn.ReLU(inplace=True),
    
                nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True),
            )

        self.model = nn.Sequential(
            conv_bn(  3,  32, 2), 
            conv_dw( 32,  64, 1),
            conv_dw( 64, 128, 2),
            conv_dw(128, 128, 1),
            conv_dw(128, 256, 2),
            conv_dw(256, 256, 1),
            conv_dw(256, 512, 2),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 1024, 2),
            conv_dw(1024, 1024, 1),
            nn.AvgPool2d(7),
        )
        self.fc = nn.Linear(1024, 1000)

    def forward(self, x):
        x = self.model(x)
        x = x.view(-1, 1024)
        x = self.fc(x)
        return x

def speed(model, name, use_gpu=True):
    t0 = time.time()
    if use_gpu:
        input = torch.rand(1,3,224,224).cuda()
        input = Variable(input, volatile = True)
    else:
        input = torch.rand(1,3,224,224)
        input = Variable(input, volatile = True)
    t1 = time.time()

    model(input)
    t2 = time.time()

    model(input)
    t3 = time.time()
    
    print('%10s : %f' % (name, t3 - t2))

if __name__ == '__main__':
    #cudnn.benchmark = True # This will make network slow ??
    print("usding gpu")
    if torch.cuda.is_available():
        resnet18 = models.resnet18().cuda()
        alexnet = models.alexnet().cuda()
        vgg16 = models.vgg16().cuda()
        squeezenet = models.squeezenet1_0().cuda()
        mobilenet = MobileNet().cuda()

        speed(resnet18, 'resnet18', use_gpu=True)
        speed(alexnet, 'alexnet', use_gpu=True)
        speed(vgg16, 'vgg16', use_gpu=True)
        speed(squeezenet, 'squeezenet', use_gpu=True)
        speed(mobilenet, 'mobilenet', use_gpu=True)
    print("usding cpu")
    resnet18 = models.resnet18()
    alexnet = models.alexnet()
    vgg16 = models.vgg16()
    squeezenet = models.squeezenet1_0()
    mobilenet = MobileNet()

    speed(resnet18, 'resnet18', use_gpu=False)
    speed(alexnet, 'alexnet', use_gpu=False)
    speed(vgg16, 'vgg16', use_gpu=False)
    speed(squeezenet, 'squeezenet', use_gpu=False)
    speed(mobilenet, 'mobilenet', use_gpu=False)

