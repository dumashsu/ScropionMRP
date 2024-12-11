# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/E:/WorklSpace/Eclipse/SMRP2/UI/UI_Vendorm.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import db

db.
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")

        
        self.verticalLayout.addWidget(self.create_filterframe)
        self.main_splitter = QtWidgets.QSplitter(Form)
        self.main_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.main_splitter.setObjectName("main_splitter")
        self.c_tableView_vendrom = QtWidgets.QTableView(self.main_splitter)
        self.c_tableView_vendrom.setObjectName("c_tableView_vendrom")
        self.splitter_center = QtWidgets.QSplitter(self.main_splitter)
        self.splitter_center.setOrientation(QtCore.Qt.Vertical)
        self.splitter_center.setObjectName("splitter_center")
        
        


        self.verticalLayout.addWidget(self.main_splitter)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 12)
        self.verticalLayoutWidget.raise_()
        self.create_mainframe.raise_()
        self.c_tableView_vendord.raise_()
        self.v_tableView_vendors.raise_()
        self.create_filterframe.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.c_le_no, self.c_le_nm)
        Form.setTabOrder(self.c_le_nm, self.c_le_f_nm)
        Form.setTabOrder(self.c_le_f_nm, self.c_le_uni_no)
        Form.setTabOrder(self.c_le_uni_no, self.c_cbb_type)
        Form.setTabOrder(self.c_cbb_type, self.c_cbb_kind)
        Form.setTabOrder(self.c_cbb_kind, self.c_cbb_purchasepolicy)
        Form.setTabOrder(self.c_cbb_purchasepolicy, self.c_cbb_tradeticket)
        Form.setTabOrder(self.c_cbb_tradeticket, self.c_le_ticketrate)
        Form.setTabOrder(self.c_le_ticketrate, self.c_cbb_taxsource)
        Form.setTabOrder(self.c_cbb_taxsource, self.c_le_taxrate)
        Form.setTabOrder(self.c_le_taxrate, self.c_le_deductrate)
        Form.setTabOrder(self.c_le_deductrate, self.c_cbb_payment)
        Form.setTabOrder(self.c_cbb_payment, self.c_le_payday)
        Form.setTabOrder(self.c_le_payday, self.c_cbb_coin)
        Form.setTabOrder(self.c_cbb_coin, self.c_le_manager)
        Form.setTabOrder(self.c_le_manager, self.c_le_expirydate)
        Form.setTabOrder(self.c_le_expirydate, self.c_te_address)
        Form.setTabOrder(self.c_te_address, self.c_pb_append)
        Form.setTabOrder(self.c_pb_append, self.c_pb_edit)
        Form.setTabOrder(self.c_pb_edit, self.c_pb_delete)
        Form.setTabOrder(self.c_pb_delete, self.c_pb_save)
        Form.setTabOrder(self.c_pb_save, self.c_pb_quit)
        Form.setTabOrder(self.c_pb_quit, self.c_le_no_filter)
        Form.setTabOrder(self.c_le_no_filter, self.c_le_nm_filter)
        Form.setTabOrder(self.c_le_nm_filter, self.c_tableView_vendord)
        Form.setTabOrder(self.c_tableView_vendord, self.v_tableView_vendors)
        Form.setTabOrder(self.v_tableView_vendors, self.c_le_modify_user)
        Form.setTabOrder(self.c_le_modify_user, self.c_le_modify_dt)
        Form.setTabOrder(self.c_le_modify_dt, self.c_tableView_vendrom)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.c_lb_no_filter.setText(_translate("Form", "供應商編號:"))
        self.c_lb_nm_filter.setText(_translate("Form", "簡稱:"))
        self.c_lb_no.setText(_translate("Form", "供應商編號:"))
        self.c_lb_nm.setText(_translate("Form", "簡稱:"))
        self.c_lb_f_nm.setText(_translate("Form", "全名:"))
        self.c_lb_uni_no.setText(_translate("Form", "統一編號:"))
        self.c_lb_type.setText(_translate("Form", "類別:"))
        self.c_cbb_type.setItemText(0, _translate("Form", "A.皮類"))
        self.c_lb_kind.setText(_translate("Form", "性質:"))
        self.c_cbb_kind.setItemText(0, _translate("Form", "1.內銷"))
        self.c_lb_purchasepolicy.setText(_translate("Form", "採購政策:"))
        self.c_cbb_purchasepolicy.setItemText(0, _translate("Form", "1.當地購"))
        self.c_lb_tradeticket.setText(_translate("Form", "交易票據:"))
        self.c_cbb_tradeticket.setItemText(0, _translate("Form", "1.開票"))
        self.c_lb_ticketrate.setText(_translate("Form", "票據比率:"))
        self.c_lb_taxsource.setText(_translate("Form", "稅金來源:"))
        self.c_cbb_taxsource.setItemText(0, _translate("Form", "1.票面金額"))
        self.c_lb_taxrate.setText(_translate("Form", "稅金比率:"))
        self.c_lb_deductrate.setText(_translate("Form", "扣款比率:"))
        self.c_cbb_payment.setItemText(0, _translate("Form", "1.月結30天"))
        self.c_lb_payment.setText(_translate("Form", "交易方式:"))
        self.c_lb_payday.setText(_translate("Form", "付款天數:"))
        self.c_lb_coin.setText(_translate("Form", "交易幣別:"))
        self.c_cbb_coin.setItemText(0, _translate("Form", "U.美金"))
        self.c_lb_manager.setText(_translate("Form", "負責人:"))
        self.c_lb_expirydate.setText(_translate("Form", "停用日期:"))
        self.c_lb_address.setText(_translate("Form", "地址:"))
        self.c_lb_modify_user.setText(_translate("Form", "異動人:"))
        self.c_le_modify_user.setText(_translate("Form", "DumasHsu"))
        self.c_le_modify_dt.setText(_translate("Form", "2016/11/29 13:20:11"))
        self.c_lb_modify_dt.setText(_translate("Form", "異動時間:"))
        self.c_pb_append.setText(_translate("Form", "新增"))
        self.c_pb_edit.setText(_translate("Form", "修改"))
        self.c_pb_delete.setText(_translate("Form", "刪除"))
        self.c_pb_save.setText(_translate("Form", "儲存"))
        self.c_pb_quit.setText(_translate("Form", "離開"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

