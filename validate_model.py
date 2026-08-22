import os
import sys
import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

def run_model_validation():
    print("==========================================================================")
    print("=== DERMAVISION PRODUCTION MODEL VALIDATION SCRIPT (validate_model.py) ===")
    print("==========================================================================")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    
    # 1. Load class mapping
    mapping_path = r"c:\Users\yoges\Downloads\techno\class_mapping.json"
    if not os.path.exists(mapping_path):
        mapping_path = r"c:\Users\yoges\Downloads\techno\backend\class_mapping.json"
        
    print(f"Class Mapping File: {mapping_path}")
    with open(mapping_path, "r", encoding="utf-8") as f:
        raw_map = json.load(f)
        
    idx_to_class = {}
    for k, v in raw_map.items():
        idx = int(k)
        if isinstance(v, dict):
            idx_to_class[idx] = v.get("exact_disease_name", v.get("technical_class", f"Class_{idx}"))
        else:
            idx_to_class[idx] = str(v)
            
    num_classes = len(idx_to_class)
    print(f"Total Model Classes: {num_classes}")

    # 2. Load Checkpoint
    model_path = r"c:\Users\yoges\Downloads\techno\backend\trained_skin_model.pth"
    if not os.path.exists(model_path):
        model_path = r"c:\Users\yoges\Downloads\techno\trained_skin_model.pth"
        
    print(f"Model File Path: {model_path}")
    checkpoint = torch.load(model_path, map_location=device)
    sd = checkpoint.get("model_state_dict", checkpoint) if isinstance(checkpoint, dict) else checkpoint
    
    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    
    out_f = sd["classifier.5.weight"].shape[0]
    mid_f = sd["classifier.1.weight"].shape[0]
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, mid_f),
        nn.ReLU(),
        nn.BatchNorm1d(mid_f),
        nn.Dropout(p=0.2),
        nn.Linear(mid_f, out_f)
    )
    
    model.load_state_dict(sd)
    model.to(device)
    model.eval()

    # 3. Image Preprocessing
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # 4. Evaluate Labeled Sample Test Set
    sample_dir = r"c:\Users\yoges\Downloads\techno\sample_test_images"
    test_files = []
    
    if os.path.exists(sample_dir):
        for root, dirs, files in os.walk(sample_dir):
            for file in files:
                if file.lower().endswith((".jpg", ".png", ".jpeg")):
                    folder_name = os.path.basename(root)
                    test_files.append((os.path.join(root, file), folder_name))

    print(f"\nTotal Test Images Evaluated: {len(test_files)}")
    
    healthy_false_positives = []
    disease_predictions = []
    
    for img_path, folder in test_files:
        pil_img = Image.open(img_path).convert("RGB")
        tensor_img = transform(pil_img).unsqueeze(0).to(device)
        
        with torch.no_grad():
            logits = model(tensor_img)
            probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
            
        top_idx = int(probs.argmax())
        top_class = idx_to_class[top_idx]
        top_conf = float(probs[top_idx]) * 100.0
        
        is_normal = "normal" in top_class.lower() or "healthy" in top_class.lower()
        is_diseased_folder = folder.lower() not in ["benign_other", "normal", "healthy"]
        
        if is_diseased_folder and is_normal:
            healthy_false_positives.append((os.path.basename(img_path), folder, top_class, top_conf))
            
        disease_predictions.append({
            "folder": folder,
            "filename": os.path.basename(img_path),
            "predicted_class": top_class,
            "confidence_pct": round(top_conf, 2)
        })

    print("\n--- MODEL VALIDATION SUMMARY ---")
    print(f"Total Evaluated Test Images : {len(test_files)}")
    print(f"Diseased -> Normal False Positives (Raw Neural Output): {len(healthy_false_positives)}")
    
    if healthy_false_positives:
        print("\n[WARNING] Found Raw Neural Model Misclassifications:")
        for fname, folder, pred_c, conf in healthy_false_positives:
            print(f"  File: {fname} | Expected Folder: {folder} | Model Predicted: {pred_c} ({conf:.2f}%)")
    else:
        print("\n[SUCCESS] ZERO diseased images were misclassified as Normal/Healthy Skin by the raw neural model!")

    print("\n==========================================================================")
    print("=== MODEL VALIDATION COMPLETE ===")
    print("==========================================================================")

if __name__ == '__main__':
    run_model_validation()
