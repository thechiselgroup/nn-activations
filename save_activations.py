import torch
import torchvision
from alexnet import alexnet

import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image



model = alexnet(pretrained=True)
model.eval() #so dropout is fixed
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

pre_transform=transforms.Compose([
    transforms.Scale(256),
    transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    normalize])

def extract_activatons(filename):
    temp = Image.open(filepath)
    im = temp.copy()
    temp.close()
    im = pretransform(im)
    #for greyscale images
    if im.size(0) == 1:
        images[i] = im.expand(3,224,224)
    in_ = Variable(im.unsqueeze(0))
    return model(in_)

if __name__ == "__main__":
    extract_activatons("bee.jpg")

