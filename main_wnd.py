# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_wnd.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(842, 430)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"font: 24pt \"楷体\";")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setStyleSheet("font: 24pt \"楷体\";\n"
"background-color: rgb(0, 170, 0);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setStyleSheet("font: 24pt \"宋体\";\n"
"background-color: rgb(255, 0, 0);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 1, 2, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setEnabled(True)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout_3.addWidget(self.textEdit_2, 1, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_3.addWidget(self.pushButton_4, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.single_run)
        self.pushButton_2.clicked.connect(MainWindow.loop_run)
        self.pushButton_3.clicked.connect(MainWindow.stop)
        self.pushButton_4.clicked.connect(MainWindow.clear_log_slot)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "自动操作工具"))
        self.pushButton.setText(_translate("MainWindow", "cmd"))
        self.pushButton_2.setText(_translate("MainWindow", "cmd2"))
        self.pushButton_3.setText(_translate("MainWindow", "停止"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#5500ff;\">使用说明：</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#5500ff;\">1、把每一步要操作的图标、区域截图保存至本文件夹  png格式（注意如果同屏有多个相同图标，回默认找到最左上的一个，因此怎么截图，截多大的区域，是个学问，如输入框只截中间空白部分肯定是不行的，宗旨就是“唯一”）</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; color:#5500ff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">2、在</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">cmd.x</span><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">ls </span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">的</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">sheet</span><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">1 </span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">中，配置每一步的指令，如指令类型</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">1</span><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">234  </span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">对应的内容填截图文件名（别用中文），指令</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">5</span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">对应的内容是等待时长（单位秒） 指令</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">6</span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">对应的内容是滚轮滚动的距离，正数表示向上滚，负数表示向下滚</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">,</span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">数字大一点，先用</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">2</span><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">00</span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">和</span><span style=\" font-family:\'宋体\',\'等线\'; font-size:10pt; color:#5500ff;\">-</span><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">200</span><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">试试</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'宋体\'; font-size:10pt; color:#5500ff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\'; font-size:10pt; color:#5500ff;\">3、</span><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">保存文件</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'等线\'; font-size:10pt; color:#5500ff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">4、开始程序后请将程序框最小化，不然程序框挡住的区域是无法识别和操作的</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'等线\'; font-size:10pt; color:#5500ff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">5、如果程序开始后因为你选择了无限重复而鼠标被占用停不下来，alt+F4吧~</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'等线\'; font-size:10pt; color:#5500ff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'等线\'; font-size:10pt; color:#5500ff;\">6、如果出错，请把日志复制出来发给Lee分析</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "日志:"))
        self.pushButton_4.setText(_translate("MainWindow", "清除日志"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())