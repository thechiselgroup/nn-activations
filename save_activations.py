import torch
import torchvision
from alexnet import alexnet

import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image

import os
import cPickle as pickle

import sys

model = alexnet(pretrained=True)
model.eval() #so dropout is fixed
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

pre_transform=transforms.Compose([
    transforms.Scale(256),
    transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    normalize])

images = []
paths  = []
directory = '.'
save_destination = 'activations'

for filename in os.listdir(directory):
    filepath = os.path.join(directory,filename)
    if filename.endswith(".jpg"):
        print 'reading image', filepath
        temp = Image.open(filepath)
        im = temp.copy()
        temp.close()
        images.append(im)
        paths.append(filepath)


print "TOTAL NUMBER OF IMAGES LOADED:", len(images)

#normalization and preprocessing
images = map(pre_transform,images)

#check for greyscale images
for i, im in enumerate(images):
    if im.size(0) == 1:
        images[i] = im.expand(3,224,224)

#mega_batch = torch.zeros((len(images),3,224,224))
#for i, im in enumerate(images):
#    mega_batch[i] = im
#mega_batch = Variable(mega_batch)
print "FINSHED LOADING IMAGES."

def layer_name(l):
    name = str(l)
    index = name.index('(')
    return name[:index].strip()

for i, input in enumerate(images):
    in_ = Variable(input.unsqueeze(0)) 
    print "evalutating:", paths[i]
    out = model(in_)

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





