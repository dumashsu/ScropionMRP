# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt, QCursor, QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox, QHBoxLayout, QTableView, QTabWidget, QMenu, QFrame, QAbstractItemView, QSplitter
import db
import gv
import sys


class  C_widget(QWidget):
    def  __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        self.c_sqlquery = QSqlQuery()
        #視窗置中
        self.setGeometry((QDesktopWidget().availableGeometry().width()-830)/2,(QDesktopWidget().availableGeometry().height()-380)/2,830,380)
        self.setWindowTitle("使用者權限作業")
        main_hbox = QHBoxLayout(self)
        main_hbox.setContentsMargins(2, 2, 2, 2)
        main_hbox.setSpacing(2)
        self.c_tabwidget = QTabWidget()
        self.c_tabwidget.addTab(self.F_tabUser(),"使用者")
        self.c_tabwidget.addTab(self.F_tabGroup(),"群  組")
        self.c_tabwidget.tabBarClicked.connect(self.F_clickedtab)
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.c_tabwidget)
        main_splitter.addWidget(self.F_tableviewR())
        main_splitter.setStretchFactor(0,2)
        main_splitter.setStretchFactor(1,5)
        main_hbox.addWidget(main_splitter)
        self.c_tabUser.selectionModel().setCurrentIndex(self.c_tabUser.model().index(0, 0), QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        #self.c_tabUser.setCurrentIndex(self.c_tabUser.currentIndex())
        self.F_readuserlimited()
        self.show()
    def F_clickedtab(self,index):
        # 換 tag 時將 index 指為 1
        self.c_tabwidget.setCurrentIndex(index)
        if index:   # clicked tabGroup
            self.c_tabGroup.selectionModel().setCurrentIndex(self.c_tabGroup.model().index(0,0), QItemSelectionModel.ClearAndSelect|QItemSelectionModel.Rows)
        else:
            self.c_tabUser.selectionModel().setCurrentIndex(self.c_tabUser.model().index(0, 0), QItemSelectionModel.ClearAndSelect|QItemSelectionModel.Rows)
        self.F_readuserlimited()
    def F_tabUser(self):        # userm
        self.c_tabUser = db.F_QTableView(self,"s_userm","",["2|使用者ID","3|使用者名稱"],[0,1,4,5,6,7,8,9,10],[100,180],"S")
        self.c_tabUser.clicked.connect(self.F_readuserlimited)
        self.c_tabUser.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.c_tabUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.c_tabUser.setSelectionMode(QAbstractItemView.SingleSelection)
        return self.c_tabUser
    def F_tabGroup(self):       # kindm's pk_s_kindm = 03
        self.c_sqlquery.exec_("SELECT * FROM s_kindm WHERE kindm_no = '03'")  # 取得 類別主檔中使用者群組的 key, 再由key 一一讀出 明細檔中的資料
        if self.c_sqlquery.next():
            self.c_tabGroup = db.F_QTableView(self, "s_kindd", "pk_s_kindm ={}".format(self.c_sqlquery.value(0)), ["2|No.", "3|群組名稱"], [0, 1], [40, 180], "S")
        else:
            QMessageBox.critical(self,"錯誤!","無群組資料....")
            self.c_tabGroup = QTableView()
        self.c_tabGroup.clicked.connect(self.F_readuserlimited)
        self.c_tabGroup.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.c_tabGroup.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.c_tabGroup.setSelectionMode(QAbstractItemView.SingleSelection)
        return self.c_tabGroup

    def F_readuserlimited(self):
        # 清空後再一一讀取 userlimitrf
        for row in range(self.c_tableviewR.model().rowCount()):
            for column in range(2,8):
                temp_item = self.c_tableviewR.model().item(row,column )
                if temp_item.isCheckable():         #原先有無勾選框，若有才還原
                    temp_item.setCheckState(Qt.Unchecked)
        self.c_tableviewR.model().setHorizontalHeaderLabels(['主鍵值','程式名稱','□全部','□新增','□修改','□刪除','□查詢','□列印'])

        if self.c_tabwidget.currentIndex() == 0:    # self.c_tabUser
            temp_filter = "pk_s_userm = {}".format(self.c_tabUser.model().index(self.c_tabUser.currentIndex().row(), 0).data())
        else:
            temp_filter = "pk_s_kindd = {}".format(self.c_tabGroup.model().index(self.c_tabGroup.currentIndex().row(), 0).data())
        self.c_sqlquery.exec_("SELECT * FROM s_userlimited WHERE "+temp_filter)
        while self.c_sqlquery.next():
            temp_item = self.c_tableviewR.model().match(self.c_tableviewR.model().index(0, 0), Qt.DisplayRole, str(self.c_sqlquery.value(3)), 1, Qt.MatchFixedString)
            temp_row = temp_item[0].row()
            for column in range(3,8):
                temp_item = self.c_tableviewR.model().item(temp_row, column)
                if self.c_sqlquery.value(column+1) == '1' and temp_item.isCheckable():
                    temp_item.setCheckState(Qt.Checked)
    def F_tableviewR(self):
        self.c_tableviewR = QTableView(self)
        self.c_tableviewR.setFrameShape(QFrame.Box)
        self.c_tableviewR.setFrameShadow(QFrame.Raised)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['主鍵值','程式名稱','□全部','□新增','□修改','□刪除','□查詢','□列印'])
        self.c_sqlquery = QSqlQuery()
        # 暫用 program_nm 寫程式實際用 program_par
        self.c_sqlquery.exec_("SELECT * FROM s_programd WHERE program_par is not NULL")
        while self.c_sqlquery.next():
            limited = self.c_sqlquery.value(6).split("|")           # program_par, 取 第 3 個 list
            if len(limited) < 4:                                    # 理論上程式就會有資料,測程式時會無故加入上此判斷
                limited = 'AED'
            else:
                limited = limited[3]
            item0 = QStandardItem(str(self.c_sqlquery.value(0)))    #pk_s_program
            item1 = QStandardItem(self.c_sqlquery.value(4))         #program_id
            item2 = QStandardItem("")
            item2.setCheckable(True)
            item3 = QStandardItem("")
            item3.setCheckable(True if 'A' in limited else False)
            item4 = QStandardItem("")
            item4.setCheckable(True if 'E' in limited else False)
            item5 = QStandardItem("")
            item5.setCheckable(True if 'D' in limited else False)
            item6 = QStandardItem("")
            item6.setCheckable(True if 'F' in limited else False)
            item7 = QStandardItem("")
            item7.setCheckable(True if 'P' in limited else False)
            model.appendRow([item0,item1,item2,item3,item4,item5,item6,item7])
        model.itemChanged.connect(self.F_itemchanged)
        self.c_tableviewR.setModel(model)
        self.c_tableviewR.verticalHeader().setVisible(False)
        self.c_tableviewR.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.c_tableviewR.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.c_tableviewR.setSelectionMode(QAbstractItemView.SingleSelection)
        self.c_tableviewR.hideColumn(0)
        self.c_tableviewR.setColumnWidth(1, 210)
        for column in range(2,8):
            self.c_tableviewR.setColumnWidth(column, 50)
        self.c_tableviewR.horizontalHeader().sectionClicked.connect(self.F_tabviewRheaderclick)
        self.c_tableviewR.setContextMenuPolicy(Qt.CustomContextMenu)
        self.c_tableviewR.customContextMenuRequested.connect(self.F_PopMenu)
        return self.c_tableviewR
    def F_itemchanged(self,item):
        if item.column() == 2:
            temp_checkstate = Qt.Checked if item.checkState() else Qt.Unchecked
            for column in range(3,8):
                temp_item =self.c_tableviewR.model().item(item.row(),column)
                if temp_item.isCheckable(): temp_item.setCheckState(temp_checkstate)

    def F_tabviewRheaderclick(self,headernum):
        #□ ■
        headername = self.c_tableviewR.model().headerData(headernum, Qt.Horizontal)
        if '□' in headername:
            temp_clickstr = '■'
            temp_checkstate = Qt.Checked
        else:
            temp_clickstr = '□'
            temp_checkstate = Qt.Unchecked
        self.c_tableviewR.model().setHeaderData(headernum, Qt.Horizontal, "{}".format(temp_clickstr) + headername[1:])
        for row in range(self.c_tableviewR.model().rowCount()):
            temp_item =self.c_tableviewR.model().item(row,headernum)
            if temp_item.isCheckable(): temp_item.setCheckState(temp_checkstate)

    def F_PopMenu(self,viewpos):
        viewpos.menu = QMenu()
        viewpos.menu.setStyleSheet(gv.gv_bg_font)
        temp_tabselected = self.c_tabUser.selectionModel().hasSelection() if self.c_tabwidget.currentIndex() == 0 else self.c_tabGroup.selectionModel().hasSelection()

        if temp_tabselected:
            pop_save = viewpos.menu.addAction("儲存")
            pop_save.triggered.connect(self.F_pop_save)
            pop_save.setVisible(self.appendstatus)
        pop_exit = viewpos.menu.addAction("離開")
        pop_exit.triggered.connect(self.F_pop_quit)

        viewpos.menu.exec_(QCursor.pos())
    def F_pop_save(self,index):
        if self.c_tabwidget.currentIndex() == 0:    # self.c_tabUser
            temp_pk_s_userm = self.c_tabUser.model().index(self.c_tabUser.currentIndex().row(), 0).data()
            temp_pk_s_kindd = None
            temp_filter = "pk_s_userm = {}".format(temp_pk_s_userm)
        else:
            temp_pk_s_userm = None
            temp_pk_s_kindd = self.c_tabGroup.model().index(self.c_tabGroup.currentIndex().row(), 0).data()
            temp_filter = "pk_s_kindd = {}".format(temp_pk_s_kindd)
        if self.c_sqlquery.exec_("DELETE FROM s_userlimited WHERE "+temp_filter):
            for row in range(self.c_tableviewR.model().rowCount()):
                if self.c_tableviewR.model().item(row, 3).checkState() or self.c_tableviewR.model().item(row, 4).checkState() or \
                   self.c_tableviewR.model().item(row, 5).checkState() or self.c_tableviewR.model().item(row, 6).checkState() or \
                   self.c_tableviewR.model().item(row, 7).checkState() :
                    sql=("INSERT INTO s_userlimited (pk_s_userm,pk_s_kindd,pk_s_programd,limited_append,limited_edit,limited_delete,limited_find,limited_print) VALUES "
                                                   "(:pk_s_userm,:pk_s_kindd,:pk_s_programd,:limited_append,:limited_edit,:limited_delete,:limited_find,:limited_print)")
                    if self.c_sqlquery.prepare(sql):
                        self.c_sqlquery.bindValue(":pk_s_userm",temp_pk_s_userm)
                        self.c_sqlquery.bindValue(":pk_s_kindd",temp_pk_s_kindd)
                        self.c_sqlquery.bindValue(":pk_s_programd",int(self.c_tableviewR.model().item(row,0).text()))
                        self.c_sqlquery.bindValue(":limited_append", "1" if self.c_tableviewR.model().item(row, 3).checkState() else None )
                        self.c_sqlquery.bindValue(":limited_edit", "1" if self.c_tableviewR.model().item(row, 4).checkState() else None )
                        self.c_sqlquery.bindValue(":limited_delete", "1" if self.c_tableviewR.model().item(row, 5).checkState() else None )
                        self.c_sqlquery.bindValue(":limited_find", "1" if self.c_tableviewR.model().item(row, 6).checkState() else None )
                        self.c_sqlquery.bindValue(":limited_print", "1" if self.c_tableviewR.model().item(row, 7).checkState() else None )
                        self.c_sqlquery.exec_()
                    else:
                        QMessageBox.critical(self, "錯誤!!", "儲存失敗.\n\n" + self.c_sqlquery.lastError().text())

        else:
            QMessageBox.critical(self,"錯誤!","更新失敗!.....\n\n"+self.c_sqlquery.lastError().text())
        #print(int(self.c_tableviewL.model().index(self.c_tableviewL.currentIndex().row(), 0).data()))

    def F_pop_quit(self):
        if self.parent() == None:
            self.close()
        else:
            self.parent().close()
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     db.F_DBConnect()
#     window = C_widget('AED')
#     sys.exit(app.exec_())