#!/usr/bin/env python3
import os
import json
from google.cloud import vision
from collections import defaultdict

# 初始化Vision API客户端
client = vision.ImageAnnotatorClient()

folder = "/Users/wyl/Documents/GitHub/VOYAGEUR-Stickers"
results = {}

# 获取所有PNG文件并按数字排序
files = sorted([f for f in os.listdir(folder) if f.endswith(".png") and f.startswith("sticker")],
              key=lambda x: int(x.replace("sticker", "").replace(".png", "")))

print(f"开始分析 {len(files)} 张贴纸...")
print("=" * 60)

# 分析每张图片
for i, file in enumerate(files, 1):
    path = os.path.join(folder, file)

    try:
        with open(path, "rb") as img:
            content = img.read()

        image = vision.Image(content=content)
        response = client.label_detection(image=image)

        # 获取前5个标签
        labels = [label.description for label in response.label_annotations[:5]]
        results[file] = labels

        # 显示进度
        if i % 10 == 0:
            print(f"已处理: {i}/{len(files)}")

    except Exception as e:
        print(f"处理 {file} 出错: {e}")
        results[file] = []

print("=" * 60)
print("\n分析完成！正在分类...")

# 根据标签进行分类
categories = defaultdict(list)

for filename, labels in results.items():
    if not labels:
        categories["未识别"].append(filename)
        continue

    # 主标签作为分类依据
    primary_label = labels[0].lower()

    # 创建更智能的分类
    if any(word in primary_label for word in ["animal", "toy", "plush", "bear", "dog", "cat", "rabbit"]):
        categories["玩具/动物"].append(filename)
    elif any(word in primary_label for word in ["text", "ticket", "label", "sign", "poster", "newspaper"]):
        categories["文字/标签"].append(filename)
    elif any(word in primary_label for word in ["vehicle", "car", "bike", "transport"]):
        categories["交通工具"].append(filename)
    elif any(word in primary_label for word in ["nature", "plant", "flower", "tree", "leaf"]):
        categories["自然/植物"].append(filename)
    elif any(word in primary_label for word in ["food", "fruit", "cake", "drink"]):
        categories["食物"].append(filename)
    elif any(word in primary_label for word in ["sport", "game", "ball", "play"]):
        categories["运动/游戏"].append(filename)
    elif any(word in primary_label for word in ["person", "people", "face", "head"]):
        categories["人物"].append(filename)
    elif any(word in primary_label for word in ["art", "pattern", "design", "color"]):
        categories["艺术/设计"].append(filename)
    else:
        categories[f"其他-{primary_label}"].append(filename)

# 输出分类清单
print("\n" + "=" * 60)
print("📋 VOYAGEUR-Stickers 分类清单")
print("=" * 60)

output = []
for category in sorted(categories.keys()):
    items = sorted(categories[category], key=lambda x: int(x.replace("sticker", "").replace(".png", "")))
    print(f"\n【{category}】共 {len(items)} 张")
    output.append(f"\n【{category}】共 {len(items)} 张")

    # 显示编号
    numbers = [x.replace("sticker", "").replace(".png", "") for x in items]
    print(f"编号: {', '.join(numbers)}")
    output.append(f"编号: {', '.join(numbers)}")

# 保存到文件
with open("/Users/wyl/Documents/GitHub/VOYAGEUR-Stickers/分类清单.txt", "w", encoding="utf-8") as f:
    for line in output:
        f.write(line + "\n")

print("\n" + "=" * 60)
print(f"✅ 分类完成！共 {len(results)} 张贴纸，分为 {len(categories)} 类")
print(f"详细清单已保存到: 分类清单.txt")

# 同时保存详细的JSON结果用于参考
with open("/Users/wyl/Documents/GitHub/VOYAGEUR-Stickers/分析结果.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("详细分析结果已保存到: 分析结果.json")
