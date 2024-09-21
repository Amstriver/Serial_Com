from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QDesktopWidget, QGroupBox, QFormLayout \
    , QPushButton, QComboBox

class SerialUi(QWidget):
    """_summary_

    Args:
        None
    """
    def __init__(self) -> None:
        super().__init__()

        self.__initUi()

    # 初始化UI界面
    def __initUi(self) -> None:
        grid_layout = QGridLayout()  # 设置网格布局3行3列
        # 添加组件
        grid_layout.addWidget(self.set_serial_setting_groupbox(), 0, 0)
        # grid_layout.addWidget(self.set_serial_send(), 1, 0)
        # grid_layout.addWidget(self.set_project_web(), 2, 0)
        # grid_layout.addLayout(self.set_sensor_curve(), 0, 1)
        # grid_layout.addLayout(self.set_operate_grid(), 1, 1)
        # grid_layout.addLayout(self.set_serial_status(), 2, 1)
        # grid_layout.addLayout(self.set_sensor_setting(), 0, 2)
        # grid_layout.addLayout(self.set_check_status(), 1, 2)
        # grid_layout.addLayout(self.set_now_time(), 2, 2)
        # 设置布局grid_layout
        self.setLayout(grid_layout)
        # 设置窗口大小
        self.resize(1500, 1000)
        # 设置窗口图标
        self.setWindowIcon(QIcon("./icon/window_gas.png"))
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
    
    # 串口设置区
    def set_serial_setting_groupbox(self) -> QGroupBox:
        # 设置一个 串口设置 分组框
        serial_setting_gb = QGroupBox('串口设置')
        # 创建 串口设置 分组框内的布局管理器
        serial_setting_formlayout = QFormLayout()
        
        # 检测串口 按钮  创建一个按钮
        self.set_btn_detect = QPushButton('检测串口')
        serial_setting_formlayout.addRow('串口选择  ', self.set_btn_detect)
        
        # 选择串口 下拉菜单  创建一个下拉列表
        self.set_cb_choose = QComboBox(serial_setting_gb)
        # 添加一个下拉列表 由于没有标签 直接省略即可
        serial_setting_formlayout.addRow(self.set_cb_choose)
        
        # 波特率 下拉菜单
        self.set_baud_rate = QComboBox(serial_setting_gb)
        self.set_baud_rate.addItems(['100', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
                            '38400', '56000', '57600', '115200', '128000', '256000']) 
        serial_setting_formlayout.addRow('波特率  ', self.set_baud_rate)
        
        # 停止位 下拉菜单
        self.set_stop_bit = QComboBox(serial_setting_gb)    
        self.set_stop_bit.addItems(['1', '1.5', '2'])
        serial_setting_formlayout.addRow('停止位  ', self.set_stop_bit)
        
        # 数据位 下拉菜单
        self.set_data_bit = QComboBox(serial_setting_gb)
        self.set_data_bit.addItems(['8', '7', '6', '5'])
        serial_setting_formlayout.addRow('数据位  ', self.set_data_bit)
        
        # 奇偶校验 下拉菜单
        self.set_odd_check = QComboBox(serial_setting_gb)
        self.set_odd_check.addItems(['None', 'Odd', 'Even'])
        serial_setting_formlayout.addRow('校验位  ', self.set_odd_check)
        
        # 显示栏 下拉菜单
        self.set_display_bar = QComboBox(serial_setting_gb)
        self.set_display_bar.addItems(['whiteblack', 'blackwhite', 'blackgreen'])
        serial_setting_formlayout.addRow('显示颜色  ', self.set_display_bar)
        
        # 串口操作 按钮
        self.set_serial_operate = QPushButton('打开串口')
        self.set_serial_operate.setIcon(QIcon('./icon/serial_down.png'))
        self.setEnabled(False)
        serial_setting_formlayout.addRow('串口操作  ', self.set_serial_operate)
        
        # 设置控件的间隔距离
        serial_setting_formlayout.setSpacing(12)
        # 设置分组框的布局格式
        serial_setting_gb.setLayout(serial_setting_formlayout)
        
        return serial_setting_gb

        
        