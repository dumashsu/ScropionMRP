# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/winE/WorklSpace/Eclipse/SMRP2/UI/ui_colorm.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 400)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(10, 35, 786, 346))
        
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.c_frame = QtWidgets.QFrame(self.splitter)
        self.c_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.c_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.c_frame.setObjectName("c_frame")
        self.c_le_color_no_filter = QtWidgets.QLineEdit(self.c_frame)
        self.c_le_color_no_filter.setGeometry(QtCore.QRect(61, 10, 102, 26))
        self.c_le_color_no_filter.setObjectName("c_le_color_no_filter")
        self.c_lb_color_no_filter = QtWidgets.QLabel(self.c_frame)
        self.c_lb_color_no_filter.setGeometry(QtCore.QRect(5, 10, 52, 18))
        self.c_lb_color_no_filter.setObjectName("c_lb_color_no_filter")
        self.c_lb_color_nm_filter = QtWidgets.QLabel(self.c_frame)
        self.c_lb_color_nm_filter.setGeometry(QtCore.QRect(167, 10, 52, 18))
        self.c_lb_color_nm_filter.setObjectName("c_lb_color_nm_filter")
        self.c_le_color_nm_filter = QtWidgets.QLineEdit(self.c_frame)
        self.c_le_color_nm_filter.setGeometry(QtCore.QRect(223, 10, 102, 26))
        self.c_le_color_nm_filter.setObjectName("c_le_color_nm_filter")
        self.c_tv_color = QtWidgets.QTableView(self.splitter)
        self.c_tv_color.setObjectName("c_tv_color")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.c_lb_color_no_filter.setText(_translate("Form", "顏色代號:"))
        self.c_lb_color_nm_filter.setText(_translate("Form", "顏色名稱:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

