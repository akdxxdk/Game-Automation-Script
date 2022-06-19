#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project : pytorch_射击游戏
# @FileName  :游戏检测区域操作.py
# @Time      :2022/5/18 22:56
# @Author    :和孔哥一起学
# @Email     :2338199895@qq.com
# @CSDN and Public      :和孔哥一起学

import win32gui,win32api,win32ui,win32con
import numpy as np
import time

class My_pywin32(object):
    def __init__(self,win_name,win_more):
        self.win_name = win_name
        self.win_more = win_more

    def get_hwnd(self):
        hwnd_title = {}
        def _get_all_hwnd(hwnd, mouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

        win32gui.EnumWindows(_get_all_hwnd, 0)
        new_dict = {v: k for k, v in hwnd_title.items()}
        print(new_dict)
        # for wnd in hwnd_title.items():
        #     print(wnd)
        return new_dict[self.win_name]

    def set_win(self,hwdn,win_size=[1280, 720],win_index=[0,0]):
        """设置窗口大小尺寸并置顶"""
        win32gui.SetWindowPos(hwdn, win32con.HWND_TOPMOST, win_index[0], win_index[1], win_size[0], win_size[1], win32con.SWP_NOSIZE| win32con.SWP_SHOWWINDOW)

    def get_win_wh(self,hwnd):
        """游戏窗口截图"""
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # 根据窗口的DC获取mfcDC
        saveDC = mfcDC.CreateCompatibleDC()
        # mfcDC创建可兼容的DC
        saveBitMap = win32ui.CreateBitmap()
        # 创建bigmap准备保存图片
        rctA = win32gui.GetWindowRect(hwnd)
        Screen_w = rctA[2] - rctA[0]  # 游戏界面宽度
        Screen_h = rctA[3] - rctA[1]  # 游戏界面高度

        # 获取图片大小
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveBitMap.CreateCompatibleBitmap(mfcDC, Screen_w, Screen_h)
        # 为bitmap开辟空间
        saveDC.SelectObject(saveBitMap)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.BitBlt((0, 0), (Screen_w, Screen_h), mfcDC, (0, 0), win32con.SRCCOPY)

        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype="uint8")
        img.shape = (Screen_h, Screen_w, 4)
        # bit图转mat图
        win32gui.DeleteObject(saveBitMap.GetHandle())
        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        # 释放内存
        return img, (Screen_w,Screen_h)  # 转为RGB图返回

    def get_roi(self,img,Screen):
        Screen_w,Screen_h = Screen[0],Screen[1]-self.win_more
        Screen_cx = Screen_w // 2  # 游戏界面中心x
        Screen_cy = Screen_h // 2  # 游戏界面中心y
        Screen_c = [Screen_cx, Screen_cy]  # 游戏界面中心坐标
        x0 = Screen_cx - Screen_cx // 2    # 游戏界面检测框左上角x0
        y0 = Screen_cy - Screen_cy // 2    # 游戏界面检测框左上角y0
        x1 = Screen_cx + Screen_cx // 2    # 游戏界面检测框右下角x1
        y1 = Screen_cy + Screen_cy // 2    # 游戏界面检测框右下角y1
        # 选取roi = img[y0,y1,x0,x1]窗口
        print("ROI区域大小为",[x0,y0,x1,y1])
        roi = img[int(y0):int(y1),int(x0):int(x1)]
        return roi,Screen_c,[x0,y0+self.win_more,x1,y1+self.win_more]


if __name__ == '__main__':
    # 窗口标题
    win_name ="Counter-Strike: Global Offensive - Direct3D 9"
    print("游戏窗口标题为：",win_name)
    # 窗口多余部分，即窗口标题
    win_more = 24
    my_pywin32 = My_pywin32(win_name,win_more)
    # hwdn = my_pywin32.get_hwnd()
    # my_pywin32.set_win(hwdn)
    # img,Screen = my_pywin32.get_win_wh(hwdn)
    # img_roi,Screen_c = my_pywin32.get_roi(img,Screen)
    # print("窗口大小为：",Screen)
    # print("中心点为：",Screen_c)
    # import cv2
    # cv2.imshow("img",img_roi)
    # cv2.waitKey()
    # cv2.destroyAllWindows()