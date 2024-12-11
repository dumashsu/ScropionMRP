#-*- coding: utf-8 -*-
'''
類別名稱維護(s_kindm)
代號 '00,01,02,03' 內定使用禁止刪除
    00.廠別代號
    01.部門
    02.類別名稱明細
    03.群組名稱
'''

#from PyQt5.QtCore import Qt
#from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView,  \
                            QAbstractItemView, QPushButton , QHBoxLayout,  \
                            QSpacerItem, QSizePolicy, QMessageBox
import db
import gv
import sys 

class C_tableview(QTableView):      
    def __init__(self, limited, parent = None):
        QWidget.__init__( self , parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        self.setGeometry(300,300,550,250)
        self.setWindowTitle("類別名稱維護")

        self.pB_append= QPushButton('新增')
        self.pB_append.clicked.connect(self.pB_append_Clicked)
        self.pB_edit = QPushButton('修改')
        self.pB_edit.clicked.connect(self.pB_edit_Clicked)
        self.pB_delete = QPushButton('刪除') 
        self.pB_delete.clicked.connect(self.pB_delete_Clicked)
        
        self.pB_save = QPushButton('儲存')
        self.pB_save.clicked.connect(self.pB_save_Clicked)        
        self.pB_quit = QPushButton('離開')
        self.pB_quit.clicked.connect(self.pB_quit_Clicked)
        self.pB_save.setVisible(False)
        self.vbox=QVBoxLayout()
        self.vbox.addWidget(self.pB_append)
        self.vbox.addWidget(self.pB_edit)
        self.vbox.addWidget(self.pB_delete)
        self.vbox.addItem(QSpacerItem(100, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.vbox.addWidget(self.pB_save)
        self.vbox.addWidget(self.pB_quit) 
               
        self.hbox = QHBoxLayout(self)
        #self.view = C_QTableView()
        self.view = db.F_QTableView(self,"s_kindm","",["1|類別代號","2|代號名稱"],[0],[80,300],"S")
        self.hbox.addWidget(self.view)
        self.hbox.addLayout(self.vbox)
        self.modify_button(False)
        self.show()
    def pB_append_Clicked(self):
        self.modify_button(True)
        rowNum = self.view.model().rowCount()
        self.view.model().insertRow(rowNum)
        #self.view.model().setData(self.view.model().index(rowNum,1),1)          
        #self.modify_button(True)
        
    def pB_edit_Clicked(self):
        select_row = self.view.currentIndex().row()
        self.view.model().removeRow(select_row)
        if self.view.model().index(select_row,1).data() in '00,01,02,03':   #
            QMessageBox.critical(self,"錯誤!","系統資料用，不可修改")
        else:
            self.modify_button(True)
        
    def pB_delete_Clicked(self):
        select_row = self.view.currentIndex().row()
        self.view.model().removeRow(select_row)
        if self.view.model().index(select_row,1).data() in '00,01,02,03':   #
            QMessageBox.critical(self,"錯誤!","系統資料用，禁止刪除")
        else:
            self.answer_Message("是否刪除? ")
        
    def pB_save_Clicked(self):
        self.answer_Message("是否變更? ")
    def pB_quit_Clicked(self):
        
        if self.pB_save.isVisible():            
            self.view.model().revertAll()
        else:
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
        self.modify_button(False)
    
    def answer_Message(self, msg_txt):
        QM_replay = QMessageBox.question(self, "訊息!!!", msg_txt, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if QM_replay == QMessageBox.Yes:
            if not self.view.model().submitAll():
                QMessageBox.warning(self, "錯誤!!", "儲存失敗.\n\n"+self.view.model().lastError().text())
                self.view.model().revertAll()
        else:
            self.view.model().revertAll()
        self.modify_button(False)                        
        
    def modify_button(self, turn_status):
        if turn_status:
            self.pB_append.setVisible(False)
            self.pB_edit.setVisible(False)
            self.pB_delete.setVisible(False)
            self.pB_save.setVisible(True)                
            self.pB_quit.setVisible(True)        
            self.pB_quit.setText('放棄')            
            self.view.setEditTriggers(QAbstractItemView.DoubleClicked)            
        else:
            self.pB_append.setVisible(self.appendstatus)
            self.pB_edit.setVisible(self.editstatus)
            self.pB_delete.setVisible(self.deletestatus)
            self.pB_save.setVisible(False)        
            #self.pB_quit.setVisible(False)                 
            self.pB_quit.setText('離開')            
            self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)                        
        #return True
    def buttonClicked(self):
        if self.pB_append.isVisible():
            self.pB_append.setVisible(False)
        else:
            self.pB_append.setVisible(True)
    # 檢查有無系統必需使用的資料,若無自動新增            

             
if __name__=="__main__":
    app=QApplication(sys.argv)
    db.F_DBConnect()
    w=C_tableview('AED')
    sys.exit(app.exec_())
