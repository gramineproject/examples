from torchvision import models
import torch

output_filename = "alexnet-pretrained-model.pt"
alexnet = models.alexnet(weights=models.AlexNet_Weights.IMAGENET1K_V1)
torch.save(alexnet, output_filename)

print("Pre-trained model was saved in \"%s\"" % output_filename)
