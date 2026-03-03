import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# ---------------------------------------------------------
# PyTorch CNN Trainer for PlantVillage Dataset
# ---------------------------------------------------------
# Note: You need to download the PlantVillage dataset from Kaggle
# and extract it into: data/PlantVillage/
# Structure should be:
# data/PlantVillage/Apple___Apple_scab/...
# data/PlantVillage/Apple___Black_rot/...
# ---------------------------------------------------------

DATA_DIR = '../data/PlantVillage'
MODEL_SAVE_PATH = 'plant_disease_model.pth'
BATCH_SIZE = 32
EPOCHS = 5
LEARNING_RATE = 0.001

def train_model():
    print("Checking for dataset...")
    if not os.path.exists(DATA_DIR):
        print(f"Error: Dataset not found at {DATA_DIR}.")
        print("Please download the PlantVillage dataset from Kaggle and extract it there.")
        return

    # 1. Define Image Transformations
    # PlantVillage images are 256x256, we resize them to 224x224 for ResNet
    data_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # 2. Load the Dataset
    print("Loading images into memory...")
    full_dataset = datasets.ImageFolder(root=DATA_DIR, transform=data_transforms)
    
    # Save the class names for inference later
    class_names = full_dataset.classes
    with open('disease_classes.txt', 'w') as f:
        for c in class_names:
            f.write(c + '\n')
            
    num_classes = len(class_names)
    print(f"Loaded {len(full_dataset)} images across {num_classes} classes.")

    # Split into train/val (80% / 20%)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    # 3. Define the CNN Architecture (ResNet-18)
    print("Initializing ResNet18...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Training on device: {device}")
    
    # Using a pretrained ResNet18 model and replacing the final layer
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    model = model.to(device)

    # 4. Loss Function and Optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 5. Training Loop
    print("Starting Training Loop...")
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += int((predicted == labels).sum())
            
        train_acc = 100 * correct / total
        print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {running_loss/len(train_loader):.4f} - Train Acc: {train_acc:.2f}%")

    # 6. Save Model
    print("Training Complete. Saving weights...")
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

if __name__ == '__main__':
    train_model()
