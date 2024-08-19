import win32gui
import win32ui
from ctypes import windll
import cv2
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QScreen
import gui_tools as Gt


def read_img(filename):
    # 读取图像
    img = cv2.imread(filename, 1)

    # 检查图像是否成功加载
    if img is None:
        print(f"[ERROR]: 图片 '{filename}' 无法被加载")
        return None

    return img


def read_img2mask(filename):
    # 读取图像
    img = cv2.imread(filename, 0)

    # 检查图像是否成功加载
    if img is None:
        print(f"[ERROR]: 图片 '{filename}' 无法被加载")
        return None

    # 将所有非零像素转换为255
    # 使用阈值操作将图像转换为二值图像
    _, mask = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)

    # # 检查并显示蒙版
    # if mask is not None:
    #     print(f"features/read_img2mask: 图片 '{filename}' 加载成功")
    #     # cv2.imshow('Mask', mask)
    #     # cv2.waitKey(0)
    #     # cv2.destroyAllWindows()

    return mask


def match_template_with_mask(image, template, mask):

    # 执行模板匹配（归一化相关系数）
    match_method = cv2.TM_CCOEFF_NORMED
    similarity = cv2.matchTemplate(image, template, match_method, mask=mask)

    return similarity


def average_rgb_within_mask(image, mask):
    # avg_bgr = cv2.mean(image, mask=mask)[:3]
    # 将BGR转换为RGB
    # avg_rgb = avg_bgr[::-1]
    # 将BGR图像转换为HSV图像
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 使用蒙版作为权重，只计算蒙版为白色的像素的平均HSV值
    avg_hsv = cv2.mean(hsv_image, mask=mask)[:3]

    return avg_hsv


def get_window_info():
    # 使用win32gui获取窗口handle及位置像素等信息
    pass


def capture_screen(window_name):
    hwnd = win32gui.FindWindow(None, window_name)  # 获取窗口的句柄

    if hwnd == 0:
        print("[ERROR]: 窗口句柄获取失败")
        return False

    # 使用高 DPI 显示器（或 > 100% 缩放尺寸）
    windll.user32.SetProcessDPIAware()

    # 窗口的客户区
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)  # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框。DC（Device Context）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 创建设备描述表
    saveDC = mfcDC.CreateCompatibleDC()  # 创建内存设备描述表

    saveBitMap = win32ui.CreateBitmap()  # 创建位图对象准备保存图片
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)  # 为bitmap开辟空间

    saveDC.SelectObject(saveBitMap)  # 将截图保存到saveBitMap中

    # saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)  # 保存bitmap到内存设备描述表

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    # 最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
    # 选择合适的 window number，如0，1，2，3，直到截图从黑色变为正常画面
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    print(result)

    # 保存图像
    # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")  # 使用windows api，保存到.bmp

    # opencv+numpy保存
    signedIntsArray = saveBitMap.GetBitmapBits(True)  # 获取位图信息

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    # opencv+numpy保存
    # 若PrintWindow成功，保存到文件，显示到屏幕
    if result == 1:
        im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
        im_opencv.shape = (height, width, 4)

        img_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_RGBA2RGB)

        # cv2.imwrite("img_opencv.jpg", img_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存1
        # cv2.imwrite("img_opencv.png", img_opencv)  # 保存2

        # cv2.imshow("img_opencv", img_opencv)  # 显示
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # print("features/capture_screen: 成功返回截图")
        return img_opencv  # 返回opencv图片
    else:
        print("[ERROR]: 截图获取失败")
        return False


# # 使用PyQt6获取屏幕对应位置的图像
# screen = QApplication.primaryScreen()
# pixmap = screen.grabWindow(handle)
# pixmap.save('123.png')  # 可以直接保存为文件, qt 会根据扩展名 保存成不同的格式


def process_image(im_opencv, template, mask):
    # 使用cv2进行处理和模板匹配
    similarity = match_template_with_mask(im_opencv, template, mask)

    # 返回相似度
    return similarity


def check_window_state(similar_money_cart, color_blood_bar, similar_death):
    game_player = 0
    # 根据处理后的信息，判断当前窗口状态，执行对应处理
    if similar_money_cart > 0.92:
        if 96 <= color_blood_bar[0] <= 110:
            game_player = 0
            print("当前阵营：CT")
        elif 16 <= color_blood_bar[0] <= 30:
            game_player = 0
            print("当前阵营：T")
        else:
            if similar_death > 0.7:
                game_player = 1
                print("检测到玩家死亡")
    else:
        print("玩家处于空闲状态")

    return game_player



def feature_test():

    cs2_window_name = "Counter-Strike 2"
    cs2_window_handle = win32gui.FindWindow(None, cs2_window_name)
    print(cs2_window_handle)
    print(win32gui.GetWindowRect(cs2_window_handle))  # 相对屏幕 窗体带阴影 坐标
    print(win32gui.GetClientRect(cs2_window_handle))  # 相对工作区 工作区 坐标

    print(win32gui.ScreenToClient(cs2_window_handle, (320, 180)))  # 屏幕坐标 转换为 相对指定工作区的坐标
    print(win32gui.ClientToScreen(cs2_window_handle, (0, 0)))  # 工作区指定点坐标 转换为屏幕坐标

    # def grabWindow(self, WId=0, x, y, width, height) -> QPixmap:

    # # 打印图像的信息
    # print("Image type:", type(image))
    # print("Image shape:",
    #       image.shape)  # (height, width, channels) for color images or (height, width) for grayscale
    # print("Image dtype:", image.dtype)  # Depth of each pixel
    # print("Image ndim:", image.ndim)  # Number of dimensions
