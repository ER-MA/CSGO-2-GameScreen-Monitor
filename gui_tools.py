import win32gui


# 获取所有窗口的句柄
def get_all_windows():
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    print(hWnd_list)
    return hWnd_list


# 获取子窗口的句柄
def get_son_windows(parent):
    hWnd_child_list = []
    win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd), hWnd_child_list)
    print(hWnd_child_list)
    return hWnd_child_list


# 获取句柄的标题
def get_title(hwnd):
    title = win32gui.GetWindowText(hwnd)
    print('窗口标题:%s' % (title))
    return title


# 获取窗口类名
def get_class_name(hwnd):
    clasname = win32gui.GetClassName(hwnd)
    print('窗口类名:%s' % (clasname))
    return clasname


# 使用标题搜索句柄
def find_enum_by_title(title):
    handle = win32gui.FindWindow(None, title)
    return handle


# 获取窗口坐标
def get_window_rect(handle):
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    coordinates = (left, top, right, bottom)
    return coordinates


# 获取窗口坐标
def get_window_client_rect(handle):
    left, top, right, bottom = win32gui.GetClientRect(handle)
    rect = (left, top, right, bottom)
    return rect


def get_window_size(rect):
    # rect 元组包含 (left, top, right, bottom)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    return width, height
