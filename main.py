from collections import deque

import cv2
import win32gui
from PyQt6.QtWidgets import QApplication
import pyautogui



import sys
import time

import features as ft


def main():
    # 初始化自定义变量
    # cs2_window_name = "Counter-Strike 2"  # 国际服使用这个窗口名
    cs2_window_name = "反恐精英：全球攻势"  # 国服使用这个窗口名
    cs2_class_name = "SDL_app"
    cs2_app_name = "cs2.exe"
    cs2_app_path = r"D:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe"  # 替换为你本地的cs2路径（不过暂时没用上）

    # ft.feature_test()

    # app = QApplication(sys.argv)
    # 创建实例，PyQt6 的基础，会通过 `app.exec()` 开启的主循环
    # 用完后用 `sys.exit(app.exec())` 结束应用程序
    # 或使用 `app.quit()` 让 QAPP 运行完后自行退出
    # 游戏的硬件加速导致第三方库湖区的截图均为纯黑，故弃用

    player_faction = deque(maxlen=600)  # 玩家阵营（存储10分钟内信息的双队列）

    img_test_game = ft.read_img("img_test/gameUI_CT_death_01.png")
    img_test_template = ft.read_img("img_test/gameUI_CT_death_00.png")
    img_test_bold = ft.read_img("img_test/gameUI_T_play_00.png")

    # 主循环
    running = True
    while running:

        # 获取窗口信息
        # window_info = ft.get_window_info()

        # 截取屏幕
        cs2_client_img = ft.capture_screen(cs2_window_name)

        # 处理图像
        # 购物车图标
        mask_money_cart = ft.read_img2mask("img_process/img_mask/gameUI_money_cart.png")
        similarity_money_cart = ft.process_image(cs2_client_img, img_test_template, mask_money_cart)
        print(f"main: 购物车图标相似度为 '{similarity_money_cart}' ")
        # 血条颜色
        mask_blood_bar = ft.read_img2mask("img_process/img_mask/gameUI_blood_bar_CT.png")
        color_blood_bar = ft.average_rgb_within_mask(cs2_client_img, mask_blood_bar)
        print(f"main: 血条颜色为 '{color_blood_bar}' ")
        # 死亡提示
        mask_death = ft.read_img2mask("img_process/img_mask/gameUI_death_popup_middle.png")
        similarity_death = ft.process_image(cs2_client_img, img_test_template, mask_death)
        print(f"main: 死亡提示相似度为 '{similarity_death}' ")

        # 检查窗口状态
        game_player = ft.check_window_state(similarity_money_cart, color_blood_bar, similarity_death)

        # 按下 'Y' 键
        if game_player == 1:
            # 等待五秒
            time.sleep(5)
            pyautogui.press('y')

        # player_faction.append((time.time(), faction))

        # 等待一秒
        time.sleep(0.5)

    print("[CSGO2Monitor]: 运行结束")
    # 关闭应用程序
    # app.quit()
    # 也是PyQt的遗孤


if __name__ == "__main__":
    main()





