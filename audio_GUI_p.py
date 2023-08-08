from PyQt5.Qt import *
from audio_spider_p import *
import sys
import time


class WorkerThread(QThread):
    # 自定义信号，传递两个字符串参数
    finish = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.text1 = None
        self.text2 = None
        self.text3 = None

    def run(self):
        # 调用audio_spider_p.py的函数
        filename, url_headers = bv_name(self.text1, self.text2, self.text3)  # 得到文件路径和url及其请求头
        MusicName = music_name(self.text1)  # 待下载文件名的列表

        start_time = time.time()  # 下载开始时间
        for k in range(len(url_headers)):
            URL = list(url_headers[k].keys())[0]  # url
            headers = list(url_headers[k].values())[0]  # header

            res = send_request(URL, headers).text  # 源代码

            video = get_video_data(res, headers)  # 解析数据
            if video != 1:  # 判断video是否为1，不为1，则执行
                save_data(filename, video, MusicName[k])  # 下载音乐

        end_time = time.time()  # 下载结束时间

        value = str(round(end_time - start_time, 2)) + '秒'  # 下载用时，保留两位小数
        self.finish.emit(value)  # 发射信号，传递结果给主线程


class WorkerThread2(QThread):
    # 自定义信号，传递两个字符串参数
    finish = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkerThread2, self).__init__(parent)
        self.text1 = None
        self.text2 = None
        self.text3 = None

    def run(self):
        # 调用audio_spider_p.py的函数
        MusicName = music_name(self.text1)  # 待下载文件名的列表
        value = ''
        for i in range(len(MusicName)):

            value = value + str(i+1) + '：' + MusicName[i] + '\n'

        self.finish.emit(value)  # 发射信号，传递结果给主线程


class mainwindow(QWidget):

    def __init__(self):
        super(mainwindow, self).__init__()
        icon = QIcon("icon.ico")  # 创建一个图标对象
        self.setWindowIcon(icon)  # 设置窗口图标
        self.setWindowTitle("B站音频提取")

        self.setGeometry(350, 190, 1500, 1000)

        self.windowUI()

        self.resizeEvent = self.on_resize

    def windowUI(self):
        label_width = self.width()
        label_height = self.height()

        self.label_1 = QLabel(self)
        self.label_1.setGeometry(int(label_width / 2) - 125, 70, 250, 100)
        self.label_1.setText("B站音频提取")
        self.label_1.setFont(QFont('SimHei', 20))
        self.label_1_y = 70 / label_height
        self.label_1_w = 250 / label_width
        self.label_1_h = 100 / label_height

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(950, 920, 200, 100)
        self.label_2.setText("数据来源：Bilibili")
        self.label_2_x = 950 / label_width
        self.label_2_y = 920 / label_height
        self.label_2_w = 200 / label_width
        self.label_2_h = 100 / label_height


        self.label_3 = QLabel(self)
        self.label_3.setGeometry(1300, 920, 200, 100)
        self.label_3.setText("作者：Polaris")
        self.label_3_x = 1300 / label_width
        self.label_3_y = 920 / label_height
        self.label_3_w = 200 / label_width
        self.label_3_h = 100 / label_height


        self.label_4 = QLabel(self)
        self.label_4.setGeometry(400, 170, 200, 100)
        self.label_4.setText("输入BV号")
        self.label_4.setFont(QFont('SimSun', 20, 75))
        self.label_4_x = 400 / label_width
        self.label_4_y = 170 / label_height
        self.label_4_w = 200 / label_width
        self.label_4_h = 100 / label_height


        self.label_5 = QLabel(self)
        self.label_5.setGeometry(400, 620, 200, 100)
        self.label_5.setText("所属文件")
        self.label_5.setFont(QFont('SimSun', 20, 75))
        self.label_5_x = 400 / label_width
        self.label_5_y = 620 / label_height
        self.label_5_w = 200 / label_width
        self.label_5_h = 100 / label_height


        self.label_6 = QLabel(self)
        self.label_6.setGeometry(400, 720, 200, 100)
        self.label_6.setText("爬取数量")
        self.label_6.setFont(QFont('SimSun', 20, 75))
        self.label_6_x = 400 / label_width
        self.label_6_y = 720 / label_height
        self.label_6_w = 200 / label_width
        self.label_6_h = 100 / label_height


        self.label_7 = QLabel(self)
        self.label_7.setGeometry(400, 390, 200, 100)
        self.label_7.setText("音频目录")
        self.label_7.setFont(QFont('SimSun', 20, 75))
        self.label_7_x = 400 / label_width
        self.label_7_y = 390 / label_height
        self.label_7_w = 200 / label_width
        self.label_7_h = 100 / label_height


        self.label_8 = QLabel(self)
        self.label_8.setGeometry(400, 820, 200, 100)
        self.label_8.setText("下载用时")
        self.label_8.setFont(QFont('SimSun', 20, 75))
        self.label_8_x = 400 / label_width
        self.label_8_y = 820 / label_height
        self.label_8_w = 200 / label_width
        self.label_8_h = 100 / label_height


        self.line_1 = QLineEdit(self)  # BV号
        self.line_1.setGeometry(630, 200, 320, 40)
        self.line_1_x = 630 / label_width
        self.line_1_y = 200 / label_height
        self.line_1_w = 320 / label_width
        self.line_1_h = 40 / label_height


        self.line_2 = QLineEdit(self)  # 文件名
        self.line_2.setGeometry(630, 650, 320, 40)
        self.line_2_x = 630 / label_width
        self.line_2_y = 650 / label_height
        self.line_2_w = 320 / label_width
        self.line_2_h = 40 / label_height


        self.line_3 = QLineEdit(self)  # 爬取数量
        self.line_3.setGeometry(630, 750, 320, 40)
        self.line_3_x = 630 / label_width
        self.line_3_y = 750 / label_height
        self.line_3_w = 320 / label_width
        self.line_3_h = 40 / label_height


        self.text_1 = QTextEdit(self)  # 音频目录
        self.text_1.setGeometry(630, 300, 320, 300)
        self.text_1.setReadOnly(True)  # 设置文本框为只读
        self.text_1_x = 630 / label_width
        self.text_1_y = 300 / label_height
        self.text_1_w = 320 / label_width
        self.text_1_h = 300 / label_height


        self.text_2 = QTextEdit(self)  # 下载进度
        self.text_2.setGeometry(630, 850, 320, 40)
        self.text_2.setReadOnly(True)  # 设置文本框为只读
        self.text_2_x = 630 / label_width
        self.text_2_y = 850 / label_height
        self.text_2_w = 320 / label_width
        self.text_2_h = 40 / label_height


        self.btn = QPushButton('查看音频', self)
        self.btn.setFont(QFont('SimSun', 10, 75))
        self.btn.setGeometry(1100, 350, 200, 120)
        self.btn_x = 1100 / label_width
        self.btn_y = 350 / label_height
        self.btn_w = 200 / label_width
        self.btn_h = 120 / label_height

        self.btn_download = QPushButton('立即下载', self)
        self.btn_download.setFont(QFont('SimSun', 10, 75))
        self.btn_download.setGeometry(1100, 700, 200, 120)
        self.btn_download_x = 1100 / label_width
        self.btn_download_y = 700 / label_height
        self.btn_download_w = 200 / label_width
        self.btn_download_h = 120 / label_height

        """
        接下来是多线程操作
        在 mainwindow 类的构造函数中创建了一个 WorkerThread 对象（在主线程中创建一个子线程对象）
        """
        self.worker_thread = WorkerThread()
        self.worker_thread2 = WorkerThread2()
        # 绑定按钮事件
        self.btn_download.clicked.connect(self.start_thread)
        self.btn.clicked.connect(self.start_thread2)
        # 将子线程的 finish 信号连接到主线程的 value_change 槽函数上
        self.worker_thread.finish.connect(self.value_change)
        self.worker_thread2.finish.connect(self.value_change2)

    def update_positions(self):
        label_width = self.width()
        label_height = self.height()

        """
        setGeometry的参数必须是整数，这里使用了 __int__的隐式方法将float转成了int
        
        如果版本更新，这行报错了，需要自行将参数转换成整型
        """
        self.label_1.setGeometry(int(label_width / 2) - 100, int(self.label_1_y * label_height),
                                 int(self.label_1_w * label_width), int(self.label_1_h * label_height))
        self.label_2.setGeometry(int(self.label_2_x * label_width), int(self.label_2_y * label_height),
                                 int(self.label_2_w * label_width), int(self.label_2_h * label_height))
        self.label_3.setGeometry(int(self.label_3_x * label_width), int(self.label_3_y * label_height),
                                 int(self.label_3_w * label_width), int(self.label_3_h * label_height))
        self.label_4.setGeometry(int(self.label_4_x * label_width), int(self.label_4_y * label_height),
                                 int(self.label_4_w * label_width), int(self.label_4_h * label_height))
        self.label_5.setGeometry(int(self.label_5_x * label_width), int(self.label_5_y * label_height),
                                 int(self.label_5_w * label_width), int(self.label_5_h * label_height))
        self.label_6.setGeometry(int(self.label_6_x * label_width), int(self.label_6_y * label_height),
                                 int(self.label_6_w * label_width), int(self.label_6_h * label_height))
        self.label_7.setGeometry(int(self.label_7_x * label_width), int(self.label_7_y * label_height),
                                 int(self.label_7_w * label_width), int(self.label_7_h * label_height))
        self.label_8.setGeometry(int(self.label_8_x * label_width), int(self.label_8_y * label_height),
                                 int(self.label_8_w * label_width), int(self.label_8_h * label_height))

        self.line_1.setGeometry(int(self.line_1_x * label_width), int(self.line_1_y * label_height),
                                int(self.line_1_w * label_width), int(self.line_1_h * label_height))
        self.line_2.setGeometry(int(self.line_2_x * label_width), int(self.line_2_y * label_height),
                                int(self.line_2_w * label_width), int(self.line_2_h * label_height))
        self.line_3.setGeometry(int(self.line_3_x * label_width), int(self.line_3_y * label_height),
                                int(self.line_3_w * label_width), int(self.line_3_h * label_height))

        self.text_1.setGeometry(int(self.text_1_x * label_width), int(self.text_1_y * label_height),
                                int(self.text_1_w * label_width), int(self.text_1_h * label_height))
        self.text_2.setGeometry(int(self.text_2_x * label_width), int(self.text_2_y * label_height),
                                int(self.text_2_w * label_width), int(self.text_2_h * label_height))

        self.btn.setGeometry(int(self.btn_x * label_width), int(self.btn_y * label_height),
                             int(self.btn_w * label_width), int(self.btn_h * label_height))
        self.btn_download.setGeometry(int(self.btn_download_x * label_width), int(self.btn_download_y * label_height),
                                      int(self.btn_download_w * label_width), int(self.btn_download_h * label_height))

    def set_background(self):
        palette = QPalette()
        pix = QPixmap("./file/background.png")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

    def on_resize(self, event):
        self.set_background()
        self.update_positions()
        event.accept()

    def start_thread(self):
        # 获取文本框内容
        self.worker_thread.text1 = self.line_1.text()
        self.worker_thread.text2 = self.line_2.text()
        self.worker_thread.text3 = self.line_3.text()
        # 我们使用 moveToThread 方法将 worker_thread 移动到一个新的线程中(即子线程中)
        # 将主线程中text1、text2的值传递到子线程中
        self.worker_thread.moveToThread(self.worker_thread)
        # 启动子线程
        self.worker_thread.start()


    def start_thread2(self):
        # 获取文本框内容
        self.worker_thread2.text1 = self.line_1.text()
        # 我们使用 moveToThread 方法将 worker_thread 移动到一个新的线程中(即子线程中)
        # 将主线程中text1、text2的值传递到子线程中
        self.worker_thread2.moveToThread(self.worker_thread2)
        # 启动子线程
        self.worker_thread2.start()

    def value_change(self, value):
        # 在槽函数中获取子线程传递的结果，并进行处理
        self.text_2.setText(value)

    def value_change2(self, value):
        # 在槽函数中获取子线程传递的结果，并进行处理
        self.text_1.setText(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = mainwindow()
    a.show()
    sys.exit(app.exec_())
