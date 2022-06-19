#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project : pytorch_射击游戏
# @FileName  :深度学习推理.py
# @Time      :2022/5/19 21:28
# @Author    :和孔哥一起学
# @Email     :2338199895@qq.com
# @CSDN and Public      :和孔哥一起学

import cv2
import torch
import torchvision
import numpy as np
import torchvision.transforms as transforms

# 定义使用COCO数据集对应的每类的名称
"""
    fire hydrant 消防栓，stop sign 停车标志， parking meter 停车收费器， bench 长椅。
    zebra 斑马， giraffe 长颈鹿， handbag 手提包， suitcase 手提箱， frisbee （游戏用）飞盘（flying disc）。
    skis 滑雪板（ski的复数），snowboard 滑雪板（ski是单板滑雪，snowboarding 是双板滑雪。）
    kite 风筝， baseball bat 棒球棍， baseball glove 棒球手套， skateboard 滑板， surfboard 冲浪板， tennis racket 网球拍。
    broccoli 西蓝花，donut甜甜圈，炸面圈(doughnut，空心的油炸面包), cake 蛋糕、饼, couch 长沙发（靠chi)。
    potted plant 盆栽植物。 dining table 餐桌。 laptop 笔记本电脑，remote 遥控器(=remote control), 
    cell phone 移动电话(=mobile phone)(cellular 细胞的、蜂窝状的)， oven 烤炉、烤箱。 toaster 烤面包器（toast 烤面包片）
    sink 洗碗池, refrigerator 冰箱。（=fridge）， scissor剪刀(see, zer), teddy bear 泰迪熊。 hair drier 吹风机。 
    toothbrush 牙刷。
"""

# COCO数据集对应的类别
COCO_INSTANCE_CATEGORY_NAMES = [
    '__BACKGROUND__', 'person', 'bicycle', 'car', 'motorcycle',
    'airplane', 'bus', 'train', 'trunk', 'boat', 'traffic light',
    'fire hydrant', 'N/A', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
    'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A',
    'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A',
    'dining table', 'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop',
    'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven',
    'toaster', 'toaster', 'sink', 'refrigerator', 'N/A', 'book', 'clock',
    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# 定义能够检测出的关键点名称
"""
    elbow 胳膊肘，wrist 手腕，hip 臀部
"""
COCO_PERSON_KEYPOINT_NAMES = ['nose', 'left_eye', 'right_eye', 'left_ear',
                              'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow',
                              'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
                              'left_knee', 'right_knee', 'left_ankle', 'right_ankle']

# 加载pytorch提供的keypointrcnn_resnet50_fpn()网络模型，可以对17个人体关键点进行检测。
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torchvision.models.detection.keypointrcnn_resnet50_fpn(pretrained=True)
model.to(device)
model.eval()

def My_Detect(image, threshold=0.9):
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    # 准备需要检测的图像
    transform_d = transforms.Compose([transforms.ToTensor()])
    image_t = transform_d(image)    ## 对图像进行变换
    # print(image_t.shape)
    pred = model([image_t.to(device)])         ## 将模型作用到图像上
    # 检测出目标的类别和得分
    pred_class = [COCO_INSTANCE_CATEGORY_NAMES[ii] for ii in list(pred[0]['labels'].cpu().numpy())]
    pred_score = list(pred[0]['scores'].detach().cpu().numpy())
    # print(pred_class,pred_score)
    # 检测出目标的边界框
    pred_boxes = [[ii[0], ii[1], ii[2], ii[3]] for ii in list(pred[0]['boxes'].detach().cpu().numpy())]
    ## 只保留识别的概率大约 threshold 的结果。
    pred_index = [pred_score.index(x) for x in pred_score if x > threshold]
    for index in pred_index:
        box = pred_boxes[index]
        box = [int(i) for i in box]
        cv2.rectangle(image,(int(box[0]),int(box[1])),(int(box[2]),int(box[3])),(0,255,255))
        texts = pred_class[index] + ":" + str(np.round(pred_score[index], 2))
        cv2.putText(image, texts,(box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

    pred_keypoint = pred[0]["keypoints"]
    # 检测到实例的关键点
    pred_keypoint = pred_keypoint[pred_index].detach().cpu().numpy()
    # 对实例数量索引
    my_result = {}
    for index in range(pred_keypoint.shape[0]):
        # 对每个实例的关键点索引
        keypoints = pred_keypoint[index]
        for ii in range(keypoints.shape[0]): ##ii为第几个坐标点
            x = int(keypoints[ii, 0]) #x坐标
            y = int(keypoints[ii, 1]) #y坐标
            visi = keypoints[ii, 2] #置信度
            if visi > 0.:
                cv2.circle(image, (int(x),int(y)), 1, (0,0,255),4)
                texts = str(ii+1)
                cv2.putText(image,texts, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
                my_result[texts] = (int(x), int(y))
    return image,my_result