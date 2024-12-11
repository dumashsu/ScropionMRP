# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QDesktopWidget, QTableView, QFrame, QAbstractItemView, QMenu, QMessageBox, QSplitter
import db
import gv


class C_widget(QWidget):
    def __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        self.c_sqlquery = QSqlQuery()
        #視窗置中
        self.setGeometry((QDesktopWidget().availableGeometry().width()-690)/2,(QDesktopWidget().availableGeometry().height()-500)/2,690,500)
        self.setWindowTitle("群組使用者維護作業")
        main_hbox = QHBoxLayout(self)
        main_hbox.setContentsMargins(2, 2, 2, 2)
        main_hbox.setSpacing(2)
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.F_tableviewL())
        main_splitter.addWidget(self.F_tableviewR())
        main_splitter.setStretchFactor(0,1)
        main_splitter.setStretchFactor(1,1)
        main_hbox.addWidget(main_splitter)

        self.show()
    def F_tableviewL(self):
        self.c_sqlquery.exec_("SELECT * FROM s_kindm WHERE kindm_no = '03'")    #取得 類別主檔中使用者群組的 key, 再由key 一一讀出 明細檔中的資料
        if self.c_sqlquery.next():
            self.c_tableviewL = db.F_QTableView(self, "s_kindd", "pk_s_kindm ={}".format(self.c_sqlquery.value(0)), ["2|No.", "3|群組名稱"], [0, 1], [50, 270], "S")
        else:
            self.c_tableviewL = QTableView()
        self.c_tableviewL.setFrameShape(QFrame.Box)
        self.c_tableviewL.setFrameShadow(QFrame.Raised)
        self.c_tableviewL.clicked.connect(self.F_readtableviewR)
        return self.c_tableviewL
    def F_tableviewR(self):
        self.c_tableviewR = QTableView()
        self.c_tableviewR.setFrameShape(QFrame.Box)
        self.c_tableviewR.setFrameShadow(QFrame.Raised)
        temp_model = QStandardItemModel()
        temp_model.setHorizontalHeaderLabels(['使用者ID', '使用者名稱',""])
        self.c_sqlquery.exec_("SELECT * FROM s_userm")
        while self.c_sqlquery.next():
            temp_user_id = QStandardItem(self.c_sqlquery.value(2))
            temp_user_id.setCheckable(True)
            temp_user_nm = QStandardItem(self.c_sqlquery.value(3))
            temp_pk_s_userm = QStandardItem(str(self.c_sqlquery.value(0)))
            temp_model.appendRow([temp_user_id,temp_user_nm,temp_pk_s_userm])
        self.c_tableviewR.setModel(temp_model)
        self.c_tableviewR.verticalHeader().setVisible(False)
        self.c_tableviewR.setColumnWidth(0,120)
        self.c_tableviewR.setColumnWidth(1,200)
        self.c_tableviewR.hideColumn(2)
        self.c_tableviewR.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.c_tableviewR.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.c_tableviewR.setSelectionMode(QAbstractItemView.SingleSelection)
        self.c_tableviewR.setContextMenuPolicy(Qt.CustomContextMenu)
        self.c_tableviewR.customContextMenuRequested.connect(self.F_PopMenu)
        self.c_tableviewR.clicked.connect(self.F_checktableviewR)
        return self.c_tableviewR
    def F_readtableviewR(self,index):
        temp_groupuser = []
        temp_pk_s_kindd = int(self.c_tableviewL.model().index(index.row(), 0).data())  # 取出 c_tableviewL's pk_s_kindd
        self.c_sqlquery.exec_("SELECT * FROM s_groupuserm WHERE pk_s_kindd = {}".format(temp_pk_s_kindd))
        while self.c_sqlquery.next():
            temp_groupuser.append(str(self.c_sqlquery.value(2)))
        for row in range(self.c_tableviewR.model().rowCount()):     #取消所有使用者，再一一設定已建立的使用者群組
            if  self.c_tableviewR.model().item(row,2).text() in temp_groupuser:
                self.c_tableviewR.model().item(row,0).setCheckState(Qt.Checked)
                temp_groupuser.pop(temp_groupuser.index(self.c_tableviewR.model().item(row,2).text()))
            else:
                self.c_tableviewR.model().item(row, 0).setCheckState(Qt.Unchecked)
    def F_checktableviewR(self,index):
        if self.c_tableviewL.selectionModel().hasSelection():
            row = index.row()
            self.c_tableviewR.model().item(row, 0).setCheckState(Qt.Unchecked) if self.c_tableviewR.model().item(row, 0).checkState() else self.c_tableviewR.model().item(row, 0).setCheckState(Qt.Checked)
        else:
            QMessageBox.critical(self,"錯誤!","請先點選左方群組後再勾選使用者")

    def F_PopMenu(self,viewpos):
        viewpos.menu = QMenu()
        viewpos.menu.setStyleSheet(gv.gv_bg_font)
        if self.c_tableviewL.selectionModel().hasSelection():
            pop_save = viewpos.menu.addAction("儲存")
            pop_save.triggered.connect(self.F_pop_save)
            pop_exit = viewpos.menu.addAction("離開")
            pop_exit.triggered.connect(self.F_pop_quit)
            pop_save.setVisible(self.appendstatus)
            viewpos.menu.exec_(QCursor.pos())
    def F_pop_save(self):
        if self.c_sqlquery.exec_("DELETE FROM s_groupuserm WHERE pk_s_kindd ={}".format(int(self.c_tableviewL.model().index(self.c_tableviewL.currentIndex().row(), 0).data()))):
            for row in range(self.c_tableviewR.model().rowCount()):
                if self.c_tableviewR.model().item(row,0).checkState():
                    if not self.c_sqlquery.exec_("INSERT INTO s_groupuserm (pk_s_kindd,pk_s_userm) VALUES ({},{})".format(
                        int(self.c_tableviewL.model().index(self.c_tableviewL.currentIndex().row(), 0).data()),
                        int(self.c_tableviewR.model().item(row,2).text()))):
                        QMessageBox.critical(self,"警告!","更新失敗!!..\n\n"+self.c_sqlquery.lastError().text())
        else:
            QMessageBox.critical(self,"錯誤!","更新失敗!.....\n\n"+self.c_sqlquery.lastError().text())

    def F_pop_quit(self):
        if self.parent() == None:
            self.close()
        else:
            self.parent().close()

# if __name__ == "__main__":
#     import sys
#     app=QApplication(sys.argv)
#     db.F_DBConnect()
#     window = C_widget('AED')
#     sys.exit(app.exec_())