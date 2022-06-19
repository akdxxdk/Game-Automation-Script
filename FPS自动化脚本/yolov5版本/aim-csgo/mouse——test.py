import pynput
from pynput.mouse import Listener, Button

"""监听鼠标事件"""

# 监听鼠标按键
# on_click(x, y, button, pressed)是鼠标点击时回调的函数
# 四个参数x，y，button，pressed。
# x，y描述的是鼠标点击的位置
# button是鼠标的按键，值有三种Button.left(左键)、Button.right（右键）、Button.middle（中键）
# 注意鼠标button使用按下一次会有两次反馈（按下和松开）。想要使用一次可以把一个if pressed:语句放在它的外层
# pressed的值是bool类型是鼠标按键的按下时是True，松开时为False。
def on_click(x, y, button, pressed):
    if button == Button.left:
        print('{0}位置{1}'.format('鼠标按下' if pressed else '鼠标松开', (x, y)))
    elif button == Button.middle:  # 停止监听
        return False


# Collect events until released
# with Listener(on_click=on_click) as listener:
#     listener.join()


lock_mode = False
with pynput.mouse.Events() as events:
    print('~')
    while True:
        it = next(events)
        while it is not None and not isinstance(it, pynput.mouse.Events.Click):
            it = next(events)
        if it is not None and it.button == it.button.left and it.pressed:
            lock_mode = not lock_mode
            print('lock mode', 'on' if lock_mode else 'off')
            print("是否锁人 = ", lock_mode)