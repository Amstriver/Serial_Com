import serial.tools
import serial.tools.list_ports
from SerialUi import SerialUi
import serial
from PyQt5.QtWidgets import QMessageBox, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QTextCursor, QPen, QColor
from PyQt5.QtCore import QTimer
from qwt import QwtPlot, QwtPlotCurve
import time
import csv

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
        # 初始化曲线和数据  
        self.sensor1_xdata = []  # X轴数据，例如时间戳  
        self.sensor1_ydata = []  # Y轴数据，接收到的传感器值  
        self.sensor1_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图  
        self.sensor1_curve_item.setPen(QPen(QColor("#FF0000"), 2)) # 红色
        self.sensor1_curve_item.setTitle('Sensor1')   
        self.sensor1_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上
        self.sensor_curve.replot()  # 初始重绘

        self.sensor2_xdata = []  # X轴数据，例如时间戳.
        self.sensor2_ydata = []  # Y轴数据，接收到的传感器值.
        self.sensor2_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图.
        self.sensor2_curve_item.setPen(QPen(QColor("#00FF00"), 2)) # 绿色
        self.sensor2_curve_item.setTitle('Sensor2')
        self.sensor2_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上.
        self.sensor_curve.replot()  # 初始重绘.

        self.sensor3_xdata = []  # X轴数据，例如时间戳.
        self.sensor3_ydata = []  # Y轴数据，接收到的传感器值.
        self.sensor3_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图
        self.sensor3_curve_item.setPen(QPen(QColor("#0000FF"), 2)) # 蓝色
        self.sensor3_curve_item.setTitle('Sensor3')
        self.sensor3_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上.
        self.sensor_curve.replot()  # 初始重绘.

        self.sensor4_xdata = []  # X轴数据，例如时间戳.
        self.sensor4_ydata = []  # Y轴数据，接收到的传感器值.
        self.sensor4_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图.
        self.sensor4_curve_item.setPen(QPen(QColor("#FFFF00"), 2)) # 黄色
        self.sensor4_curve_item.setTitle('Sensor4')
        self.sensor4_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上.
        self.sensor_curve.replot()  # 初始重绘.

        self.sensor5_xdata = []  # X轴数据，例如时间戳.
        self.sensor5_ydata = []  # Y轴数据，接收到的传感器值.
        self.sensor5_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图.
        self.sensor5_curve_item.setPen(QPen(QColor("#800080"), 2)) # 紫色
        self.sensor5_curve_item.setTitle('Sensor5')
        self.sensor5_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上.
        self.sensor_curve.replot()  # 初始重绘.

        self.sensor6_xdata = []  # X轴数据，例如时间戳.
        self.sensor6_ydata = []  # Y轴数据，接收到的传感器值.
        self.sensor6_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图.
        self.sensor6_curve_item.setPen(QPen(QColor("#00FFFF"), 2)) # 青色
        self.sensor6_curve_item.setTitle('Sensor6')
        self.sensor6_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上.
        self.sensor_curve.replot()  # 初始重绘.

        self.sensor7_xdata = []  # X轴数据，例如时间戳.
        self.sensor7_ydata = []  # Y轴数据，接收到的传感器值.
        self.sensor7_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图.
        self.sensor7_curve_item.setData(self.sensor7_xdata, self.sensor7_ydata)
        self.sensor7_curve_item.setPen(QPen(QColor("#FFA500"), 2)) # 橙色
        self.sensor7_curve_item.setTitle('Sensor7')
        self.sensor_curve.replot()  # 初始重绘.

        self.sensor8_xdata = []  # X轴数据，例如时间戳.
        self.sensor8_ydata = []  # Y轴数据，接收到的传感器值.
        self.sensor8_curve_item = QwtPlotCurve()  # QwtPlotCurve对象用于绘图.
        self.sensor8_curve_item.setPen(QPen(QColor("#FFC0CB"), 2)) # 粉色
        self.sensor8_curve_item.setTitle('Sensor8')
        self.sensor8_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上.
        self.sensor_curve.replot()  # 初始重绘.

        # 初始化开关
        self.bottom = False

    # 初始化串口
    def init_serial(self) -> None:
        # 串口检测  绑定槽
        self.set_btn_detect.clicked.connect(self.detect_serial)
        # 串口打开/关闭 绑定槽
        self.set_serial_operate.clicked.connect(self.open_serial)
        # 定时器接收数据
        self.serial_receive_timer = QTimer(self)
        self.serial_receive_timer.timeout.connect(self.receive_data)
        # 设置温度设置 绑定槽
        self.set_button.clicked.connect(self.setting_temperature)

        # 设置传感器数据显示 绑定槽
        self.serial_send_max.clicked.connect(self.ser_smax)
        self.serial_send_min.clicked.connect(self.ser_smin)
        self.serial_send_time.clicked.connect(self.ser_stime)
        # 设置开始、关闭采集、清空数据、保存数据一栏 绑定槽
        self.open_collect_button.clicked.connect(self.start_collect)
        self.close_collect_button.clicked.connect(self.stop_collect)
        self.clear_data_button.clicked.connect(self.clear_data)
        self.save_data_button.clicked.connect(self.save_sensor_data)
        # 设置All checkbox 绑定槽
        self.sensor_check_all.clicked.connect(self.all_check_box_changed)
        # 设置清空串口日志 绑定槽
        self.clear_data_view.clicked.connect(self.clear_serial_data)
        # 设置清空发送数据 绑定槽
        self.clear_send_data.clicked.connect(self.clear_send_data_view)
        # 设置查看温度、湿度 绑定槽
        self.check_button_tem.clicked.connect(self.check_temperature)
        self.check_button_hum.clicked.connect(self.check_humidity)


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
            self.serial_send.setText(str(self.sent_count_num))
            self.receive_count_num = 0
            self.serial_receive.setText(str(self.receive_count_num))

    # 发送
    def send_text(self, send_string) -> None:
        if self.serial.isOpen():
            # # 非空字符串
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
                    single_sent_string = send_string.encode('utf-8')

                # 获得发送字节数
                sent_num = self.serial.write(single_sent_string)
                self.sent_count_num += sent_num
                self.serial_send.setText(str(self.sent_count_num))

        else:
            QMessageBox.warning(self, 'Port Warning', '没有可用的串口，请先打开串口！')
            return None

    def setting_temperature(self) -> None:
        # 获取需要发送的字符串
        send_string = self.set_temperature.text()
        if send_string:
            self.send_text(send_string)
        else:
            QMessageBox.warning(self, 'Port Warning', '请输入需要发送的内容！')

    # # 设置传感器数据 显示布局 按键槽
    def ser_smax(self) -> None:
        scale_div = self.sensor_curve.axisScaleDiv(QwtPlot.yLeft)
        restrict_mval = self.serial_max_content.text()
        if restrict_mval:
            self.ymax_restrict = float(restrict_mval)
            self.sensor_curve.setAxisScale(QwtPlot.yLeft, scale_div.lowerBound(), self.ymax_restrict) 
            self.sensor_curve.replot()
        else:
            QMessageBox.warning(self, 'Port Warning', '请先输入数值！')
            return None
    def ser_smin(self) -> None:
        scale_div = self.sensor_curve.axisScaleDiv(QwtPlot.yLeft)
        restrict_mval = self.serial_min_content.text()
        if restrict_mval:
            self.ymin_restrict = float(restrict_mval)
            self.sensor_curve.setAxisScale(QwtPlot.yLeft, self.ymin_restrict, scale_div.upperBound()) 
            self.sensor_curve.replot()
        else:
            QMessageBox.warning(self, 'Port Warning', '请先输入数值！')
            return None
    def ser_stime(self) -> None:
        scale_div = self.sensor_curve.axisScaleDiv(QwtPlot.xBottom)
        restrict_mval = self.serial_time_content.text()
        if restrict_mval:
            self.time_restrict = float(restrict_mval)
            self.sensor_curve.setAxisScale(QwtPlot.xBottom, scale_div.lowerBound(), self.time_restrict)
            self.sensor_curve.replot()
        else:
            QMessageBox.warning(self, 'Port Warning', '请先输入数值！')
            return None

    # 接收数据
    def receive_data(self) -> None:
        try:
            # inWaiting()：返回接收缓存中的字节数
            num = self.serial.in_waiting
        except:
            pass
        else:
        	# 接收缓存中有数据
            if num > 0:
            	# 读取所有的字节数
                self.data = self.serial.read(num)
                receive_num = len(self.data)
                # HEX显示
                if self.sins_cb_hex_receive.isChecked():
                    receive_string = ''
                    for i in range(0, len(self.data)):
                        # {:X}16进制标准输出形式 02是2位对齐 左补0形式
                        receive_string = receive_string + '{:02X}'.format(self.data[i]) + ' '
                    self.receive_log_view.append(receive_string)
                    # 让滚动条随着接收一起移动
                    self.receive_log_view.moveCursor(QTextCursor.End)
                else:
                    self.value = (self.data).decode('UTF-8')
                    self.receive_log_view.insertPlainText(self.value)
                    self.receive_log_view.moveCursor(QTextCursor.End)

                # 更新已接收字节数
                self.receive_count_num += receive_num
                self.serial_receive.setText(str(self.receive_count_num))
                if self.bottom is True:
                    self.update_sensor_data()
            else:
                pass

    # 设置温度、湿度查看一栏
    def check_temperature(self) -> None:
        """查看温度"""
        data_str = self.value.strip()
        parts = data_str.split('/')  # 使用'/'拆分字符串  
        for part in parts:  
            if part.startswith('t'):  # 查找以't'开头的部分  
                temperature = part[1:]  # 提取't'后面的数据  
                self.check_temperature_value.setText(temperature)

    def check_humidity(self) -> None:
        """查看湿度"""
        data_str = self.value.strip() 
        parts = data_str.split('/')  # 使用'/'拆分字符串  
        for part in parts:  
            if part.startswith('h'):  # 查找以'h'开头的部分  
                humidity = part[1:]  # 提取'h'后面的数据  
                self.check_humidity_value.setText(humidity)

    # 设置开始、关闭采集、清空数据、保存数据一栏
    def start_collect(self) -> None:
        """开始采集"""
        self.start_time = time.time()  
        self.open_collect_button.setEnabled(False)
        self.bottom = True
    
    def stop_collect(self) -> None:
        """"关闭采集"""
        self.open_collect_button.setEnabled(True)
        self.bottom = False

    def clear_data(self) -> None:
        """清空数据"""
        num_sensors = 8
        for i in range(1, num_sensors + 1):  
            # 初始化X轴和Y轴数据  
            xdata_var_name = f'sensor{i}_xdata'  
            ydata_var_name = f'sensor{i}_ydata'  
            setattr(self, xdata_var_name, [])  # X轴数据，例如时间戳  
            setattr(self, ydata_var_name, [])  # Y轴数据，接收到的传感器值  
            
            # 设置曲线数据  
            curve_item_var_name = f'sensor{i}_curve_item'  
            curve_item = getattr(self, curve_item_var_name)  # 假设curve_item已经是QwtPlotCurve的实例  
            curve_item.setData([], [])  # 设置曲线数据为空，等待后续更新
        self.sensor_curve.replot()

    def update_sensor_data(self) -> None:  
        # 解析串口数据  
        data_str = self.value.strip()  # 去除首尾空格和换行符  
        if data_str:  # 如果数据不为空  
            sensor_data = data_str.split('/')  # 按'/'分割数据  
            for data in sensor_data:  
                parts = data.split('y')  # 按'y'分割数据和传感器标识  
                if len(parts) == 2:  
                    sensor_id = int(parts[0])  # 传感器ID  
                    sensor_value = float(parts[1])  # 传感器值  
                    # 根据传感器ID更新对应的数据和曲线  
                    self.update_sensor_curve(sensor_id, sensor_value)  
    
    def update_sensor_curve(self, sensor_id: int, sensor_value: float) -> None:  
        current_time = time.time() - self.start_time  # 时间戳  
        # 根据sensor_id选择对应的数据列表和曲线对象进行更新  
        if sensor_id == 1 and self.sensor_check1.isChecked():  
            self.sensor1_xdata.append(current_time)  
            self.sensor1_ydata.append(sensor_value)
            self.sensor_editone.setText(str(sensor_value))  # 回显数据到文本框
            self.sensor1_curve_item.setData(self.sensor1_xdata, self.sensor1_ydata) # 更新曲线数据
        elif sensor_id == 2 and self.sensor_check2.isChecked():  
            self.sensor2_xdata.append(current_time)
            self.sensor2_ydata.append(sensor_value)
            self.sensor_edittwo.setText(str(sensor_value))
            self.sensor2_curve_item.setData(self.sensor2_xdata, self.sensor2_ydata)
        elif sensor_id == 3 and self.sensor_check3.isChecked():
            self.sensor3_xdata.append(current_time)
            self.sensor3_ydata.append(sensor_value)
            self.sensor_editthree.setText(str(sensor_value))
            self.sensor3_curve_item.setData(self.sensor3_xdata, self.sensor3_ydata)
        elif sensor_id == 4 and self.sensor_check4.isChecked():
            self.sensor4_xdata.append(current_time)
            self.sensor4_ydata.append(sensor_value)
            self.sensor_editfour.setText(str(sensor_value))
            self.sensor4_curve_item.setData(self.sensor4_xdata, self.sensor4_ydata)
        elif sensor_id == 5 and self.sensor_check5.isChecked():
            self.sensor5_xdata.append(current_time)
            self.sensor5_ydata.append(sensor_value)
            self.sensor_editfive.setText(str(sensor_value))
            self.sensor5_curve_item.setData(self.sensor5_xdata, self.sensor5_ydata)
        elif sensor_id == 6 and self.sensor_check6.isChecked():
            self.sensor6_xdata.append(current_time)
            self.sensor6_ydata.append(sensor_value)
            self.sensor_editsix.setText(str(sensor_value))
            self.sensor6_curve_item.setData(self.sensor6_xdata, self.sensor6_ydata)
        elif sensor_id == 7 and self.sensor_check7.isChecked():
            self.sensor7_xdata.append(current_time)
            self.sensor7_ydata.append(sensor_value)
            self.sensor_editseven.setText(str(sensor_value))
            self.sensor7_curve_item.attach(self.sensor_curve)  # 将曲线附加到plot上.
        elif sensor_id == 8 and self.sensor_check8.isChecked():
            self.sensor8_xdata.append(current_time)
            self.sensor8_ydata.append(sensor_value)
            self.sensor_editeight.setText(str(sensor_value))
            self.sensor8_curve_item.setData(self.sensor8_xdata, self.sensor8_ydata)
        self.sensor_curve.replot() 

    def save_sensor_data(self) -> None:  
        """保存传感器数据""" 
        # 弹窗选择保存的文件类型和路径  
        file_dialog = QFileDialog(self)  
        file_dialog.setFileMode(QFileDialog.AnyFile)  
        # file_dialog.setNameFilter("CSV Files (*.csv);;Text Files (*.txt);;Excel Files (*.xlsx)")  
        file_dialog.setNameFilter("CSV Files (*.csv)")  
        if file_dialog.exec_():  
            selected_files = file_dialog.selectedFiles()  
            file_path = selected_files[0]  
            file_type = file_dialog.selectedNameFilter()  
            
            # 根据文件类型保存数据  
            if 'CSV' in file_type:  
                self.save_data_as_csv(file_path)  
            # elif 'Text' in file_type:  
            #     self.save_data_as_txt(file_path)  
            # elif 'Excel' in file_type:  
            #     self.save_data_as_xlsx(file_path)  
            else:  
                QMessageBox.warning(self, 'Warning', 'Unsupported file type.')  
                return  
            
            QMessageBox.information(self, 'Information', f'Data saved to {file_path}')  

    def save_data_as_csv(self, file_path: str) -> None:  
        """将数据保存为CSV文件，仅保存被勾选的传感器的数据"""  
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:  
            writer = csv.writer(csvfile)  
            # 修正表头以匹配数据写入的格式  
            csv_list = ['Time', 'sensor1', 'Time', 'sensor2', 'Time', 'sensor3', 'Time', 'sensor4',
                         'Time', 'sensor5', 'Time', 'sensor6', 'Time', 'sensor7', 'Time', 'sensor8']  
            # 写入表头  
            writer.writerow(csv_list)  
            
            # 假设传感器数量和数据长度  
            sensor_count = 8  
            max_length = 0  
            for i in range(1, sensor_count + 1):  
                xdata_var_name = f'sensor{i}_xdata'  
                ydata_var_name = f'sensor{i}_ydata'  
                xdata = getattr(self, xdata_var_name, [])  
                ydata = getattr(self, ydata_var_name, [])  
                max_length = max(max_length, len(xdata), len(ydata))  
            
            # 初始化行数据，长度为表头长度的两倍  
            row_data = [None] * (sensor_count * 2)  
            
            # 遍历数据  
            for t in range(max_length):  
                for i in range(1, sensor_count + 1):  
                    xdata_var_name = f'sensor{i}_xdata'  
                    ydata_var_name = f'sensor{i}_ydata'  
                    xdata = getattr(self, xdata_var_name, [])  
                    ydata = getattr(self, ydata_var_name, [])  
                    
                    check_box_var_name = f'sensor_check{i}'  
                    check_box = getattr(self, check_box_var_name)  
                    
                    # 根据复选框状态和数据长度来设置行数据  
                    if check_box.isChecked() and t < len(xdata) and t < len(ydata):  
                        # 时间戳和传感器数据在行中的位置是交叉的，计算正确的索引  
                        time_index = (i - 1) * 2  
                        sensor_index = time_index + 1  
                        row_data[time_index] = xdata[t]  # 保存时间戳  
                        row_data[sensor_index] = ydata[t]  # 保存传感器数据  
                
                # 写入当前时间戳下所有勾选传感器的数据  
                writer.writerow(row_data)  
                # 重置行数据以供下一轮使用  
                row_data = [None] * (sensor_count * 2)

    def all_check_box_changed(self) -> None:
        """全选或全不选复选框状态改变时调用"""
        if self.sensor_check_all.isChecked():
            self.sensor_check1.setChecked(True)
            self.sensor_check2.setChecked(True)
            self.sensor_check3.setChecked(True)
            self.sensor_check4.setChecked(True)
            self.sensor_check5.setChecked(True)
            self.sensor_check6.setChecked(True)
            self.sensor_check7.setChecked(True)
            self.sensor_check8.setChecked(True)
        else:
            self.sensor_check1.setChecked(False)
            self.sensor_check2.setChecked(False)
            self.sensor_check3.setChecked(False)
            self.sensor_check4.setChecked(False)
            self.sensor_check5.setChecked(False)
            self.sensor_check6.setChecked(False)
            self.sensor_check7.setChecked(False)
            self.sensor_check8.setChecked(False)

    def clear_serial_data(self) -> None:
        """清空串口日志数据"""
        self.receive_log_view.clear()
        self.receive_count_num = 0
        self.serial_receive.setText(str(self.receive_count_num))

    def clear_send_data_view(self) -> None:
        """清空发送数据"""
        self.send_count_num = 0
        self.serial_send.setText(str(self.send_count_num))