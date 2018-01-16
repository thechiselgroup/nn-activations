import torch
import torchvision
from alexnet import alexnet
import sys
import os

import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image

model = alexnet(pretrained=True)
model.eval() #so dropout is fixed
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

pre_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    normalize])

def extract_activations(filename):
    temp = Image.open(filename)
    print temp.format
    im = temp.copy()
    temp.close()
    im = pre_transform(im)
    #for greyscale images
    if im.size(0) == 1:
        images[i] = im.expand(3,224,224)
    in_ = Variable(im.unsqueeze(0))
    return model(in_)

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print "Usage: save_activations.py <image path> <destination path>"
        sys.exit(1)

    try:
        os.makedirs(sys.argv[2])
    except OSError:
        if not os.path.isdir(sys.argv[2]):
            raise

    extract_activations(sys.argv[1])

