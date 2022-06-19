#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project : pytorch_射击游戏
# @FileName  :opencv_main.py
# @Time      :2022/5/19 7:07
# @Author    :和孔哥一起学
# @Email     :2338199895@qq.com
# @CSDN and Public      :和孔哥一起学


import numpy as np
import pyautogui
import win32gui, win32api, win32con
import cv2
import math
import time

CONFIG_FILE = "./yolov3.cfg"
WEIGHT_FILE = "./yolov3.weights"

net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHT_FILE)

net.setPerferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPerferableTarget(cv2.dnn.DNN_TARGET_CUDA)

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayters()]

hwnd = win32gui.GetDesktopWindow()
# hwnd = win32gui.FindWindow(None, "")
rect = win32gui.GetWindowRect(hwnd)
region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

while True:
    frame = np.array(pyautogui.screenshot(region=region))
    frame_hight, frame_width = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutLayters = net.forward(ln)

    boxes = []
    confidences = []

    for output in layerOutLayters:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > 0.7 and classID == 0:
                box = detection[:4] * np.array([frame_width, frame_hight, frame_width, frame_hight])
                (certerX, centerY, width, height) = box.astype("int")
                x = int(certerX - (width / 2))
                y = int(centerY - (height / 2))
                box = [x, y, int(width), int(height)]
                boxes.append(box)
                confidences.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indices) > 0:
        print(f"Dectioned:{len(indices)}")
        min = 99999
        min_at = 0
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            cv2.rectangle(frame, (x, y), ((x + w), y + h), (255, 255, 255), 2)

            dist = math.sqrt(
                math.pow(frame_width / 2 - (x + w / 2), 2) + math.pow(frame_hight / 2 - (y + h / 2) - (y + h / 2), 2))
            if dist < min:
                min = dist
                min_at = i
        x = int(boxes[min_at][0] + boxes[min_at][2] / 2 - frame_width / 2)
        y = int(boxes[min_at][1] + boxes[min_at][3] / 2 - frame_hight / 2) - boxes[min_at][3] * 0.45

        x = int(x + scores)
        y = int(x + scores)

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,x, y, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
