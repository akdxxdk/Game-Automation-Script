import pynput
import time
from ctypes import cdll
import threading
from mouse import *

p = r'./Dll.dll'
dll = cdll.LoadLibrary(p)
for i in range(10):
    dll.MoveTo2(int(10), int(10))
    time.sleep(1)


def lock_thread(tag, x_center, y_center, height, auto_fire):
    # 如果检测到头部
    if tag == 0:
        dll.MoveTo2(int(x_center), int(y_center))
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()
    # 如果检测到身体
    elif tag == 1:
        dll.MoveTo2(int(x_center), int(y_center - 1 / 6 * height))
        dll.MoveTo2(int(x_center), int(-100))
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()


def recoil_head(x_center, y_center):
    dll.MoveTo2(int(x_center), int(y_center))


def recoil_body(x_center, y_center, height):
    dll.MoveTo2(int(x_center), int(y_center - 1 / 6 * height))
    dll.MoveTo2(int(x_center), int(-20))


# 普通模式
def lock1(aims, mouse, x, y, auto_fire):
    mouse_pos_x, mouse_pos_y = mouse.position  # 获取当前鼠标位置
    dist_list = []  # 存放每个目标的中心点
    for det in aims:
        _, x_c, y_c, _, _ = det
        # (4 ** 0.5)是求平方根，(4 ** 2)是求的平方
        dist = (x * float(x_c) - mouse_pos_x) ** 2 + (y * float(y_c) - mouse_pos_y) ** 2  # 两点间距离公式
        dist_list.append(dist)

    det = aims[dist_list.index(min(dist_list))]  # index返回min(dist_list)在dist_list列表的索引值      取最近距离的目标

    tag, x_center, y_center, width, height = det
    # 把归一化的[cls, x_c, y_c, w, h]恢复到原图大小
    tag = int(tag)
    x_center, width = x * float(x_center), x * float(width)
    y_center, height = y * float(y_center), y * float(height)

    if tag == 0:
        dll.MoveTo2(int(x_center), int(y_center))
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()
    # 如果检测到身体
    elif tag == 1:
        dll.MoveTo2(int(x_center), int(y_center - 1 / 6 * height))
        dll.MoveTo2(int(x_center), int(-100))
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()

# 正常模式
def lock2(aims, mouse, x, y, auto_fire):
    mouse_pos_x, mouse_pos_y = mouse.position  # 获取当前鼠标位置
    dist_list = []  # 存放每个目标的中心点
    for det in aims:
        _, x_c, y_c, _, _ = det
        # (4 ** 0.5)是求平方根，(4 ** 2)是求的平方
        dist = (x * float(x_c) - mouse_pos_x) ** 2 + (y * float(y_c) - mouse_pos_y) ** 2  # 两点间距离公式
        dist_list.append(dist)

    det = aims[dist_list.index(min(dist_list))]  # index返回min(dist_list)在dist_list列表的索引值      取最近距离的目标

    tag, x_center, y_center, width, height = det
    # 把归一化的[cls, x_c, y_c, w, h]恢复到原图大小
    tag = int(tag)
    x_center, width = x * float(x_center), x * float(width)
    y_center, height = y * float(y_center), y * float(height)

    # 创建锁人线程
    lock_head = threading.Thread(target=recoil_head, args=(x_center, y_center))
    lock_body = threading.Thread(target=recoil_body, args=(x_center, y_center, height))
    if tag == 0:
        lock_head.start()
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()
    # 如果检测到身体
    elif tag == 1:
        lock_body.start()
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()

# 优化模式
def lock3(aims, mouse, x, y, auto_fire):
    mouse_pos_x, mouse_pos_y = mouse.position  # 获取当前鼠标位置
    dist_list = []  # 存放每个目标的中心点
    for det in aims:
        _, x_c, y_c, _, _ = det
        # (4 ** 0.5)是求平方根，(4 ** 2)是求的平方
        dist = (x * float(x_c) - mouse_pos_x) ** 2 + (y * float(y_c) - mouse_pos_y) ** 2  # 两点间距离公式
        dist_list.append(dist)

    det = aims[dist_list.index(min(dist_list))]  # index返回min(dist_list)在dist_list列表的索引值      取最近距离的目标

    tag, x_center, y_center, width, height = det
    # 把归一化的[cls, x_c, y_c, w, h]恢复到原图大小
    tag = int(tag)
    x_center, width = x * float(x_center), x * float(width)
    y_center, height = y * float(y_center), y * float(height)

    # 创建锁人线程
    lock_body_head = threading.Thread(target=lock_thread, args=(tag, x_center, y_center, height, auto_fire))
    lock_body_head.start()

# 驱动模式
def lock4(aims, mouse, x, y, auto_fire):
    mouse_pos_x, mouse_pos_y = mouse.position  # 获取当前鼠标位置
    dist_list = []  # 存放每个目标的中心点
    for det in aims:
        _, x_c, y_c, _, _ = det
        # (4 ** 0.5)是求平方根，(4 ** 2)是求的平方
        dist = (x * float(x_c) - mouse_pos_x) ** 2 + (y * float(y_c) - mouse_pos_y) ** 2  # 两点间距离公式
        dist_list.append(dist)

    det = aims[dist_list.index(min(dist_list))]  # index返回min(dist_list)在dist_list列表的索引值      取最近距离的目标

    tag, x_center, y_center, width, height = det
    # 把归一化的[cls, x_c, y_c, w, h]恢复到原图大小
    tag = int(tag)
    x_center, width = x * float(x_center), x * float(width)
    y_center, height = y * float(y_center), y * float(height)
    print(x_center, y_center)

    if tag == 0:
        mouse_xy(int(x_center-400), int(y_center+200))
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()
    # 如果检测到身体
    elif tag == 1:
        mouse_xy(int(x_center), int(y_center - 1 / 6 * height))
        mouse_xy(int(x_center), int(-100))
        if auto_fire:
            dll.LeftDown()
            time.sleep(0.001)
            dll.LeftUp()

