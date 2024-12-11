# -*- coding: utf-8 -*-
'''
建立系統使的模組, 系統管理模組需以 9999 建立, 其它則不限
建立後的模組代號需同 s_program(連同 pk 值) 內使用,否則無法產生上下關係的treeview
'''
from PyQt5.QtCore import QDateTime, Qt, QItemSelectionModel
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, \
                            QSizePolicy, QSplitter
import db
import gv
import sys
import udef_object


class C_widget(QWidget):
    def __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        self.setWindowTitle("主模組維護作業")
        self.setGeometry((QDesktopWidget().availableGeometry().width() - 840) / 2,(QDesktopWidget().availableGeometry().height() - 380) / 2, 840, 380)
        main_hbox = QHBoxLayout(self)
        main_hbox.setContentsMargins(2, 2, 2, 2)
        main_hbox.setSpacing(2)
        main_splitter = QSplitter(Qt.Horizontal)
        #TableView
        c_frame1 = QFrame()
        c_frame1.setFrameShape(QFrame.Box)
        c_frame1.setFrameShadow(QFrame.Raised)
        vbox1 = QVBoxLayout(c_frame1)
        self.c_le_tableview_filter = QLineEdit(self)
        self.c_le_tableview_filter.returnPressed.connect(self.tableview_filter)
        #self.c_le_tableview_filter.setGeometry(5, 10, 195, 26)
        self.c_tableview = db.F_QTableView(self,"s_modulem","",  ["2|代號", "3|模組簡稱"], [0,1,4,5,6,7], [60,130],"S")
        self.c_tableview.clicked.connect(self.viewClicked)
        self.c_tableview.sortByColumn(2,Qt.AscendingOrder)
        #self.c_tableview.setGeometry(5, 40, 195, 350)
        vbox1.addWidget(self.c_le_tableview_filter)
        vbox1.addWidget(self.c_tableview)
        vbox1.setContentsMargins(0,0,0,0)
        main_splitter.addWidget(c_frame1)
        #Freeform
        main_splitter.addWidget(self.F_define_form())
        # Button
        main_splitter.addWidget(self.F_PushButton())
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 28)
        main_splitter.setStretchFactor(2, 1)
        main_hbox.addWidget(main_splitter)
        # 新增或修改 的按紐
        self.maintain(False)
        self.update_status = True
        self.maintain_status = False
        # 首次進入則開啟第一筆資料
        if self.c_tableview.model().rowCount() > 0:
            self.c_tableview.selectionModel().setCurrentIndex(self.c_tableview.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
            self.viewClicked(self.c_tableview.model().index(0, 0))
        self.show()
    def tableview_filter(self):
        self.c_tableview.model().setFilter("module_no like '%{}%'".format(self.c_le_tableview_filter.text()))
        self.maintain(False)
        self.c_le_pk_s_modulem.setText("")
        self.c_le_module_seq.setText("")
        self.c_le_module_no.setText("")
        self.c_le_module_s_nm.setText("")
        self.c_le_module_nm.setText("")
        self.c_te_module_memo.setText("")
        if self.c_tableview.model().rowCount() > 0:
            self.c_tableview.selectionModel().setCurrentIndex(self.c_tableview.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
            self.viewClicked(self.c_tableview.model().index(0, 0))

    def viewClicked(self,indexClicked):
        if not self.c_pb_save.isVisible():
            #取 Tableview's 主鍵
            #self.c_sqlquery.exec("SELECT * FROM s_modulem WHERE pk_s_modulem ={}".format(int(self.c_tableview.model().index(indexClicked.row(), 0).data())))
            row = indexClicked.row()
            self.c_le_pk_s_modulem.setText(str(self.c_tableview.model().index(row, 0).data()))
            self.c_le_module_seq.setText("%d" % self.c_tableview.model().index(row, 1).data())
            self.c_le_module_no.setText(self.c_tableview.model().index(row, 2).data())
            self.c_le_module_s_nm.setText(self.c_tableview.model().index(row, 3).data())
            self.c_le_module_nm.setText(self.c_tableview.model().index(row, 4).data())
            self.c_te_module_memo.setText(self.c_tableview.model().index(row, 5).data())
            self.c_le_modify_user.setText(db.F_get_user_nm(self.c_tableview.model().index(row, 6).data()))
            self.c_le_modify_dt.setText(self.c_tableview.model().index(row, 7).data())

    def pb_append(self):
        self.maintain(True)
        self.update_status = True
        #清空橍位
        self.c_le_pk_s_modulem.setText("")
        self.c_le_module_seq.setText("")
        self.c_le_module_no.setText("")
        self.c_le_module_s_nm.setText("")
        self.c_le_module_nm.setText("")
        self.c_te_module_memo.setText("")
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
        self.c_le_module_no.setFocus()
    def pb_edit(self):
        #Tableview空值或和資料區 資料不一時禁止修改/刪除
        chk_tableview_data = self.c_tableview.model().index(self.c_tableview.currentIndex().row(), 0).data()
        if ( chk_tableview_data != None) and (chk_tableview_data == int(self.c_le_pk_s_modulem.text())):
            self.maintain(True)
            self.c_le_modify_user.setText(gv.gv_user)
            self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
            self.c_le_module_no.setFocus()
            self.update_status = False
        else:
            QMessageBox.critical(self, "錯誤!!", "請先選擇左方欲修改或刪除的資料.....\n\n")
    def pb_delete(self):
        #Tableview空值或和資料區 資料不一時禁止修改/刪除
        chk_tableview_data = self.c_tableview.model().index(self.c_tableview.currentIndex().row(), 0).data()
        if ( chk_tableview_data != None) and (chk_tableview_data == int(self.c_le_pk_s_modulem.text())):
            QM_replay = QMessageBox.question(self, "訊息!!!","是否確認刪除?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if QM_replay == QMessageBox.Yes:
                row = self.c_tableview.currentIndex().row()
                self.c_tableview.model().removeRow(row)
                if not self.c_tableview.model().submitAll():
                    QMessageBox.critical(self, "錯誤!!", "刪除失敗.\n\n" + self.view.model().lastError().text())
                    self.c_tableview.model().revertAll()
                else:
                    row -= 1
                    if row < 0 : row =0
                    self.c_tableview.selectionModel().setCurrentIndex(self.c_tableview.model().index(row, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
                    self.viewClicked(self.c_tableview.model().index(row, 0))
        else:
            QMessageBox.critical(self, "錯誤!!", "請先選擇左方欲修改或刪除的資料.....\n\n")
    def pb_save(self):
        if self.update_status:
            row = self.c_tableview.model().rowCount()
            self.c_tableview.model().insertRow(row)
        else:
            row = self.c_tableview.currentIndex().row()
        self.c_tableview.model().setData(self.c_tableview.model().index(row, 1), int(self.c_le_module_seq.text()))
        self.c_tableview.model().setData(self.c_tableview.model().index(row, 2), self.c_le_module_no.text())
        self.c_tableview.model().setData(self.c_tableview.model().index(row, 3), self.c_le_module_s_nm.text())
        self.c_tableview.model().setData(self.c_tableview.model().index(row, 4), self.c_le_module_nm.text())
        self.c_tableview.model().setData(self.c_tableview.model().index(row, 5), self.c_te_module_memo.toPlainText())
        self.c_tableview.model().setData(self.c_tableview.model().index(row, 6), gv.gv_pk_s_userm)
        self.c_tableview.model().setData(self.c_tableview.model().index(row, 7), self.c_le_modify_dt.text())

        if not self.c_tableview.model().submitAll():
            QMessageBox.critical(self, "錯誤!!", "儲存失敗.\n\n" + self.c_tableview.model().lastError().text())
            self.c_tableview.model().revertAll()
        else:
            self.c_tableview.selectionModel().setCurrentIndex(self.c_tableview.model().index(row, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
            self.maintain(False)

    def pb_quit(self):
        if not self.c_pb_save.isVisible():
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
        else:
            if self.c_le_pk_s_modulem.isModified() or \
                    self.c_le_module_seq.isModified() or \
                    self.c_le_module_no.isModified() or \
                    self.c_le_module_s_nm.isModified() or \
                    self.c_le_module_nm.isModified() :
                    #self.c_te_module_memo.isModified():
                QM_replay = QMessageBox.question(self, "訊息!!!", "資料己被更改，是否放棄?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if QM_replay == QMessageBox.Yes:
                    arg = self.c_tableview.selectedIndexes()
                    self.maintain(False)
                    self.viewClicked(arg[0])
            else:
                # 第一次未點選 Tableview 自動選擇 所以 currentIndex 無法取得該值
                arg = self.c_tableview.selectedIndexes()
                if len(arg) > 0:
                    self.viewClicked(arg[0])
                self.maintain(False)

    # def closeEvent(self, QCloseEvent):
    #     QM_replay = QMessageBox.question(self, "訊息!!!", "是否離開？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if QM_replay == QMessageBox.Yes:
    #         QCloseEvent.accept()
    #     else:
    #         QCloseEvent.ignore()
    def maintain(self,modify_mark):

        if modify_mark:
            self.c_pb_append.setVisible(False)
            self.c_pb_edit.setVisible(False)
            self.c_pb_delete.setVisible(False)            
            self.c_pb_save.setVisible(True)
            self.c_pb_quit.setText("放  棄")           
            self.c_le_pk_s_modulem.setReadOnly(False)
            self.c_le_module_seq.setReadOnly(False)
            self.c_le_module_no.setReadOnly(False)
            self.c_le_module_s_nm.setReadOnly(False)
            self.c_le_module_nm.setReadOnly(False)
            self.c_te_module_memo.setReadOnly(False)
            self.c_le_tableview_filter.setEnabled(False)
        else:
            self.c_pb_append.setVisible(self.appendstatus)
            self.c_pb_edit.setVisible(self.editstatus)
            self.c_pb_delete.setVisible(self.deletestatus)
            self.c_pb_save.setVisible(False)
            self.c_pb_quit.setText("離  開")
            self.c_le_pk_s_modulem.setReadOnly(True)
            self.c_le_module_seq.setReadOnly(True)
            self.c_le_module_no.setReadOnly(True)
            self.c_le_module_s_nm.setReadOnly(True)
            self.c_le_module_nm.setReadOnly(True)
            self.c_te_module_memo.setReadOnly(True)
            self.c_le_tableview_filter.setEnabled(True)

    #@property
    def F_define_form(self):
        c_frame = QFrame()
        vbox = QVBoxLayout(c_frame)
        #c_frame.setGeometry(205, 10, 510, 380)
        c_frame.setFrameShape(QFrame.Box)
        c_frame.setFrameShadow(QFrame.Raised)
        c_frame.setLineWidth(1)
        self.c_lb_module_no = QLabel("模組代號:",c_frame)
        self.c_lb_module_no.setGeometry(10, 10, 64, 26)
        self.c_lb_module_seq = QLabel("排序號:",c_frame)
        self.c_lb_module_seq.setGeometry(390, 10, 71, 26)
        self.c_lb_module_s_nm = QLabel("模組簡稱:",c_frame)
        self.c_lb_module_s_nm.setGeometry(10, 40, 64, 26)
        self.c_lb_module_nm = QLabel("模組全名:",c_frame)
        self.c_lb_module_nm.setGeometry(10, 70, 64, 26)
        self.c_lb_module_memo = QLabel("說明:",c_frame)
        self.c_lb_module_memo.setGeometry(40, 100, 64, 26)
        self.c_lb_modify_user = QLabel("異動人:",c_frame)
        self.c_lb_modify_user.setGeometry(25, 340, 61, 26)
        self.c_lb_modify_dt = QLabel("異動時間:",c_frame)
        self.c_lb_modify_dt.setGeometry(295, 340, 65, 26)
        self.c_le_pk_s_modulem = QLineEdit("",c_frame)
        self.c_le_module_no = udef_object.C_QLineEdit(c_frame,"c_le_module_no",4,"",1,self.F_checkdata)
        self.c_le_module_no.setGeometry(75, 10, 41, 26)
        self.c_le_module_seq = udef_object.C_QLineEdit(c_frame,"c_le_module_seq",4,"9999",1,self.F_checkdata)
        self.c_le_module_seq.setGeometry(445, 10, 41, 26)
        self.c_le_module_s_nm = QLineEdit(c_frame)
        self.c_le_module_s_nm.setGeometry(75, 40, 211, 26)
        self.c_le_module_nm = QLineEdit(c_frame)
        self.c_le_module_nm.setGeometry(75, 70, 411, 26)
        self.c_te_module_memo = QTextEdit(c_frame)
        self.c_te_module_memo.setGeometry(75, 100, 420, 235)
        self.c_le_modify_user = QLineEdit(c_frame)
        self.c_le_modify_user.setGeometry(75, 340, 211, 26)
        self.c_le_modify_dt = QLineEdit(c_frame)
        self.c_le_modify_dt.setGeometry(360, 340, 130, 26)
        self.c_le_pk_s_modulem.setVisible(False)
        self.c_le_modify_user.setReadOnly(True)
        self.c_le_modify_dt.setReadOnly(True)

        #TAB 順序
        c_frame.setTabOrder(self.c_le_module_no, self.c_le_module_seq)
        c_frame.setTabOrder(self.c_le_module_seq, self.c_le_module_s_nm)
        c_frame.setTabOrder(self.c_le_module_s_nm, self.c_le_module_nm)
        c_frame.setTabOrder(self.c_le_module_nm, self.c_te_module_memo)
        return c_frame
    def F_PushButton(self):
        c_frame = QFrame()
        vbox = QVBoxLayout(c_frame)
        # PushButtom
        self.c_pb_append = QPushButton("新  增", c_frame)
        self.c_pb_append.setGeometry(725, 70, 65, 26)
        self.c_pb_edit = QPushButton("修  改", c_frame)
        self.c_pb_edit.setGeometry(725, 110, 65, 26)
        self.c_pb_delete = QPushButton("刪  除", c_frame)
        self.c_pb_delete.setGeometry(725, 150, 65, 26)
        self.c_pb_save = QPushButton("儲  存", c_frame)
        self.c_pb_save.setGeometry(725, 325, 65, 26)
        self.c_pb_save.setVisible(False)
        self.c_pb_quit = QPushButton("離  開", c_frame)
        self.c_pb_quit.setGeometry(725, 365, 65, 26)
        # PushButtom
        self.c_pb_append.clicked.connect(self.pb_append)
        self.c_pb_edit.clicked.connect(self.pb_edit)
        self.c_pb_delete.clicked.connect(self.pb_delete)
        self.c_pb_save.clicked.connect(self.pb_save)
        self.c_pb_quit.clicked.connect(self.pb_quit)
        vbox.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        vbox.addWidget(self.c_pb_append)
        vbox.addSpacing(20)
        vbox.addWidget(self.c_pb_edit)
        vbox.addSpacing(20)
        vbox.addWidget(self.c_pb_delete)
        vbox.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addWidget(self.c_pb_save)
        vbox.addSpacing(20)
        vbox.addWidget(self.c_pb_quit)
        return c_frame
    def F_checkdata(self,objectName):    #各欄位需檢查的判斷式寫在這理
        temp_return = False
        if objectName == "c_le_module_seq":
            return False if self.c_le_module_seq.text().isnumeric() else (True,"請輸入數字....")
        elif objectName == "c_le_module_no":
            if len(self.c_le_module_no.text()) == 0:
                self.c_le_module_no.setText(self.c_tableview.model().index(self.c_tableview.currentIndex().row(), 2).data())
                temp_return=(True, "模組編號 不可為空....")
        return temp_return
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     db.F_DBConnect()
#     c_window = C_widget('AED')
#     sys.exit(app.exec_())
