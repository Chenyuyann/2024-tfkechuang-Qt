import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from Ui_detect1 import Ui_MainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MyMainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 获取 graphicsView 的大小
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()

        # 创建 Matplotlib 图形和画布，设置画布大小与 graphicsView 相同
        self.figure = Figure(figsize=(width / 16, height / 6))
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # 创建一个新的场景并将画布添加到其中
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.canvas)

        # 将场景添加到graphicsView组件中
        self.ui.graphicsView.setScene(self.scene)

        # 初始化x和y数据列表
        self.x_data = []
        self.y_data = []

        # 设置x、y轴范围：
        self.axes.set_xlim(0, 30)
        self.axes.set_ylim(60, 100)

        # 设置x、y轴标签
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Heart Rate')

        # 定时器用于定时更新图形
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)

        # 按钮点击连接到槽函数
        self.ui.detectButton.clicked.connect(self.start_plot)
        self.ui.stopButton.clicked.connect(self.stop_plot)

        # 是否正在绘制标志
        self.plotting = False
        self.scroll_index = 0

        # 创建 QMediaPlayer 和 QVideoWidget
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        # 添加视频窗口到 OpenGLWidget
        self.ui.openGLWidget.setLayout(QtWidgets.QVBoxLayout())
        self.ui.openGLWidget.layout().addWidget(self.video_widget)

        # 设置按钮点击连接到槽函数
        self.ui.startButton.clicked.connect(self.start_video)
        self.ui.stopButton.clicked.connect(self.stop_video)

    def start_plot(self):
        # 启动定时器，每秒更新一次图形
        self.plotting = True
        self.timer.start(1000)

    def stop_plot(self):
        # 停止定时器
        self.plotting = False
        self.timer.stop()

    def update_plot(self):
        # 生成随机数并更新数据列表
        random_num = random.uniform(60, 100)
        self.x_data.append(len(self.x_data))
        self.y_data.append(random_num)

        # 绘制图形
        self.axes.clear()
        self.axes.plot(self.x_data, self.y_data, 'r-')
        # 画出实心点：
        self.axes.plot(self.x_data, self.y_data, 'ro')

        # 设置x、y轴范围：
        self.axes.set_xlim(0, 30)
        self.axes.set_ylim(60, 100)
        # 设置x、y轴标签
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Heart Rate')
        # 标记y值，且不消失：
        for i in range(len(self.x_data)):
            self.axes.text(i, self.y_data[i], '%d' % self.y_data[i], ha='center', va='bottom', fontsize=10)

        # 控制横向滚动
        self.scroll_index += 1
        if self.scroll_index > 20:
            self.axes.set_xlim(self.scroll_index - 20, self.scroll_index + 10)
        else:
            self.axes.set_xlim(0, 30)

        self.axes.autoscale_view()  # 自适应视图范围
        self.canvas.draw()

    def start_video(self):
        file_path = "./video.mp4"
        media_content = QMediaContent(QtCore.QUrl.fromLocalFile(file_path))
        self.media_player.setMedia(media_content)

        # 播放视频
        self.media_player.play()

    def stop_video(self):
        # 暂停视频
        self.media_player.pause()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
