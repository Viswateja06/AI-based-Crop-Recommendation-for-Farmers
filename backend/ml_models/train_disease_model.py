import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from PIL import Image

# ---------------------------------------------------------
# PyTorch CNN Trainer for PlantVillage Dataset
# ---------------------------------------------------------

MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), 'plant_disease_model.pth')
CLASSES_SAVE_PATH = os.path.join(os.path.dirname(__file__), 'disease_classes.txt')
BATCH_SIZE = 32
EPOCHS = 1
LEARNING_RATE = 0.001

class PlantVillageKagglehub(torch.utils.data.Dataset):
    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform
        self.samples = []
        self.classes = []
        
        crops = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
        class_set = set()
        
        for crop in crops:
            crop_path = os.path.join(root, crop)
            # The structure is Crop -> Split -> Disease -> images
            for split in os.listdir(crop_path):
                split_path = os.path.join(crop_path, split)
                if not os.path.isdir(split_path): continue
                for disease in os.listdir(split_path):
                    disease_path = os.path.join(split_path, disease)
                    if not os.path.isdir(disease_path): continue
                    
                    class_name = f"{crop} {disease}"
                    class_set.add(class_name)
                    
        self.classes = sorted(list(class_set))
        class_to_idx = {c: i for i, c in enumerate(self.classes)}
        
        for crop in crops:
            crop_path = os.path.join(root, crop)
            for split in os.listdir(crop_path):
                split_path = os.path.join(crop_path, split)
                if not os.path.isdir(split_path): continue
                for disease in os.listdir(split_path):
                    disease_path = os.path.join(split_path, disease)
                    if not os.path.isdir(disease_path): continue
                    
                    class_idx = class_to_idx[f"{crop} {disease}"]
                    for filename in os.listdir(disease_path):
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                            self.samples.append((os.path.join(disease_path, filename), class_idx))
                            
    def __len__(self):
        return len(self.samples)
        
    def __getitem__(self, idx):
        path, target = self.samples[idx]
        img = Image.open(path).convert('RGB')
        if self.transform is not None:
            img = self.transform(img)
        return img, target

def train_model():
    print("Downloading/Locating dataset via kagglehub...")
    import kagglehub
    DATA_DIR = kagglehub.dataset_download('tushar5harma/plant-village-dataset-updated')
    print(f"Dataset downloaded/found at: {DATA_DIR}")

    data_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    print("Loading images into memory...")
    full_dataset = PlantVillageKagglehub(root=DATA_DIR, transform=data_transforms)
    class_names = full_dataset.classes
    
    with open(CLASSES_SAVE_PATH, 'w') as f:
        for c in class_names:
            f.write(c + '\n')
             
    num_classes = len(class_names)
    print(f"Loaded {len(full_dataset)} images across {num_classes} classes.")

    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    print("Initializing ResNet18...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Training on device: {device}")
    
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    # Use AdamW for better weight decay and an lr scheduler
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=1, verbose=True)

    EPOCHS = 5 # Increased epochs for better accuracy
    best_val_acc = 0.0

    print("Starting Training Loop...")
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for i, (inputs, labels) in enumerate(train_loader):
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
            
            if i % 50 == 0:
                print(f"Epoch {epoch+1} - Step [{i}/{len(train_loader)}] Train Loss: {loss.item():.4f}")
            
        train_acc = 100 * correct / total
        
        # Validation Loop
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += int((predicted == labels).sum())
                
        val_acc = 100 * val_correct / val_total
        print(f"Epoch [{epoch+1}/{EPOCHS}] - Train Acc: {train_acc:.2f}% - Val Loss: {val_loss/len(val_loader):.4f} - Val Acc: {val_acc:.2f}%")
        
        scheduler.step(val_acc)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"New best validation accuracy! Saving model weights...")
            torch.save(model.state_dict(), MODEL_SAVE_PATH)

    print(f"Training Complete. Best Validation Accuracy: {best_val_acc:.2f}%")

if __name__ == '__main__':
    train_model()
