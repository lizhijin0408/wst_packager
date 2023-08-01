from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui
import sys
import pyautogui
import pydirectinput
import time
import xlrd
import pyperclip
import _thread

from main_wnd import Ui_MainWindow

task_exit = False

def mouseLeftClick():
    pyautogui.click()

def mouseClick(clickTimes, lOrR, img, reTry):
    global task_exit
    if reTry == 1:
        location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        # print(location)
        if location is not None:
            pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
            return True
        print("未找到匹配图片")
        return False
    elif reTry == -1:
        location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        # print(location)
        if location is not None:
            while True:
                if task_exit:
                    return True
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
                time.sleep(0.1)
        print("未找到匹配图片")
        return False
    elif reTry > 1:
        i = 1
        location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        # print(location)
        if location is not None:
            while i < reTry + 1:
                if task_exit:
                    return True
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
                print("重复")
                i += 1
                time.sleep(0.1)
        print("未找到匹配图片")
        return False

scroll_pos_list = {}
# 数据检查
# cmdType.value  1.0 左键单击    2.0 左键双击  3.0 右键单击  4.0 输入  5.0 等待  6.0 滚轮 7.0 鼠标移动 8.0 单击坐标
# ctype     空：0
#           字符串：1
#           数字：2
#           日期：3
#           布尔：4
#           error：5
def dataCheck(sheet1):
    checkCmd = True
    #行数检查
    if sheet1.nrows < 2:
        print("没数据啊哥")
        checkCmd = False
    #每行数据检查
    i = 1
    while i < sheet1.nrows:
        # 第1列 操作类型检查
        cmdType = sheet1.row(i)[0]
        if cmdType.ctype != 2 or (cmdType.value != 1.0 and cmdType.value != 2.0 and cmdType.value != 3.0
                                  and cmdType.value != 4.0 and cmdType.value != 5.0 and cmdType.value != 6.0
                                  and cmdType.value != 7.0 and cmdType.value != 8.0 and cmdType.value != 9.0):
            print('第', i+1, "行,第1列数据有毛病")
            checkCmd = False
        # 第2列 内容检查
        cmdValue = sheet1.row(i)[1]
        # 读图点击类型指令，内容必须为字符串类型
        if cmdType.value == 1.0 or cmdType.value == 2.0 or cmdType.value == 3.0 or cmdType.value == 7.0\
                or cmdType.value == 8.0:
            if cmdValue.ctype != 1:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 输入类型，内容不能为空
        if cmdType.value == 4.0:
            if cmdValue.ctype == 0:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 等待类型，内容必须为数字
        if cmdType.value == 5.0:
            if cmdValue.ctype != 2:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 滚轮事件，内容必须为数字
        if cmdType.value == 6.0:
            if cmdValue.ctype != 2:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 滚轮事件，内容必须为数字
        if cmdType.value == 9.0:
            if cmdValue.ctype != 2:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
            else:
                scroll_pos_list[str(i)] = 0
        i += 1
    return checkCmd

#任务
def mainWork(sheet1):
    i = 1
    global task_exit
    print(f'总共有 {sheet1.nrows} 行指令')
    while i < sheet1.nrows:
        if task_exit:
            return
        print(f'开始执行第{i}条指令')
        #取本行指令的操作类型
        cmdType = sheet1.row(i)[0]
        if cmdType.value == 1.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            print("单击左键", img)
            mouseClick(1, "left", img, reTry)
        #2代表双击左键
        elif cmdType.value == 2.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            #取重试次数
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            print("双击左键", img)
            mouseClick(2, "left", img, reTry)
        #3代表右键
        elif cmdType.value == 3.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            #取重试次数
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            print("右键", img)
            mouseClick(1, "right", img, reTry)
        #4代表输入
        elif cmdType.value == 4.0:
            inputValue = sheet1.row(i)[1].value
            print("输入:", inputValue)
            pyperclip.copy(inputValue)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
        #5代表等待
        elif cmdType.value == 5.0:
            #取图片名称
            waitTime = sheet1.row(i)[1].value
            print("等待", waitTime, "秒")
            time.sleep(waitTime)
        #6代表滚轮
        elif cmdType.value == 6.0:
            #取图片名称
            scroll = sheet1.row(i)[1].value
            print("滚轮滑动", int(scroll), "距离")
            pyautogui.scroll(int(scroll))
        #6代表鼠标移动
        elif cmdType.value == 7.0:
            #取图片名称
            pos = sheet1.row(i)[1].value
            pos_split = pos.split(',')
            if len(pos_split) != 2:
                print(f'鼠标移动坐标位置设置不对 {pos}')
            else:
                try:
                    posx = int(pos_split[0].strip())
                    posy = int(pos_split[1].strip())
                    print(f"滚轮移动到 {posx} {posy}")
                    pyautogui.moveTo(posx, posy, duration=0.25)
                except Exception as e:
                    print(f'鼠标移动坐标位置设置不对 {pos}')
        #6代表单击坐标位置
        elif cmdType.value == 8.0:
            # print("鼠标左键单击")
            # pyautogui.click()
            # pydirectinput.click(relative=True)
            pos = sheet1.row(i)[1].value
            pos_split = pos.split(',')
            if len(pos_split) != 2:
                print(f'鼠标移动坐标位置设置不对 {pos}')
            else:
                try:
                    posx = int(pos_split[0].strip())
                    posy = int(pos_split[1].strip())
                    print(f"鼠标左键单击 {posx} {posy}")
                    # pyautogui.click(posx, posy, clicks=2, interval=0.2, duration=0.2, button="left")
                    pyautogui.doubleClick()
                except Exception as e:
                    print(f'鼠标移动坐标位置设置不对 {pos}')
        #9代表滚轮(支持累加)
        elif cmdType.value == 9.0:
            #取图片名称
            scroll = sheet1.row(i)[1].value
            scroll += scroll_pos_list[str(i)]
            scroll_pos_list[str(i)] = scroll
            print("滚轮滑动", int(scroll), "距离")
            pyautogui.scroll(int(scroll))
        i += 1

class Stream(QtCore.QObject):
    """Redirects console output to text widget."""
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowTitle("答题工具V1.1")
        sys.stdout = Stream(newText=self.onUpdateText)
        self.thread_run = False
        self.stop_run = False

    def clear_log_slot(self):
        self.textEdit_2.clear()

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.textEdit_2.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_2.setTextCursor(cursor)
        self.textEdit_2.ensureCursorVisible()

    def single_run(self):
        print('运行cmd.xls')
        _thread.start_new_thread(self.luti_thread, ('cmd.xls',))

    def loop_run(self):
        print('运行cmd2.xls')
        _thread.start_new_thread(self.luti_thread, ('cmd2.xls',))

    def stop(self):
        print('停止运行')
        global task_exit
        task_exit = True
        self.stop_run = True

    def luti_thread(self, file):
        global task_exit
        task_exit = False
        self.stop_run = False
        self.thread_run = True
        # file = 'cmd.xls'
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        print('欢迎使用Lee的自动界面操作工具~')
        # 打开文件
        try:
            wb = xlrd.open_workbook(filename=file)
            sheet1 = wb.sheet_by_index(0)
        except Exception as e:
            print(e)
            self.thread_run = False
            self.stop_run = False
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            return
        checkCmd = dataCheck(sheet1)
        if checkCmd:
            # 循环拿出每一行指令
            # if loop:
            if True:
                while True:
                    if self.stop_run:
                        self.stop_run = False
                        break
                    mainWork(sheet1)
                    time.sleep(0.1)
            # else:
            #     mainWork(sheet1)
        else:
            print('输入有误或者已经退出!')
        print('自动化操作退出')
        self.thread_run = False
        self.stop_run = False
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())