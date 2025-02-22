# This PyTorch image classification example is based off
# https://www.learnopencv.com/pytorch-for-beginners-image-classification-using-pre-trained-models/

from torchvision import models
import torch

# Load the model from a file. This file needs to be obtained from a trusted
# source, because it can contain code, not only data.
# Note: For PyTorch 2.6 and later, direct unpickling with weights_only=True
# (which was made the default) can fail if the model file contains more than
# just the weights and includes classes or functions that are not allowlisted.
alexnet = torch.load("alexnet-pretrained.pt", weights_only=False)

# Prepare a transform to get the input image into a format (e.g., x,y dimensions) the classifier
# expects.
from torchvision import transforms
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)])

# Load the image.
from PIL import Image
img = Image.open("input.jpg")

# Apply the transform to the image.
img_t = transform(img)

# Magic (not sure what this does).
batch_t = torch.unsqueeze(img_t, 0)

# Prepare the model and run the classifier.
alexnet.eval()
out = alexnet(batch_t)

# Load the classes from disk.
with open('classes.txt') as f:
    classes = [line.strip() for line in f.readlines()]

# Sort the predictions.
_, indices = torch.sort(out, descending=True)

# Convert into percentages.
percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

# Print the 5 most likely predictions.
with open("result.txt", "w") as outfile:
    outfile.write(str([(classes[idx], percentage[idx].item()) for idx in indices[0][:5]]))

print("Done. The result was written to `result.txt`.")
