from SerialUi import SerialUi
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    
    app = QApplication([])
    
    serialui = SerialUi()
    serialui.show()
    app.exec_()