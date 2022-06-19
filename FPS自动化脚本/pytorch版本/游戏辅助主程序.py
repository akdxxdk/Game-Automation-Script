#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project : pytorch_射击游戏
# @FileName  :游戏辅助主程序.py
# @Time      :2022/5/19 21:26
# @Author    :和孔哥一起学
# @Email     :2338199895@qq.com
# @CSDN and Public      :和孔哥一起学

import cv2
import time,pyautogui
from tkinter import *
from 游戏检测区域操作 import My_pywin32
from 深度学习推理  import My_Detect

"""
# moused_x,moused_y = win32api.GetCursorPos() #获取当前坐标
# win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,0,0,0,0)   #鼠标中键点击
# win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)
# time.sleep(0.01)
# # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
# # time.sleep(0.01)
# # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

fps游戏里的鼠标移动带来的是角度变化，移动多少像素点与游戏中的角度是正比例关系，4:3的分辨率下视角为90度，鼠标到人像上需要移动多少距离还得计算一下，不能直接靠一个参数搞定

2D坐标-3D坐标原理
    电脑的鼠标是在屏幕的2D坐标上运动的，而我们要获取的是3D世界中的一个三维坐标，在游戏引擎中的实现原理如下：
    先获取鼠标在屏幕上的2D坐标。
    结合摄像机平面计算出这个点在3D世界中的坐标。
    从这个3D坐标沿着摄像机的视角发射一条射线，让这个射线和3D世界中的对象发生碰撞。
    这样，如果发生了碰撞，我们就可以获取最先和射线碰撞的物体以及发生碰撞的点坐标。
"""


def cv_show(win_name,roi_image):
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_name, 640, 320)
    cv2.imshow(win_name, roi_image)
    cv2.moveWindow(win_name, 1280, 0)
    cv2.getWindowImageRect(win_name)

def gui_ui():
    myUI = Tk()  # 界面开头
    myUI.title("学习测试项目")
    myUI.geometry("400x120")
    myUI.resizable(0, 0)
    Label(myUI, text='欢迎来到学习测试项目', font=('微软雅黑', 28), fg='#FF69B4', bg="#CAFF70").pack()
    Button(myUI, text="开始学习！", width=13, height=1, command=main, activeforeground="green", activebackground="black").pack()
    Button(myUI, text="结束学习！", width=13, height=1, command=myUI.destroy).pack()
    mainloop()  # 界面结尾

def main():
    # 窗口标题 ,记得改为自己的窗口名，不然无法找到窗口句柄!!!
    win_name = "Counter-Strike: Global Offensive - Direct3D 9"
    # win_name = "腾讯手游助手" #窗口标题
    win_size = [1280, 720]  #窗口大小
    win_index = [0, 0]  #窗口放置位置
    win_more = 24   #窗口多余部分，即窗口标题
    my_pywin32 = My_pywin32(win_name, win_more) #创建窗口处理对象
    hwdn = my_pywin32.get_hwnd()    #获取窗口句柄
    my_pywin32.set_win(hwdn, win_size, win_index)    #设置窗口参数
    MouseX, MouseY = pyautogui.position()
    while True: #   循环处理
#     for i in range(0,300):
        start_time = time.time()    #开始时间
        img, Screen = my_pywin32.get_win_wh(hwdn)   #获取窗口截图
        img_roi, Screen_c,[x0,y0,x1,y1] = my_pywin32.get_roi(img, Screen)   #获取窗口截图ROI图片
        print("窗口大小为：", Screen)
        print("中心点为：", Screen_c)
        roi_image,my_result = My_Detect(img_roi, threshold=0.8) #ROI图像进行推理，返回图像与ROI图像中位置坐标
        print("图像推理结果为：", my_result)
        fps = int(1/(time.time() - start_time)) #   计算推理帧率
        print("FPS:{}".format(fps))
        cv_show(win_name, roi_image)  # OpenCV窗口显示结果图像
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if my_result == {}:
            continue

        #####################
        # 计算瞄准点与目标点之间的移动距离
        # 鼠标使用相对移动
        # 1.56为自测参数
        #####################
        x= int(my_result["1"][0])
        y = int(my_result["1"][0])
        currentMouseX = x / 1.56
        currentMouseY = y / 1.56
        pyautogui.moveRel(int(currentMouseX+MouseX), int(currentMouseY+MouseY))
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # main()
    gui_ui()