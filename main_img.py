import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from Ui_detect2 import Ui_MainWindow
from PyQt5.QtGui import QPixmap

class MyMainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 创建 Matplotlib 图形和画布
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # 设置画布的大小策略为 Expanding，使其自适应父组件的大小
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(size_policy)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.scene.addWidget(self.canvas)

        self.x_data = []
        self.y_data = []
        self.axes.set_xlim(0, 30)
        self.axes.set_ylim(60, 100)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Heart Rate')

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)

        self.ui.detectButton.clicked.connect(self.start_plot)
        self.ui.stopButton.clicked.connect(self.stop_plot)

        self.plotting = False
        self.scroll_index = 0

        # 图片
        self.img_flag = False
        self.image_list = ['img/2.jpg', 'img/3.jpg']
        self.current_img = 0

        self.scene_img = QGraphicsScene()
        self.pixmap_item = QGraphicsPixmapItem()
        self.ui.graphicsView_2.setScene(self.scene_img)
        self.scene_img.addItem(self.pixmap_item)
        
        self.ui.startButton.clicked.connect(self.start_image)
        self.ui.stopButton.clicked.connect(self.stop_image)

    def start_plot(self):
        self.plotting = True
        self.timer.start(1000)

    def stop_plot(self):
        self.plotting = False
        self.timer.stop()

    def update_plot(self):
        random_num = random.uniform(60, 100)
        self.x_data.append(len(self.x_data))
        self.y_data.append(random_num)

        self.axes.clear()
        self.axes.plot(self.x_data, self.y_data, 'r-')
        self.axes.plot(self.x_data, self.y_data, 'ro')

        self.axes.set_xlim(0, 30)
        self.axes.set_ylim(60, 100)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Heart Rate')

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

    def start_image(self):
        self.img_flag = True
        self.timer.start(1000)

    def stop_image(self):
        self.img_flag = False
        self.timer.stop()

    def update_img(self):
        pixmap = QPixmap(self.image_list[self.current_img])
        self.pixmap_item.setPixmap(pixmap)
        self.ui.graphicsView_2.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        
        self.pixmap_item.setPos((self.ui.graphicsView_2.width() - pixmap.width()) / 2,
                                (self.ui.graphicsView_2.height() - pixmap.height()) / 2)
        
        self.current_img = (self.current_img + 1) % len(self.image_list)

    def update(self):
        if self.plotting:
            self.update_plot()
        if self.img_flag:
            self.update_img()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
