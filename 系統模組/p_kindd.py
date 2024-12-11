#-*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QWidget,  QAbstractItemView, QHBoxLayout, QMessageBox, QMenu, QSizePolicy
import db
import gv
import sys 
import udef_object

class C_widget(QWidget):
    def __init__(self,limited, parent = None ):
        QWidget.__init__(self, parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        self.setGeometry(100,100,750,250)
        self.setWindowTitle("類別名稱明細維護")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_hbox = QHBoxLayout(self)
        self.c_tv_s_kindm = db.F_QTableView(self,"s_kindm","",  ["1|類別簡稱", "2|類別全名"], [0], [80, 160],"S" )
        self.c_tv_s_kindm.sortByColumn(1,Qt.AscendingOrder)
        self.c_tv_s_kindm.clicked.connect(self.F_c_tv_s_kindm_filter)
        self.c_tv_s_kindm.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.c_tv_s_kindm.setFixedWidth(250)
        # 啟始時, 右視窗顯示左視窗的第一筆資料
        self.c_tv_s_kindd = db.F_QTableView(self,"s_kindd", "", ["2|代號簡稱", "3|代號全名", "4|自訂欄位", "5|自訂欄位", "6|自訂欄位"], [0,1,4,5,6], [100,200,200,200,200],"S")
        self.c_tv_s_kindd.sortByColumn(2,Qt.AscendingOrder)
        self.c_tv_s_kindd.horizontalHeader().sectionClicked.connect(self.F_c_tv_s_kindd_headersort)
        self.c_tv_s_kindd.model().setFilter("pk_s_kindm = %d" % self.c_tv_s_kindm.model().index(0, 0).data())
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.c_tv_s_kindm)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.c_tv_s_kindd)
        main_hbox.addLayout(hbox1)
        main_hbox.addLayout(hbox2)
        main_hbox.setStretch(0,1)
        main_hbox.setStretch(1,2)
        main_hbox.setContentsMargins(2, 2, 2, 2)
        self.v_pop_status = True            
        self.c_tv_s_kindd.setContextMenuPolicy(Qt.CustomContextMenu)
        self.c_tv_s_kindd.customContextMenuRequested.connect(self.F_PopMenu)           
        self.delegate = udef_object.C_InputDelegate(1, 10, "")
        self.c_tv_s_kindd.setItemDelegateForColumn(2, self.delegate)      

    def F_c_tv_s_kindd_headersort(self,  logicIndex):
        tableview = self.focusWidget()
        number = 0
        #目前只有單筆排序, 為免混亂需先清除不同欄位的排序符號, 但若同一欄位則跳過不處理
        #不知如何判別欄位數, 利用超出欄位時回 headerdata 回傳為數字
        while not isinstance(tableview.model().headerData(number,Qt.Horizontal,0), int):
            headerdata = tableview.model().headerData(number,Qt.Horizontal,0) 
            if ("↓" in headerdata or "↑" in headerdata) and number != logicIndex:
                tableview.model().setHeaderData(number,Qt.Horizontal,(headerdata[0:-1]))
            number+=1            
        headerdata = tableview.model().headerData(logicIndex,Qt.Horizontal,0) 
        if "↓" in headerdata:
            tableview.model().setHeaderData(logicIndex,Qt.Horizontal,(headerdata[0:-1]+"↑")) 
            tableview.sortByColumn(logicIndex,Qt.DescendingOrder)
        elif "↑" in headerdata:
            tableview.model().setHeaderData(logicIndex,Qt.Horizontal,(headerdata[0:-1]))                 
            tableview.sortByColumn(0,Qt.AscendingOrder)
        else:
            tableview.model().setHeaderData(logicIndex,Qt.Horizontal,(headerdata+"↓")) 
            tableview.sortByColumn(logicIndex,Qt.AscendingOrder)
        #self.c_tv_s_kindd.sortByColumn(3,Qt.DescendingOrder)
        #↑↓
    #傳入操作時的 pos , 回傳位置以便 popmenu, 也可使用 v_viewpos 來代替 self.c_tv_s_kindd
    def F_PopMenu(self, v_viewpos):                
        self.c_tv_s_kindd.menu = QMenu()       
        if self.v_pop_status:
            pop_append = self.c_tv_s_kindd.menu.addAction("新增")
            pop_append.triggered.connect(self.F_pop_append)
            pop_edit = self.c_tv_s_kindd.menu.addAction("修改")
            pop_edit.triggered.connect(self.F_pop_edit)
            pop_delete = self.c_tv_s_kindd.menu.addAction("刪除")
            pop_delete.triggered.connect(self.F_pop_delete)
            self.c_tv_s_kindd.menu.addSeparator()         
            pop_quit = self.c_tv_s_kindd.menu.addAction("離開")
            pop_quit.triggered.connect(self.F_pop_quit)
            pop_append.setVisible(self.appendstatus)
            pop_edit.setVisible(self.editstatus)
            pop_delete.setVisible(self.deletestatus)
        else:
            pop_save = self.c_tv_s_kindd.menu.addAction("儲存")
            pop_save.triggered.connect(self.F_pop_save)            
            pop_quit = self.c_tv_s_kindd.menu.addAction("放棄")
            pop_quit.triggered.connect(self.F_pop_quit)            
            
        self.c_tv_s_kindd.menu.exec_(QCursor.pos())                
    def F_pop_append(self):
        self.v_pop_status = False
        rowNum = self.c_tv_s_kindd.model().rowCount()
        self.c_tv_s_kindd.model().insertRow(rowNum)
        #先取 Left 的PKKey
        LrowNum = self.c_tv_s_kindm.currentIndex().row()
        #依Left的 row 取出該 Row's PK 值, 將值寫入 Right 的 FK
        self.c_tv_s_kindd.model().setData(self.c_tv_s_kindd.model().index(rowNum,1),self.c_tv_s_kindm.model().index(LrowNum,0).data())
        self.c_tv_s_kindd.setEditTriggers(QAbstractItemView.DoubleClicked)                 
    def F_pop_edit(self):
        self.v_pop_status = False
        self.c_tv_s_kindd.setEditTriggers(QAbstractItemView.DoubleClicked)            
    def F_pop_delete(self):
        self.v_pop_status = False
        select_row = self.c_tv_s_kindd.currentIndex().row()
        self.c_tv_s_kindd.model().removeRow(select_row)
        self.F_pop_message("是否刪除? ")    
    def F_pop_save(self):
        self.F_pop_message("是否變更? ")        
    def F_pop_quit(self):
        if self.v_pop_status:
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
        else:
            self.c_tv_s_kindd.model().revertAll()            
            self.c_tv_s_kindd.setEditTriggers(QAbstractItemView.NoEditTriggers)            
            self.v_pop_status = True            
    def F_pop_message(self, msg_txt):
        QM_replay = QMessageBox.question(self, "訊息!!!", msg_txt, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if QM_replay == QMessageBox.Yes:
            if not self.c_tv_s_kindd.model().submitAll():
                QMessageBox.critical(self, "錯誤!!", "儲存失敗.\n\n"+self.c_tv_s_kindd.model().lastError().text())
                self.c_tv_s_kindd.model().revertAll()
        else:
            self.c_tv_s_kindd.model().revertAll()
        self.c_tv_s_kindd.setEditTriggers(QAbstractItemView.NoEditTriggers)                     
        self.v_pop_status = True
    def F_c_tv_s_kindm_filter(self, indexClicked):
        if self.focusWidget() == self.c_tv_s_kindm:
            self.c_tv_s_kindd.model().setFilter("pk_s_kindm = %d" % self.c_tv_s_kindm.model().index(indexClicked.row(), 0).data())                   
# if __name__=="__main__":
#     app=QApplication(sys.argv)
#     db.F_DBConnect()
#     window=C_widget('AED')
#     window.show()
#     sys.exit(app.exec_())
