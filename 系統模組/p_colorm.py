# -*- coding: utf-8 -*-
'''
Created on 2017年2月21日

@author: dumas
'''
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, \
                                                                        QAbstractItemView,QMenu, QLabel, QFrame, QLineEdit, \
                                                                        QSplitter,QMessageBox
from PyQt5.QtSql import QSqlQuery
from PyQt5.Qt import Qt,QCursor
from PyQt5.QtCore import QDateTime, QItemSelectionModel

import udef_object
import sys
import gv
import db

class  C_widget(QWidget):
    def  __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        #視窗置中
        self.setGeometry((QDesktopWidget().availableGeometry().width()-800)/2,(QDesktopWidget().availableGeometry().height()-400)/2,800,400)
        self.setWindowTitle("顏色資料維護")
        self.c_tv_colorm = db.F_QTableView(self,"colorm", "", ["1|顏色代號", "2|中文名稱", "3|英文名稱"], [0,4,5], [100,340,340],"S")
        self.c_tv_colorm.setContextMenuPolicy(Qt.CustomContextMenu)
        self.c_tv_colorm.customContextMenuRequested.connect(self.F_PopMenu)        
        main_vbox = QVBoxLayout(self)
        main_vbox.addWidget(self.F_filterframe())
        main_vbox.addWidget(self.c_tv_colorm)
        main_vbox.setContentsMargins(0, 0,0, 0)
        main_vbox.setStretch(0,1)
        main_vbox.setStretch(1,9)
        self.v_pop_status = True
        self.show()
    def F_filterframe(self):
        c_frame = QFrame()
        c_frame.setStyleSheet(gv.gv_filter_bg_color)
        self.c_le_color_no_filter = udef_object.C_QLineEdit(c_frame,"c_le_color_no_filter",10,"",0,self.F_checkdata)
        self.c_le_color_no_filter.setGeometry(72, 10, 102, 26)
        self.c_le_color_nm_filter = udef_object.C_QLineEdit(c_frame,"c_le_color_nm_filter",20,"",0,self.F_checkdata)
        self.c_le_color_nm_filter.setGeometry(245, 10, 102, 26)               
        c_lb_color_no_filter = QLabel("顏色編號:",c_frame)
        c_lb_color_no_filter.setGeometry(5, 10, 65, 26)
        c_lb_color_nm_filter = QLabel("顏色名稱:",c_frame)
        c_lb_color_nm_filter.setGeometry(180, 10, 65, 26)  
        #self.c_le_color_no_filter.returnPressed.connect(self.F_tv_filter)
        #self.c_le_color_nm_filter.returnPressed.connect(self.F_tv_filter)    
        return c_frame
    def F_mainframe(self):
        return
#     def F_tv_filter(self):        
#         if self.sender().objectName() == 'c_le_color_no':
#             self.c_tv_colorm.model().setFilter("color_no  like '%{}%'".format(self.c_le_color_no_filter.text()))                
#         elif  self.sender().objectName() == 'c_le_color_nm':
#             self.c_tv_colorm.model().setFilter("color_nm like '%{}%'".format(self.c_le_color_nm_filter.text()))
#         else:
#             self.c_tv_colorm.model().setFilter("")
#         return        
    def F_PopMenu(self, v_viewpos):                
        self.c_tv_colorm.menu = QMenu()       
        if self.v_pop_status:
            pop_append = self.c_tv_colorm.menu.addAction("新增")
            pop_append.triggered.connect(self.F_pop_append)
            pop_edit = self.c_tv_colorm.menu.addAction("修改")
            pop_edit.triggered.connect(self.F_pop_edit)
            pop_delete = self.c_tv_colorm.menu.addAction("刪除")
            pop_delete.triggered.connect(self.F_pop_delete)
            self.c_tv_colorm.menu.addSeparator()         
            pop_quit = self.c_tv_colorm.menu.addAction("離開")
            pop_quit.triggered.connect(self.F_pop_quit)
            pop_append.setVisible(self.appendstatus)
            pop_edit.setVisible(self.editstatus)
            pop_delete.setVisible(self.deletestatus)
            self.c_le_color_no_filter.setReadOnly(True)
            self.c_le_color_nm_filter.setReadOnly(True)
        else:
            pop_save = self.c_tv_colorm.menu.addAction("儲存")
            pop_save.triggered.connect(self.F_pop_save)            
            pop_quit = self.c_tv_colorm.menu.addAction("放棄")
            pop_quit.triggered.connect(self.F_pop_quit)            
            self.c_le_color_no_filter.setReadOnly(False)
            self.c_le_color_nm_filter.setReadOnly(False)
        self.c_tv_colorm.menu.exec_(QCursor.pos())                
    def F_pop_append(self):
        self.v_pop_status = False
        rowNum = self.c_tv_colorm.model().rowCount()
        self.c_tv_colorm.model().insertRow(rowNum)
        self.c_tv_colorm.setEditTriggers(QAbstractItemView.DoubleClicked)                
    def F_pop_edit(self):
        self.v_pop_status = False
        self.c_tv_colorm.setEditTriggers(QAbstractItemView.DoubleClicked)            
    def F_pop_delete(self):
        self.v_pop_status = False
        select_row = self.c_tv_colorm.currentIndex().row()
        self.c_tv_colorm.model().removeRow(select_row)
        self.F_pop_msg("是否刪除? ")
    def F_pop_save(self):
        self.F_pop_msg("是否變更? ")
    def F_pop_quit(self):
        if self.v_pop_status:
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
        else:
            self.c_tv_colorm.model().revertAll()            
            self.c_tv_colorm.setEditTriggers(QAbstractItemView.NoEditTriggers)            
            self.v_pop_status = True            
    def F_pop_msg(self, msg_txt):    
        QM_replay = QMessageBox.question(self, "訊息!!!", msg_txt, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if QM_replay == QMessageBox.Yes:
            select_row = self.c_tv_colorm.currentIndex().row()
            self.c_tv_colorm.model().setData(self.c_tv_colorm.model().index(select_row, 4), gv.gv_pk_s_userm)
            self.c_tv_colorm.model().setData(self.c_tv_colorm.model().index(select_row,5), QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
            if not self.c_tv_colorm.model().submitAll():
                QMessageBox.critical(self, "錯誤!!", "儲存失敗.\n\n"+self.c_tv_colorm.model().lastError().text())
                self.c_tv_colorm.model().revertAll()
        else:
            self.c_tv_colorm.model().revertAll()
        self.c_tv_colorm.setEditTriggers(QAbstractItemView.NoEditTriggers)                     
        self.v_pop_status = True
    def F_checkdata(self,temp_objectName):
        temp_return = False
        if temp_objectName == "c_le_color_no_filter":
            self.c_tv_colorm.model().setFilter("color_no  like '%{}%'".format(self.c_le_color_no_filter.text()))                
        elif  temp_objectName == "c_le_color_nm_filter":
            self.c_tv_colorm.model().setFilter("color_nm like '%{}%'".format(self.c_le_color_nm_filter.text()))
        return temp_return
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     db.F_DBConnect()
#     window = C_widget("AED")
#     sys.exit(app.exec_())


