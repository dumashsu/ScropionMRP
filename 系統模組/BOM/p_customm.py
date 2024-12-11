# -*- coding: utf-8 -*-
# p_customm 客戶基本資料維護
#
# 連絡人和明細及品牌如何處理....尚在構思中
from PyQt5.QtCore import Qt, QDateTime, QItemSelectionModel
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QFrame, QDesktopWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, \
                            QSpacerItem, QSizePolicy, QLineEdit, QMessageBox, QComboBox, QAbstractItemView
import db
import gv
import sys
import udef_object


class C_widget(QWidget):
    def __init__(self, limited, parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        #視窗置中
        self.setGeometry((QDesktopWidget().availableGeometry().width()-800)/2,(QDesktopWidget().availableGeometry().height()-610)/2,800,610)
        self.setWindowTitle("品牌客戶資料維護")
        self.c_sqlquery = QSqlQuery()
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(2, 2, 2, 2)
        main_vbox.setSpacing(2)
        main_vbox.addWidget(self.F_create_filterframe())
        main_vbox.addWidget(self.F_buttom_splitter())
        main_vbox.setStretch(0, 1)
        main_vbox.setStretch(1, 14)
        self.show()
        self.F_maintance(False)
        self.pk_customm = 0
        self.v_pop_status = True
        self.updatestatus = True
        if self.c_tableview_customm.model().rowCount() > 0:
            self.c_tableview_customm.selectionModel().setCurrentIndex(self.c_tableview_customm.model().index(0,0), QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            self.F_view_mainframe(self.c_tableview_customm.currentIndex())
    def F_buttom_splitter(self):
        # 下方的總 splitter 內放了 tableview/splitter/功能鍵
        buttom_splitter_h = QSplitter(Qt.Horizontal)
        self.c_tableview_customm = db.F_QTableView(buttom_splitter_h,"customm", \
                                                   "",["1|客戶編號","2|客戶簡稱"], [0,3,4,5,6,7,8,9,10],[80,140],"S")      
        self.c_tableview_customm.setFrameShape(QFrame.Box)
        self.c_tableview_customm.setFrameShadow(QFrame.Raised)
        self.c_tableview_customm.clicked.connect(self.F_view_mainframe)
        # 中間的 splitter 第一個是 freeframe
        splitter_h2v = QSplitter(Qt.Vertical,buttom_splitter_h)
        splitter_h2v.addWidget(self.F_create_mainframe())
        # 中間的 splitter 第二個是 2 個 tableview 放了連絡人及連絡人相關資料
        splitter_h2v2 = QSplitter(Qt.Horizontal,splitter_h2v)
        self.c_tableview_customd = db.F_QTableView(splitter_h2v2,"customd","",["2|連絡人"],[0,1],[160],"S")
        self.c_tableview_customd.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.c_tableview_customd.setContextMenuPolicy(Qt.NoContextMenu)        
        self.c_tableview_customd.customContextMenuRequested.connect(lambda:db.C_PopMenu(self, self.c_tableview_customd,["1|{}".format(self.pk_customm)],"Half"))
        self.c_tableview_customs = db.F_QTableView(splitter_h2v2,"customs","",  ["2|明細資料", "3|資料內容"], [0,1], [100,325],"R",["2|s_kindd|pk_s_kindd|kindd_nm"])
        db.F_Tableview_kindd(self.c_tableview_customs,"02",2)
        self.c_tableview_customs.setContextMenuPolicy(Qt.NoContextMenu)        
        #self.c_tableview_customs.customContextMenuRequested.connect(lambda:db.C_PopMenu(self, self.c_tableview_customs,["1|{}".format(self.pk_customm)],"Half"))
        self.c_tableview_customs.customContextMenuRequested.connect(lambda:db.C_PopMenu(self, self.c_tableview_customs,\
                                                                          ["1|{}".format(self.c_tableview_customd.model().index(self.c_tableview_customd.currentIndex().row(),0).data())],"Half"))
        splitter_h2v2.addWidget(self.c_tableview_customd)
        splitter_h2v2.addWidget(self.c_tableview_customs)
        # 中間的 splitter 第三個是 tableview 放置 客戶的品牌資料
        self.c_tableview_brandm = db.F_QTableView(splitter_h2v,"SELECT pk_brandm,brand_no,brand_nm,delivery_address,pack_desc FROM brandm", \
                                                  "",["1|品牌編號","2|品牌名稱","3|送貨地址","4|包裝方式"],[0],[80,120,160,160],"S")      
        splitter_h2v.addWidget(self.c_tableview_brandm)  
        splitter_h2v.setStretchFactor(0,3)
        splitter_h2v.setStretchFactor(1,4)
        splitter_h2v.setStretchFactor(2,4)
        buttom_splitter_h.addWidget(self.F_create_button())
        return buttom_splitter_h
    def F_create_filterframe(self):
        temp_frame = QFrame()
        temp_frame.setStyleSheet(gv.gv_filter_bg_color)
        #temp_frame.setFont(gv.gv_font)
        c_lb_customm_no_filter = QLabel("客戶編號:",temp_frame)
        c_lb_customm_no_filter.setGeometry(10, 5, 70, 26)
        c_lb_customm_nm_filter = QLabel("簡稱:",temp_frame)
        c_lb_customm_nm_filter.setGeometry(205, 5, 70, 26)
        self.c_le_customm_no_filter = udef_object.C_QLineEdit(temp_frame, "c_le_customm_no_filter", 15, "",0, self.F_checkdata)
        self.c_le_customm_no_filter.setGeometry(75, 5, 101, 26)
        self.c_le_customm_nm_filter = udef_object.C_QLineEdit(temp_frame, "c_le_customm_nm_filter", 20, "",0, self.F_checkdata)
        self.c_le_customm_nm_filter.setGeometry(240, 5, 113, 26)
        return temp_frame
    def F_create_mainframe(self):
        temp_frame = QFrame()
        temp_frame.setFrameShape(QFrame.StyledPanel)
        temp_frame.setFrameShadow(QFrame.Raised)
        c_lb_customm_no = QLabel("客戶編號:",temp_frame)
        c_lb_customm_no.setGeometry(5, 5, 66, 26)
        c_lb_customm_nm = QLabel("客戶簡稱:",temp_frame)
        c_lb_customm_nm.setGeometry(5, 40, 66, 26)
        c_lb_customm_type = QLabel("客戶類別:",temp_frame)
        c_lb_customm_type.setGeometry(295, 40, 66, 26)
        c_lb_customm_f_nm = QLabel("客戶全名:",temp_frame)
        c_lb_customm_f_nm.setGeometry(5, 75, 66, 26)
        c_lb_customm_f_nm_en = QLabel("英文全名:",temp_frame)
        c_lb_customm_f_nm_en.setGeometry(5, 110, 66, 26)
        c_lb_customm_stopdate = QLabel("停用日期:",temp_frame)
        c_lb_customm_stopdate.setGeometry(295, 145, 66, 26)
        c_lb_customm_manager = QLabel("負責人:",temp_frame)
        c_lb_customm_manager.setGeometry(20, 145, 51, 26)
        c_lb_customm_address = QLabel("地址:",temp_frame)
        c_lb_customm_address.setGeometry(35, 175, 51, 26)
        c_lb_modify_user = QLabel("異動人:",temp_frame)
        c_lb_modify_user.setGeometry(20, 235, 49, 26)
        c_lb_modify_dt = QLabel("異動時間:",temp_frame)
        c_lb_modify_dt.setGeometry(225, 235, 66, 26)
        self.c_le_customm_no = udef_object.C_QLineEdit(temp_frame, "c_le_customm_no", 15, "",1, self.F_checkdata)
        self.c_le_customm_no.setGeometry(70, 5, 61, 26)
        self.c_le_customm_nm = udef_object.C_QLineEdit(temp_frame, "c_le_customm_nm", 20, "",1, self.F_checkdata)
        self.c_le_customm_nm.setGeometry(70, 40, 111, 26)
        self.c_cbb_customm_type = QComboBox(temp_frame)
        self.c_cbb_customm_type.setGeometry(360, 40, 56, 26)
        self.c_le_customm_f_nm = udef_object.C_QLineEdit(temp_frame, "c_le_customm_f_nm", 100, "",1, self.F_checkdata)
        self.c_le_customm_f_nm.setGeometry(70, 75, 346, 26)
        self.c_le_customm_f_nm_en = udef_object.C_QLineEdit(temp_frame, "c_le_customm_f_nm_en", 100, "",0, self.F_checkdata)
        self.c_le_customm_f_nm_en.setGeometry(70, 110, 346, 26)
        self.c_le_customm_manager = udef_object.C_QLineEdit(temp_frame, "c_le_customm_manager",20, "",0, self.F_checkdata)
        self.c_le_customm_manager.setGeometry(70, 145, 113, 26)
        self.c_le_customm_stopdate = udef_object.C_QLineEdit(temp_frame, "c_le_customm_stopdate", 8, "9999/99/99",0, self.F_checkdata)
        self.c_le_customm_stopdate.setGeometry(360, 145, 56, 26)
        self.c_te_customm_address = QTextEdit(temp_frame)
        self.c_te_customm_address.setGeometry(70, 180, 346, 46)
        self.c_le_modify_user = QLineEdit(temp_frame)
        self.c_le_modify_user.setGeometry(70, 235, 116, 26)
        self.c_le_modify_dt = QLineEdit(temp_frame)
        self.c_le_modify_dt.setGeometry(290, 235, 125, 26)
        self.c_le_modify_dt.setReadOnly(True)
        self.c_le_modify_user.setReadOnly(True)       
        self.setTabOrder(self.c_le_customm_no, self.c_le_customm_nm)
        self.setTabOrder(self.c_le_customm_nm, self.c_cbb_customm_type)
        self.setTabOrder(self.c_cbb_customm_type, self.c_le_customm_f_nm)
        self.setTabOrder(self.c_le_customm_f_nm, self.c_le_customm_f_nm_en)
        self.setTabOrder(self.c_le_customm_f_nm_en, self.c_le_customm_manager)
        self.setTabOrder(self.c_le_customm_manager, self.c_le_customm_stopdate)
        self.setTabOrder(self.c_le_customm_stopdate, self.c_te_customm_address)
        self.setTabOrder(self.c_te_customm_address, self.c_le_modify_user)
        self.setTabOrder(self.c_le_modify_user, self.c_le_modify_dt)
        self.c_cbb_customm_type_tv = db.F_Tableview_kindd(temp_frame,"A8",2)
        self.c_cbb_customm_type.setModel(self.c_cbb_customm_type_tv.model())
        self.c_cbb_customm_type.setView(self.c_cbb_customm_type_tv)
        self.c_cbb_customm_type.setModelColumn(3)       #顯示的欄位
        return temp_frame
    def F_view_mainframe(self,indexclicked):
        if self.c_pb_save.isVisible():
            QMessageBox.warning(self,"警告!","資料編輯中，禁止點選!!")
            self.c_tableview_customm.selectionModel().setCurrentIndex(self.modifyindex, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        else:
            row = indexclicked.row()
            self.pk_customm = self.c_tableview_customm.model().index(row, 0).data()
            self.c_le_customm_no.setText(self.c_tableview_customm.model().index(row, 1).data()) 
            self.c_le_customm_nm.setText(self.c_tableview_customm.model().index(row, 2).data())
            customm_type_index = self.c_cbb_customm_type_tv.model().match(self.c_cbb_customm_type_tv.model().index(0, 0), Qt.DisplayRole,self.c_tableview_customm.model().index(row,3).data(), 1, Qt.MatchContains)
            self.c_cbb_customm_type_tv.selectionModel().setCurrentIndex(customm_type_index[0],QItemSelectionModel.Select| QItemSelectionModel.Rows)
            self.c_cbb_customm_type.setCurrentText(self.c_cbb_customm_type_tv.model().index(customm_type_index[0].row(),3).data())
            self.c_le_customm_f_nm.setText(self.c_tableview_customm.model().index(row, 4).data())
            self.c_le_customm_f_nm_en.setText(self.c_tableview_customm.model().index(row, 5).data())
            self.c_le_customm_manager.setText(self.c_tableview_customm.model().index(row, 6).data())
            self.c_le_customm_stopdate.setText(self.c_tableview_customm.model().index(row, 7).data())
            self.c_te_customm_address.setText(self.c_tableview_customm.model().index(row, 8).data())
            self.c_le_modify_user.setText( db.F_get_user_nm(self.c_tableview_customm.model().index(row, 9).data()))
            self.c_le_modify_dt.setText(self.c_tableview_customm.model().index(row, 10).data())           
            self.modifyindex = self.c_tableview_customm.currentIndex()
            self.c_tableview_customd.model().setFilter("pk_customm = {}".format(self.pk_customm))
            self.c_tableview_customs.model().setFilter("pk_customs = {}". \
                                                       format(self.c_tableview_customd.model().index(self.c_tableview_customd.currentIndex().row(),0).data()))
    def F_checkdata(self,temp_objectName):
        temp_return = False
        return temp_return
    def F_create_button(self):      
        temp_frame = QFrame()
        self.c_pb_append = QPushButton("新  增 (&A)")
        self.c_pb_edit = QPushButton("修  改 (&E)")
        self.c_pb_delete = QPushButton("刪  除 (&D)")
        self.c_pb_save = QPushButton("儲  存 (&S)")
        self.c_pb_quit = QPushButton("離  開 (&Q)")
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
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
        self.c_le_customm_no.setText("")
        self.c_le_customm_nm.setText("")
        self.c_le_customm_f_nm.setText("")
        self.c_le_customm_f_nm_en.setText("")
        self.c_le_customm_manager.setText("")
        self.c_le_customm_stopdate.setText("")
        self.c_te_customm_address.setText("")        
        self.c_le_customm_no.setFocus()
        self.updatestatus = True
        self.c_tableview_customd.setContextMenuPolicy(Qt.CustomContextMenu)
        self.c_tableview_customs.setContextMenuPolicy(Qt.CustomContextMenu)
    def F_pb_edit(self):
        self.F_maintance(True)
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
        self.c_le_customm_no.setFocus()
        self.updatestatus = False
        self.c_tableview_customd.setContextMenuPolicy(Qt.CustomContextMenu)
        self.c_tableview_customs.setContextMenuPolicy(Qt.CustomContextMenu)
    def F_pb_delete(self):
        pass
    def F_pb_save(self):
        if self.updatestatus:
            sql = "INSERT INTO customm  (customm_no,customm_nm,customm_type,customm_f_nm,customm_f_nm_en,customm_manager,customm_stopdate,customm_address,modify_user,modify_dt) " \
                                                "VALUES (:customm_no,:customm_nm,:customm_type,:customm_f_nm,:customm_f_nm_en,:customm_manager,:customm_stopdate,:customm_address,:modify_user,:modify_dt)"
        else:
            row = self.modifyindex.row()
            sql ="UPDATE customm SET customm_no = :customm_no," \
                                                            "customm_nm = :customm_nm,"\
                                                            "customm_type = :customm_type,"\
                                                            "customm_f_nm = :customm_f_nm,"\
                                                            "customm_f_nm_en = :customm_f_nm,"\
                                                            "customm_manager = :customm_manager,"\
                                                            "customm_stopdate = customm_stopdate,"\
                                                            "customm_address = customm_address,"\
                                                            "modify_user = :modify_user,"\
                                                            "modify_dt = :modify_dt  WHERE pk_customm = {}".format(int(self.c_tableview_customm.model().index(row,0).data()))
        if self.c_sqlquery.prepare(sql):                                                         
            self.c_sqlquery.bindValue(":customm_no",self.c_le_customm_no.text())
            self.c_sqlquery.bindValue(":customm_nm",self.c_le_customm_nm.text())
            self.c_sqlquery.bindValue(":customm_type",self.c_cbb_customm_type_tv.model().index(self.c_cbb_customm_type_tv.currentIndex().row(), 0).data())
            self.c_sqlquery.bindValue(":customm_f_nm",self.c_le_customm_f_nm.text())
            self.c_sqlquery.bindValue(":customm_f_nm_en",self.c_le_customm_f_nm_en.text())
            self.c_sqlquery.bindValue(":customm_manager",self.c_le_customm_manager.text())
            self.c_sqlquery.bindValue(":customm_stopdate",self.c_le_customm_stopdate.text())
            self.c_sqlquery.bindValue(":customm_address",self.c_te_customm_address.toPlainText())
            self.c_sqlquery.bindValue(":modify_user",gv.gv_pk_s_userm)
            self.c_sqlquery.bindValue(":modify_dt",self.c_le_modify_dt.text())
            if not self.c_sqlquery.exec_():
                QMessageBox.critical(self, "錯誤!!", "儲存失敗.資料有誤!!.....\n\n" + self.c_sqlquery.lastError().text())
            else:
                # tableview 新增一行
                if self.updatestatus:
                    row = self.c_tableview_customm.model().rowCount()
                    self.c_tableview_customm.model().insertRow(row)
                    self.pk_customm = self.c_sqlquery.lastInsertId()
                    self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 0), self.pk_customm)    
                    rowd = self.c_tableview_customd.model().rowCount()
                    #update Customd
                    if rowd > 0:
                        for number in range(rowd):
                            self.c_tableview_customd.model().setData(self.c_tableview_customd.model().index(number, 1), self.pk_customm)
                    rowd = self.c_tableview_customs.model().rowCount()
                    pk_customd = self.c_tableview_customd.current().index(self.c_tableview_customd.model().row(),0).data()
                    #update Customs
                    if rowd > 0:
                        for number in range(rowd):
                            self.c_tableview_customs.model().setData(self.c_tableview_customd.model().index(number, 1), pk_customd)
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 1), self.c_le_customm_no.text())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 2), self.c_le_customm_nm.text())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 3),self.c_cbb_customm_type_tv.model().index(self.c_cbb_customm_type_tv.currentIndex().row(), 0).data())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 4), self.c_le_customm_f_nm.text())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 5), self.c_le_customm_f_nm_en.text())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 6), self.c_le_customm_manager.text())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 7), self.c_le_customm_stopdate.text())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 8), self.c_te_customm_address.toPlainText())
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 9), gv.gv_pk_s_userm)
                self.c_tableview_customm.model().setData(self.c_tableview_customm.model().index(row, 10), self.c_le_modify_dt.text())
                # Update cudtomd
                if not self.c_tableview_customd.model().submitAll():
                    QMessageBox.critical(self, "錯誤!!", "連絡人明細資料儲存失敗....\n\n" + self.c_tableview_customd.model().lastError().text())                   
                # 新增後定位使用,懶得判別新增做用
                temp_index = self.c_tableview_customm.model().match(self.c_tableview_customm.model().index(0, 1), Qt.DisplayRole, self.c_le_customm_no.text(), 1, Qt.MatchFixedString)
                self.c_tableview_customm.selectionModel().setCurrentIndex(temp_index[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
                self.F_view_mainframe(self.c_tableview_customm.currentIndex())
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
            self.c_tableview_customd.setContextMenuPolicy(Qt.NoContextMenu)
            self.c_tableview_customs.setContextMenuPolicy(Qt.NoContextMenu)            
            self.F_maintance(False)
            #self.F_view_mainframe(self.modifyindex)
    def F_maintance(self, temp_maintance_status):      
        if temp_maintance_status:
            self.c_pb_append.setVisible(False)
            self.c_pb_edit.setVisible(False)
            self.c_pb_delete.setVisible(False)
            self.c_pb_save.setVisible(True)
            self.c_le_customm_no.setReadOnly(False)
            self.c_le_customm_nm.setReadOnly(False)
            self.c_cbb_customm_type.setDisabled(False)
            self.c_le_customm_f_nm.setReadOnly(False)
            self.c_le_customm_f_nm_en.setReadOnly(False)
            self.c_le_customm_manager.setReadOnly(False)
            self.c_le_customm_stopdate.setReadOnly(False)
            self.c_te_customm_address.setReadOnly(False)
            self.c_pb_quit.setText("放  棄 (&Q)")
        else:
            self.c_pb_append.setVisible(self.appendstatus)
            self.c_pb_edit.setVisible(self.editstatus)
            self.c_pb_delete.setVisible(self.deletestatus)
            self.c_pb_save.setVisible(False)
            self.c_le_customm_no.setReadOnly(True)
            self.c_le_customm_nm.setReadOnly(True)
            self.c_cbb_customm_type.setDisabled(True)
            self.c_le_customm_f_nm.setReadOnly(True)
            self.c_le_customm_f_nm_en.setReadOnly(True)
            self.c_le_customm_manager.setReadOnly(True)
            self.c_le_customm_stopdate.setReadOnly(True)
            self.c_te_customm_address.setReadOnly(True)
            self.c_pb_quit.setText("離  開 (&Q)")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    db.F_DBConnect()
    window = C_widget('AED')
    sys.exit(app.exec_())
