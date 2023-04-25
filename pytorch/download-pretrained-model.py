# SPDX-License-Identifier: LGPL-3.0-or-later

from torchvision import models
import torch

output_filename = "alexnet-pretrained.pt"

try:
    alexnet = models.alexnet(weights=models.AlexNet_Weights.IMAGENET1K_V1)
except AttributeError:
    # older versions of torchvision (less than 0.13.0) use below now-deprecated parameter
    alexnet = models.alexnet(pretrained=True)

torch.save(alexnet, output_filename)

print("Pre-trained model was saved in \"%s\"" % output_filename)
