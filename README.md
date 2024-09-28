效果展示
=
https://github.com/user-attachments/assets/fae87ce6-8332-4beb-8c8a-53071eb15ea3.mp4

如何使用
-
#安装所需要的库

pip install pyinstaller 

#终端运行

pyinstaller main.spec

串口接收数据要求
-
#数据发送格式

"1yxxx/2yxxx/3yxx/4yxx/5yxx/6yxx/7yxx/8yxx/txxx/hxxx"

格式说明：
1y,2y...代表传感器;
xxx为传感器所测得的数据;
t后面的数据代表温度数据 ---> 查看温度按键;
h后面的数据代表湿度数据 ---> 查看温度按键；
