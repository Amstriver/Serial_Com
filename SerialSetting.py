import serial.tools
import serial.tools.list_ports
from SerialUi import SerialUi
import serial
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

class SerialSetting(SerialUi):
    """
    串口设置类
    """
    def __init__(self) -> None:
        super().__init__()
        # 初始化serial对象
        self.serial = serial.Serial()
        # 初始化串口配置文件
        # self.serial_cfg()
        # 初始化串口 绑定槽
        self.init_serial()

    # 初始化串口
    def init_serial(self) -> None:
        # 串口检测  绑定槽
        self.set_btn_detect.clicked.connect(self.detect_serial)
        # 串口打开/关闭 绑定槽
        self.set_serial_operate.clicked.connect(self.open_serial)
        # 定时器接收数据
        self.serial_receive_timer = QTimer(self)
        # self.serial_receive_timer.timeout.connect(self.receive_data)！

    # 获取端口号
    def get_serial_port(self) -> str:
        """
        获取端口号
        """
        port_name = self.set_cb_choose.currentText()
        com_name = port_name[0:port_name.rfind(': ')]
        return com_name
    
    # 设置串口曲是否可用
    def serial_operate_enable(self, is_enable: bool):
        """
        设置串口是否可用
        :param is_enable: 是否可用
        """
        self.set_cb_choose.setEnabled(is_enable)
        self.set_baud_rate(is_enable)
        self.set_data_bit(is_enable)
        self.set_stop_bit(is_enable)
        self.set_odd_check(is_enable)
        self.set_serial_operate.setEnabled(is_enable)

    # 检测串口
    def detect_serial(self) -> None:
        # 创建一个串口信息字典
        self.serial_info = {}
        # 返回串口信息
        serial_list = list(serial.tools.list_ports.comports())
        # 清空列表的内容
        self.set_cb_choose.clear()
        for port in serial_list:
            # 添加到字典中
            self.serial_info["%s" % port[0]] = "%s" % port[1]
            # 添加到下拉框中
            self.set_cb_choose.addItem(port[0] + ': ' + port[1])
        if len(self.serial_info) == 0:
            self.set_cb_choose.addItem("未检测到串口")
        self.set_serial_operate.setEnabled(True)

    # 打开串口
    def open_serial(self) -> None:
        # 按打开串口按钮时，且串口信息不为空
        if (self.set_serial_operate.text() == "打开串口") and self.serial_info:
            self.serial.port = self.get_serial_port()  # 串口名
            self.serial.baudrate = int(self.set_baud_rate.currentText())  # 波特率
            self.serial.stopbits = int(self.set_stop_bit.currentText())  # 停止位
            self.serial.bytesize = self.set_data_bit.currentText()  # 数据位
            self.serial.parity = self.set_odd_check.currentText()  # 校验位
        # 捕获 串口打开异常
            try:
                self.serial.open()
            except serial.SerialException:
                QMessageBox.critical(self, 'Error', '串口被占用')
                return None
            
            # 打开串口接受定时器 周期2ms
            self.serial_receive_timer.start(2)

            # 判断 串口打开状态
            if self.serial.isOpen():
                self.set_serial_operate.setText("关闭串口")
                self.set_serial_operate.setIcon(QIcon('./icon/serial_open.png'))
                self.serial_operate_enable(False)

        # 按打开串口按钮时，且串口信息为空
        elif (self.set_serial_operate.text() == "打开串口") and (self.set_cb_choose.currentText() == "未检测到串口"):
            QMessageBox.critical(self, 'Warning', '没有可打开的串口')
            return None
        
        # # 按打开串口按钮时，且串口信息不为空
        # elif self.set_serial_operate.text() == "打开串口":
        #     QMessageBox.critical(self, 'Warning', '请先选择串口')
        #     return None
        
        # 按关闭串口按钮
        elif self.set_serial_operate.text() == "关闭串口":
            # 关闭串口接受定时器
            self.serial_receive_timer.stop()
            try:
                self.serial.close()
            except serial.SerialException:
                QMessageBox.critical(self, 'Error', '串口关闭失败')
                return None
            self.set_serial_operate.setText("打开串口")
            self.set_serial_operate.setIcon(QIcon('./icon/serial_close.png'))
            self.serial_operate_enable(True)

            # 更改已发送和已接收字数
            self.sent_count_num = 0
            self.serial_send = QLabel(f"已发送：{self.sent_count_num}")
            self.receive_count_num = 0
            self.serial_receive = QLabel(f"已接收：{self.receive_count_num}")

