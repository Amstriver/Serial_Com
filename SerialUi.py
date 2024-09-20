from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QDesktopWidget

class SerialUi(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.__initUi()

    def __initUi(self) -> None:
        grid_layout = QGridLayout()  # 设置网格布局3行3列
        # 添加组件
        grid_layout.addWidget(self.set_serial_setting_groupbox(), 0, 0)
        grid_layout.addWidget(self.set_serial_send(), 1, 0)
        grid_layout.addWidget(self.set_project_web(), 2, 0)
        grid_layout.addLayout(self.set_sensor_curve(), 0, 1)
        grid_layout.addLayout(self.set_operate_grid(), 1, 1)
        grid_layout.addLayout(self.set_serial_status(), 2, 1)
        grid_layout.addLayout(self.set_sensor_setting(), 0, 2)
        grid_layout.addLayout(self.set_check_status(), 1, 2)
        grid_layout.addLayout(self.set_now_time(), 2, 2)
        # 设置布局grid_layout
        self.setLayout(grid_layout)
        # 设置窗口大小
        self.resize(800, 500)
        # 设置窗口图标
        self.setWindowIcon(QIcon("icon.jpg"))
        # 窗口显示在中心
        self.__center()
        # 设置窗口名称
        self.setWindowTitle("智感微辨监测平台")
        # 显示
        self.show()

    def __center(self):
        """
            控制窗口显示在屏幕中心
        """
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())



