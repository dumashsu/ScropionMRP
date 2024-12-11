# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt, QCursor
from PyQt5.QtCore import QDateTime, QItemSelectionModel
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout
import db
import gv
import sys
import udef_object


class  C_widget(QWidget):
    def  __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        #視窗置中
        self.setGeometry((QDesktopWidget().availableGeometry().width()-800)/2,(QDesktopWidget().availableGeometry().height()-380)/2,800,380)
        self.setWindowTitle("選單資料維護")
        main_hbox = QHBoxLayout()
        main_hbox.setContentsMargins(2, 2, 2, 2)
        main_hbox.setSpacing(2)

        self.setLayout(main_hbox)
        self.show()
        self.F_maintance(False)
    def F_create_mainfream(self):
        pass
    def F_view_mainframe(self):
        pass
    def F_checkdata(self,temp_objectName):
        temp_return = False
        # if temp_objectName == "c_le_user_id":
        #     if len(self.c_le_user_id.text()) == 0:
        #         temp_return=(True, "使用者 ID 不可為空....")
        #     else:
        #         self.c_sqlquery.exec_("SELECT * FROM s_userm WHERE user_id = '{}'".format(self.c_le_user_id.text()))
        #         if self.c_sqlquery.next():                   #  不管新增/修改 資料只有一筆
        #             if self.update_status:
        #                 temp_return = (True, "使用者 ID 已存在，不可重複!")
        #             elif self.c_sqlquery.value(0) != self.c_tableviewL.model().index(self.c_tableviewL.currentIndex().row(), 0).data():
        #                 temp_return = (True, "使用者 ID 已存在，不可重複!!",self.c_tableviewL.model().index(self.c_tableviewL.currentIndex().row(), 2).data())
        return temp_return
    def F_pb_append(self):
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
    def F_pb_edit(self):
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
    def F_pb_delete(self):
        pass
    def F_pb_save(self):
        pass
    def F_pb_quit(self):
        if not self.c_pb_save.isVisible():
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
        else:
            self.F_maintance(False)
            self.F_view_mainframe(self.modifyindex)
    def F_maintance(self,temp_maintance_status):
        if temp_maintance_status:
            self.c_pb_append.setVisible(False)
            self.c_pb_edit.setVisible(False)
            self.c_pb_delete.setVisible(False)
            self.c_pb_save.setVisible(True)

            #self.c_le_brand_no.setReadOnly(False)
            #self.c_le_brand_nm.setReadOnly(False)
            #self.c_le_brand_payday.setReadOnly(False)
            #self.c_te_delivery_address.setReadOnly(False)
            #self.c_te_pack_desc.setReadOnly(False)
            self.c_pb_quit.setText("放  棄")
        else:
            self.c_pb_append.setVisible(self.appendstatus)
            self.c_pb_edit.setVisible(self.editstatus)
            self.c_pb_delete.setVisible(self.deletestatus)
            #self.c_pb_save.setVisible(False)
            #self.c_le_brand_no.setReadOnly(True)
            #self.c_le_brand_nm.setReadOnly(True)
            #self.c_le_brand_payday.setReadOnly(True)
            #self.c_te_delivery_address.setReadOnly(True)
            #self.c_te_pack_desc.setReadOnly(True)
            self.c_pb_quit.setText("離  開")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    db.F_DBConnect()
    window = C_widget("AED")
    sys.exit(app.exec_())


