# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QDateTime, QItemSelectionModel
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QLabel, QLineEdit, QTextEdit, QDesktopWidget, \
                            QSizePolicy, QFrame, QSpacerItem, QPushButton, QMessageBox
import db
import gv
import sys
import udef_object


class  C_widget(QWidget):
    def __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        self.c_sqlquery = QSqlQuery()
        #視窗置中
        self.setGeometry((QDesktopWidget().availableGeometry().width()-780)/2,(QDesktopWidget().availableGeometry().height()-320)/2,780,320)
        self.setWindowTitle("品牌資料建立")
        main_vbox = QVBoxLayout()
        main_vbox.setContentsMargins(2, 2, 2, 2)
        main_vbox.setSpacing(2)
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Horizontal)
        self.c_tableview = db.F_QTableView(self,"brandm","",["1|品牌編號","2|品牌名稱"],[0,3,4,5,6,7],[80,150],"S")
        self.c_tableview.clicked.connect(self.F_view_mainframe)
        main_splitter.addWidget(self.c_tableview)
        main_splitter.addWidget(self.F_cerate_mainframe())
        main_splitter.addWidget(self.F_create_button())
        main_splitter.setStretchFactor(0, 2)
        main_splitter.setStretchFactor(1, 6)
        main_splitter.setStretchFactor(2, 1)
        main_vbox.addWidget(self.F_create_filterframe())
        main_vbox.addWidget(main_splitter)
        main_vbox.setStretch(0, 1)
        main_vbox.setStretch(1, 10)
        self.setLayout(main_vbox)
        self.show()
        self.F_maintance(False)
        if self.c_tableview.model().rowCount() > 0:
            self.c_tableview.selectionModel().setCurrentIndex(self.c_tableview.model().index(0,0), QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            self.F_view_mainframe(self.c_tableview.currentIndex())
    def F_view_mainframe(self,indexclicked):
        if self.c_pb_save.isVisible():
            QMessageBox.warning(self,"警告!","資料編輯中，禁止點選!!")
            self.c_tableview.selectionModel().setCurrentIndex(self.modifyindex, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        else:
            row = indexclicked.row()
            self.c_le_brand_no.setText(self.c_tableview.model().index(row, 1).data())
            self.c_le_brand_nm.setText(self.c_tableview.model().index(row, 2).data())
            self.c_le_brand_payday.setText(str(self.c_tableview.model().index(row, 3).data()))
            self.c_te_delivery_address.setText(self.c_tableview.model().index(row, 4).data())
            self.c_te_pack_desc.setText(self.c_tableview.model().index(row, 5).data())
            self.c_le_modify_user.setText(db.F_get_user_nm(self.c_tableview.model().index(row, 6).data()))
            self.c_le_modify_dt.setText(self.c_tableview.model().index(row, 7).data())
            self.modifyindex = self.c_tableview.currentIndex()
    def F_create_filterframe(self):
        temp_frame = QFrame()
        temp_frame.setFont(gv.gv_font)
        temp_frame.setStyleSheet(gv.gv_filter_bg_color)
        filter_hbox = QHBoxLayout(temp_frame)
        c_lb_brand_no_filter = QLabel("品牌編號:")
        c_lb_brand_nm_filter = QLabel("品牌名稱:")
        #c_lb_brand_nm_filter.setFont(gv.gv_font)
        #c_lb_brand_no_filter.setFont(gv.gv_font)
        self.c_le_brand_no_filter = udef_object.C_QLineEdit(temp_frame, "c_le_brand_no_filter", 10, "",0, self.F_checkdata)
        self.c_le_brand_nm_filter = udef_object.C_QLineEdit(temp_frame, "c_le_brand_nm_filter", 30, "",0, self.F_checkdata)
        filter_hbox.addWidget(c_lb_brand_no_filter)
        filter_hbox.addWidget(self.c_le_brand_no_filter)
        filter_hbox.addWidget(c_lb_brand_nm_filter)
        filter_hbox.addWidget(self.c_le_brand_nm_filter)
        filter_hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        filter_hbox.setStretch(1, 2)
        filter_hbox.setStretch(2, 1)
        filter_hbox.setStretch(3, 3)
        filter_hbox.setStretch(4, 8)
        return temp_frame

    def F_cerate_mainframe(self):
        temp_frame = QFrame()
        temp_frame.setFrameShape(QFrame.Box)
        temp_frame.setFrameShadow(QFrame.Raised)
        c_lb_brand_no = QLabel("品牌編號:",temp_frame)
        c_lb_brand_no.setGeometry(15, 15, 64, 24)
        c_lb_brand_nm = QLabel("名稱:",temp_frame)
        c_lb_brand_nm.setGeometry(45, 45, 34, 24)
        c_lb_brand_payday = QLabel("收款天數:",temp_frame)
        c_lb_brand_payday.setGeometry(325, 45, 71, 24)
        c_lb_delivery_address = QLabel("地址:",temp_frame)
        c_lb_delivery_address.setGeometry(45, 75, 34, 24)
        c_lb_pack_desc = QLabel("包裝說明:",temp_frame)
        c_lb_pack_desc.setGeometry(13, 130, 66, 24)
        c_lb_modify_user = QLabel( "異動人:",temp_frame)
        c_lb_modify_user.setGeometry(35, 230, 49, 26)
        c_lb_modify_dt = QLabel("異動時間:",temp_frame)
        c_lb_modify_dt.setGeometry(240, 230, 66, 26)
        self.c_le_brand_no = udef_object.C_QLineEdit(temp_frame, "c_le_brand_no", 10, "",1, self.F_checkdata)
        self.c_le_brand_no.setGeometry(85, 15, 111, 24)
        self.c_le_brand_nm = udef_object.C_QLineEdit(temp_frame, "c_le_brand_nm", 30, "",1, self.F_checkdata)
        self.c_le_brand_nm.setGeometry(85, 45, 174, 24)
        self.c_le_brand_payday = udef_object.C_QLineEdit(temp_frame, "c_le_brand_payday", 3, "999",0, self.F_checkdata)
        self.c_le_brand_payday.setGeometry(400, 45, 36, 24)
        self.c_te_delivery_address = QTextEdit(temp_frame)
        self.c_te_delivery_address.setGeometry(85, 75, 351, 51)
        self.c_te_pack_desc = QTextEdit(temp_frame)
        self.c_te_pack_desc.setGeometry(85, 130, 351, 91)
        self.c_le_modify_user = QLineEdit(temp_frame)
        self.c_le_modify_user.setGeometry(85, 230, 116, 26)
        self.c_le_modify_dt = QLineEdit(temp_frame)
        self.c_le_modify_dt.setGeometry(305, 230, 125, 26)
        self.c_le_modify_dt.setReadOnly(True)
        self.c_le_modify_user.setReadOnly(True)
        temp_frame.setTabOrder(self.c_le_brand_no, self.c_le_brand_nm)
        temp_frame.setTabOrder(self.c_le_brand_nm, self.c_le_brand_payday)
        temp_frame.setTabOrder(self.c_le_brand_payday, self.c_te_delivery_address)
        temp_frame.setTabOrder(self.c_te_delivery_address, self.c_te_pack_desc)
        return temp_frame
    def F_checkdata(self,temp_objectName):
        temp_return = False
        if temp_objectName == "c_le_brand_no":
            if len(self.c_le_brand_no.text()) == 0:
                temp_return = (True, "品牌編號不可為空....")
            else:
                self.c_sqlquery.exec_("SELECT * FROM brandm WHERE brand_no = '{}'".format(self.c_le_brand_no.text()))
                if self.c_sqlquery.next():  # 不管新增/修改 資料只有一筆
                    if self.updatestatus:
                        temp_return = (True, "品牌編號已經存已存在，不可重複!")
                    elif self.c_sqlquery.value(0) != self.c_tableview.model().index(self.c_tableview.currentIndex().row(), 0).data():
                        temp_return = (True, "品牌編號已經存已存在，不可重複!!", self.c_tableview.model().index(self.c_tableview.currentIndex().row(), 1).data())
        elif temp_objectName == "c_le_brand_nm" and len(self.c_le_brand_nm.text()) == 0:
            temp_return = (True, "品牌編號不可為空....", self.c_tableview.model().index(self.c_tableview.currentIndex().row(), 2).data())
        return temp_return
    def F_create_button(self):
        temp_frame = QFrame()
        temp_frame.setFrameShape(QFrame.Box)
        temp_frame.setFrameShadow(QFrame.Raised)
        self.c_pb_append = QPushButton("新  增")
        self.c_pb_edit = QPushButton("修  改")
        self.c_pb_delete = QPushButton("刪  除")
        self.c_pb_save = QPushButton("儲  存")
        self.c_pb_quit = QPushButton("離  開")
        temp_vbox = QVBoxLayout(temp_frame)
        temp_vbox.setContentsMargins(2, 2, 2, 2)
        temp_vbox.setSpacing(2)
        temp_vbox.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        temp_vbox.addWidget(self.c_pb_append)
        temp_vbox.addSpacing(20)
        temp_vbox.addWidget(self.c_pb_edit)
        temp_vbox.addSpacing(20)
        temp_vbox.addWidget(self.c_pb_delete)
        temp_vbox.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        temp_vbox.addWidget(self.c_pb_save)
        temp_vbox.addSpacing(20)
        temp_vbox.addWidget(self.c_pb_quit)
        self.c_pb_append.clicked.connect(self.F_pb_append)
        self.c_pb_edit.clicked.connect(self.F_pb_edit)
        self.c_pb_delete.clicked.connect(self.F_pb_delete)
        self.c_pb_save.clicked.connect(self.F_pb_save)
        self.c_pb_quit.clicked.connect(self.F_pb_quit)
        return temp_frame
    def F_pb_append(self):
        self.F_maintance(True)
        self.updatestatus = True
        self.c_le_brand_no.setFocus()
        self.c_le_brand_no.setText("")
        self.c_le_brand_nm.setText("")
        self.c_le_brand_payday.setText("")
        self.c_te_delivery_address.setText("")
        self.c_te_pack_desc.setText("")
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))

    def F_pb_edit(self):
        self.F_maintance(True)
        self.updatestatus = False
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
        self.c_le_brand_no.setFocus()
        self.c_le_brand_no.selectAll()
    def F_pb_delete(self):
        QM_replay = QMessageBox.question(self, "訊息!!!", "是否確認刪除?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if QM_replay == QMessageBox.Yes:
            row = self.modifyindex.row()
            self.c_tableview.model().removeRow(row)
            if not self.c_tableview.model().submitAll():
                QMessageBox.critical(self, "錯誤!!", "刪除失敗.\n\n" + self.c_tableview.model().lastError().text())
                self.c_tableview.model().revertAll()
            else:
                self.c_tableview.selectionModel().setCurrentIndex(self.c_tableview.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
                self.F_view_mainframe(self.c_tableview.model().index(0, 0))
    def F_pb_save(self):
        if self.updatestatus:
            temp_sql = "INSERT INTO brandm (brand_no,brand_nm,brand_payday,delivery_address,pack_desc,modify_user,modify_dt) VALUES " \
                                    "(:c_le_brand_no,:c_le_brand_nm,:c_le_brand_payday,:c_te_delivery_address,:c_te_pack_desc,:modify_user,:modify_dt)"
        else:
            row = self.modifyindex.row()
            temp_sql = "UPDATE brandm SET "  \
                       "brand_no = :c_le_brand_no," \
                       "brand_nm = :c_le_brand_nm," \
                       "brand_payday = :c_le_brand_payday," \
                       "delivery_address = :c_te_delivery_address,"\
                       "pack_desc = :c_te_pack_desc, "\
                       "modify_user = :modify_user, "\
                       "modify_dt = :modify_dt"\
                       " WHERE pk_brandm = {}".format(int(self.c_tableview.model().index(row,0).data()))
        if self.c_sqlquery.prepare(temp_sql):
            self.c_sqlquery.bindValue(":c_le_brand_no",self.c_le_brand_no.text())
            self.c_sqlquery.bindValue(":c_le_brand_nm",self.c_le_brand_nm.text())
            self.c_sqlquery.bindValue(":c_le_brand_payday",int(self.c_le_brand_payday.text()))
            self.c_sqlquery.bindValue(":c_te_delivery_address",self.c_te_delivery_address.toPlainText())
            self.c_sqlquery.bindValue(":c_te_pack_desc",self.c_te_pack_desc.toPlainText())
            self.c_sqlquery.bindValue(":modify_user",gv.gv_pk_s_userm)
            self.c_sqlquery.bindValue(":modify_dt",self.c_le_modify_dt.text())
            if not self.c_sqlquery.exec_():
                QMessageBox.critical(self, "錯誤!!", "儲存失敗.資料有誤!!.....\n\n" + self.c_sqlquery.lastError().text())
            else:
                # tableview 新增一行
                if self.updatestatus:
                    row = self.c_tableview.model().rowCount()
                    self.c_tableview.model().insertRow(row)
                    self.c_tableview.model().setData(self.c_tableview.model().index(row, 0), self.c_sqlquery.lastInsertId())
                self.c_tableview.model().setData(self.c_tableview.model().index(row, 1), self.c_le_brand_no.text())
                self.c_tableview.model().setData(self.c_tableview.model().index(row, 2), self.c_le_brand_nm.text())
                self.c_tableview.model().setData(self.c_tableview.model().index(row, 3), self.c_le_brand_payday.text())
                self.c_tableview.model().setData(self.c_tableview.model().index(row, 4), self.c_te_delivery_address.toPlainText())
                self.c_tableview.model().setData(self.c_tableview.model().index(row, 5), self.c_te_pack_desc.toPlainText())
                self.c_tableview.model().setData(self.c_tableview.model().index(row, 6), gv.gv_pk_s_userm)
                self.c_tableview.model().setData(self.c_tableview.model().index(row, 7), self.c_le_modify_dt.text())
                # 新增後定位使用,懶得判別新增做用
                temp_index = self.c_tableview.model().match(self.c_tableview.model().index(0, 1), Qt.DisplayRole, self.c_le_brand_no.text(), 1, Qt.MatchFixedString)
                self.c_tableview.selectionModel().setCurrentIndex(temp_index[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        else:
            QMessageBox.critical(self, "錯誤!!", "儲存失敗.資料有誤!.....\n\n" + self.c_sqlquery.lastError().text())
        self.F_maintance(False)
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
            self.c_le_brand_no.setReadOnly(False)
            self.c_le_brand_nm.setReadOnly(False)
            self.c_le_brand_payday.setReadOnly(False)
            self.c_te_delivery_address.setReadOnly(False)
            self.c_te_pack_desc.setReadOnly(False)
            self.c_pb_quit.setText("放  棄")
        else:
            self.c_pb_append.setVisible(self.appendstatus)
            self.c_pb_edit.setVisible(self.editstatus)
            self.c_pb_delete.setVisible(self.deletestatus)
            self.c_pb_save.setVisible(False)
            self.c_le_brand_no.setReadOnly(True)
            self.c_le_brand_nm.setReadOnly(True)
            self.c_le_brand_payday.setReadOnly(True)
            self.c_te_delivery_address.setReadOnly(True)
            self.c_te_pack_desc.setReadOnly(True)
            self.c_pb_quit.setText("離  開")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    db.F_DBConnect()
    window = C_widget("AED")
    sys.exit(app.exec_())
