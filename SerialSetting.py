import serial.tools
import serial.tools.list_ports
from SerialUi import SerialUi
import serial
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QTextCursor
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
        self.serial_receive_timer.timeout.connect(self.receive_data)
        # 设置串口发送 绑定槽
        self.serial_send_max.clicked.connect(self.send_max)
        self.serial_send_min.clicked.connect(self.send_min)
        self.serial_send_time.clicked.connect(self.send_time)

    # 获取端口号
    def get_serial_port(self) -> str:
        """
        获取端口号
        """
        port_name = self.set_cb_choose.currentText()
        com_name = port_name[0:port_name.rfind(': ')]
        return com_name
    
    # 设置串口曲是否可用
    def ser_operate_enable(self, is_enable: bool):
        """
        设置串口是否可用
        :param is_enable: 是否可用
        """
        self.set_cb_choose.setEnabled(is_enable)
        self.set_baud_rate.setEnabled(is_enable)
        self.set_data_bit.setEnabled(is_enable)
        self.set_stop_bit.setEnabled(is_enable)
        self.set_odd_check.setEnabled(is_enable)

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
            self.serial.bytesize = int(self.set_data_bit.currentText())  # 数据位
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
                self.ser_operate_enable(False)

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
            self.ser_operate_enable(True)

            # 更改已发送和已接收字数
            self.sent_count_num = 0
            self.serial_send = QLabel(f"已发送：{self.sent_count_num}")
            self.receive_count_num = 0
            self.serial_receive = QLabel(f"已接收：{self.receive_count_num}")

    # 发送
    def send_text(self, send_string) -> None:
        if self.serial.isOpen():
            # 非空字符串
            if send_string != '' :
                # 如果勾选了HEX发送 则以HEX发送 String到Int再到Byte
                if self.sins_cb_hex_send.isChecked():
                    # 移除头尾的空格或换行符
                    send_string = send_string.strip()
                    sent_list = []
                    while send_string != '':
                        # 检查是否是16进制 如果不是则抛出异常
                        try:
                            # 将send_string前两个字符以16进制解析成整数
                            num = int(send_string[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'Wrong Data', '请输入十六进制数据，以空格分开！')
                            self.sins_cb_hex_send.setChecked(False)
                            return None
                        else:
                            send_string = send_string[2:].strip()
                            # 将需要发送的字符串保存在sent_list里
                            sent_list.append(num)
                    # 转化为byte
                    single_sent_string = bytes(sent_list)
                # 否则ASCII发送
                else:
                    single_sent_string = (send_string + '\r\n')
                    single_sent_string = single_sent_string.encode('UTF-8')

                # 获得发送字节数
                sent_num = self.serial.write(single_sent_string)
                self.sent_count_num += sent_num
                self.serial_send.setText(str(self.sent_count_num))

        else:
            QMessageBox.warning(self, 'Port Warning', '没有可用的串口，请先打开串口！')
            return None

    def send_max(self):
        # 获取需要发送的字符串
        send_string = self.serial_max_content.text()
        self.send_text(send_string)
    def send_min(self):
        # 获取需要发送的字符串
        send_string = self.serial_min_content.text()
        self.send_text(send_string)
    def send_time(self):
        # 获取需要发送的字符串
        send_string = self.serial_time_content.text()
        self.send_text(send_string)

    # 接收数据
    def receive_data(self) -> None:
        try:
            # inWaiting()：返回接收缓存中的字节数
            num = self.serial.inWaiting()
        except:
            pass
        else:
        	# 接收缓存中有数据
            if num > 0:
            	# 读取所有的字节数
                data = self.serial.read(num)
                receive_num = len(data)
                # HEX显示
                if self.sins_cb_hex_receive.isChecked():
                    receive_string = ''
                    for i in range(0, len(data)):
                        # {:X}16进制标准输出形式 02是2位对齐 左补0形式
                        receive_string = receive_string + '{:02X}'.format(data[i]) + ' '
                    self.receive_log_view.append(receive_string)
                    # 让滚动条随着接收一起移动
                    self.receive_log_view.moveCursor(QTextCursor.End)
                else:
                    self.receive_log_view.insertPlainText(data.decode('UTF-8'))
                    self.receive_log_view.moveCursor(QTextCursor.End)

                # 更新已接收字节数
                self.receive_count_num += receive_num
                self.serial_receive.setText(str(self.receive_count_num))
            else:
                pass