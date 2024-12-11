# -*- coding: utf-8 -*-
''' p_matm
說明:材料基本資料維護作業,更新 matm/matvendorm
主:pushbutton
從:popmenu

Tableview_Mater/Detail  範本程式
'''
from PyQt5.QtCore import QDateTime, Qt, QItemSelectionModel, QFile, QVariant, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QRadioButton, QButtonGroup, \
                                                                      QComboBox, QFileDialog, QAbstractItemView, QSizePolicy, QHBoxLayout, QVBoxLayout, QDesktopWidget, \
                                                                      QSpacerItem, QSplitter,QTableView
import db
import gv
import sys
import udef_object
from PyQt5.Qt import QTableWidget

class C_widget(QWidget):
    def __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setGeometry((QDesktopWidget().availableGeometry().width() - 900) / 2,(QDesktopWidget().availableGeometry().height() - 500) / 2, 900, 500)
        self.setStyleSheet(gv.gv_bg_font)
        self.c_sqlquery = QSqlQuery()
        self.setWindowTitle("材料基本資料維護作業")
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(1, 1, 1,1 )
        main_vbox.setSpacing(1)        
        main_splitter = QSplitter(Qt.Horizontal,self)
        main_splitter.addWidget(self.F_BrowserTvFrame())       # 瀏覽區's Frame
        main_splitter.addWidget(self.F_MasterFrame())      
        main_splitter.addWidget(self.F_PushButton())
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1,11)
        main_splitter.setStretchFactor(2, 1)
        main_splitter.setHandleWidth(0)
        #將各 frame 放入 window中
        main_vbox.addWidget(self.F_FilterFrame())
        main_vbox.addWidget(main_splitter)
        main_vbox.setStretch(0,1)
        main_vbox.setStretch(1,10)
        # 新增/修改/下拉 按紐的控制變數
        self.update_status = True
        self.v_pop_status = True

        # 首次進入則開啟第一筆資料
        if self.c_tv_matm.model().rowCount() > 0:
            self.c_tv_matm.selectionModel().setCurrentIndex(self.c_tv_matm.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
#            self.F_filter_tv_clicked(self.c_tv_s_userm.model().index(0, 0))
        #初進入之狀態
        self.F_maintain(False)
        self.show()

    def F_pb_append(self):
        if self.v_pop_status:
            self.F_maintain(True)
            self.update_status = True
            #清空橍位
            #self.c_le_mat_no.setText("")
            
            #設焦點
            self.c_le_mat_no.setFocus()
        else:
            QMessageBox.warning(self, "錯誤!!", "請先離開明細資料的維護作業.........\n\n")

    def F_pb_edit(self):
        #Tableview空值或和資料區 資料不一時禁止修改/刪除
        chk_tableviewL_data = self.c_tv_matm.model().index(self.c_tv_matm.currentIndex().row(), 0).data()
        if (chk_tableviewL_data != None) and (chk_tableviewL_data == int(self.c_le_matm.text())) :
            self.F_maintain(True)
            self.c_le_modify_user.setText(gv.gv_user)
            self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
            self.c_le_mat_no.setFocus()
            self.c_le_mat_no.selectAll()
            self.update_status = False
            #開啟 Detail's POPMENU
            #self.c_tv_matvendorm.setContextMenuPolicy(Qt.CustomContextMenu)
        else:
            QMessageBox.warning(self, "錯誤!!", "請先選擇左方欲修改或刪除的資料.....\n\n")
    def F_pb_delete(self):
        #Tableview空值或和資料區 資料不一時禁止修改/刪除
        chk_tableviewL_data = self.c_tv_matm.model().index(self.c_tv_matm.currentIndex().row(), 0).data()
        if (chk_tableviewL_data != None) and (chk_tableviewL_data == int(self.c_le_pk_s_userm.text())) :
            QM_replay = QMessageBox.question(self, "訊息!!!","是否確認刪除?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if QM_replay == QMessageBox.Yes:
                # 刪除明細資料
                row = self.c_tv_s_userd.model().rowCount()
                for number in range(row):
                    self.c_tv_s_userd.model().removeRow(number)
                if not self.c_tv_s_userd.model().submitAll():
                    QMessageBox.critical(self, "錯誤!!", "明細資料,刪除失敗.\n\n" + self.c_tv_s_userd.model().lastError().text())
            else:
                    row = self.c_tv_s_userm.currentIndex().row()
                    self.c_tv_s_userm.model().removeRow(row)
                    if not self.c_tv_s_userm.model().submitAll():
                        QMessageBox.critical(self, "錯誤!!", "刪除失敗.\n\n" + self.c_tv_s_userm.model().lastError().text())
                        self.c_tv_s_userm.model().revertAll()
                    else:
                        self.c_tv_s_userm.selectionModel().setCurrentIndex(self.c_tv_s_userm.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
                        self.F_filter_tv_clicked(self.c_tv_s_userm.model().index(0, 0))
        else:
            QMessageBox.warning(self, "錯誤!!", "請先選擇左方欲修改或刪除的資料.....\n\n")
    def F_pb_save(self):
        if self.update_status:
            row = self.c_tv_matm.model().rowCount()
            self.c_tv_matm.model().insertRow(row)
        else:
            row = self.c_tv_s_userm.currentIndex().row()
        #資料料寫入 Browser Tableview 
        #self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 1), self.c_cbb_tv_factory_no.model().index(self.c_cbb_tv_factory_no.currentIndex().row(), 0).data())
        self.c_tv_matm.model().setData(self.c_tv_matm.model().index(row, 15), gv.gv_pk_s_userm)
        self.c_tv_matm.model().setData(self.c_tv_matm.model().index(row, 16), self.c_le_modify_dt.text())

        if not self.c_tv_matm.model().submitAll():
            QMessageBox.critical(self, "錯誤!!", "儲存失敗....\n\n" + self.c_tv_matm.model().lastError().text())
            self.c_tv_matm.model().revertAll()
            #self.c_tv_s_userd.model().revertAll()
        else:
            # 新增儲存時，需取回主檔的 KEY,以便寫入明細檔
            self.c_tv_matm.model().setData(self.c_tv_matm.model().index(row, 5), 0)
            if self.update_status:
                self.c_le_pk_matm.setText(str(self.c_tv_matm.model().query().lastInsertId()))
                rowR = self.c_tv_matm.model().rowCount()     #明細檔 popmenu 新增榼不會寫入KEY,所以手動寫入
                if rowR > 0:
                    for number in range(rowR):
                        self.c_tv_matvendorm.model().setData(self.c_tv_matvendorm.model().index(number, 1), int(self.c_le_pk_matm.text()))
            self.F_maintain(False)
            if not self.c_tv_matvendorm.model().submitAll():
                QMessageBox.critical(self, "錯誤!!", "明細資料儲存失敗....\n\n" + self.c_tv_matvendorm.model().lastError().text())
            else:
                #找出新增的值, 以便Browser Tableview 定位
                temp_index = self.c_tv_matm.model().match(self.c_tv_matm.model().index(0, 0), Qt.DisplayRole,int(self.c_le_pk_matm.text()) , 1, Qt.MatchFixedString)
                self.c_tv_matm.selectionModel().setCurrentIndex(temp_index[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
                self.F_BrowserTvClicked(self.c_tv_matm.currentIndex())
                                        
    def F_pb_quit(self):
        if not self.c_pb_save.isVisible():
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
            #判斷資料是否有異動, 若有再次確認是否放棄
        else:
            self.c_tv_matvendorm.setContextMenuPolicy(Qt.NoContextMenu)
            self.F_maintain(False)            
#             if self.c_le_factory_no.isModified() or  \
#                     self.c_le_user_id.isModified() or \
#                     self.c_le_user_nm.isModified() or \
#                     self.c_le_user_pswd.isModified() :
#                 QM_replay = QMessageBox.question(self, "訊息!!!", "資料己被更改，是否放棄?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#                 if QM_replay == QMessageBox.Yes:
#                     arg = self.c_tv_s_userm.selectedIndexes()
#                     if len(arg) >0: self.F_filter_tv_clicked(arg[0])
#                     self.F_maintain(False)
#             else:
#                 # 第一次未點選 Tableview 自動選擇 所以 currentIndex 無法取得該值
#                 arg = self.c_tv_s_userm.selectedIndexes()
#                 self.F_maintain(False)
#                 if len(arg) > 0:
#                     self.F_filter_tv_clicked(arg[0])
    def F_checkdata(self,temp_objectName):
        temp_return = False
#         if temp_objectName == "c_le_user_id":
#             if len(self.c_le_user_id.text()) == 0:
#                 temp_return=(True, "使用者 ID 不可為空....")
#             else:
#                 self.c_sqlquery.exec_("SELECT * FROM s_userm WHERE user_id = '{}'".format(self.c_le_user_id.text()))
#                 if self.c_sqlquery.next():                   #  不管新增/修改 資料只有一筆
#                     if self.update_status:
#                         temp_return = (True, "使用者 ID 已存在，不可重複!")
#                     elif self.c_sqlquery.value(0) != self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 0).data():
#                         temp_return = (True, "使用者 ID 已存在，不可重複!!",self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 2).data())

        return temp_return

    def F_maintain(self,modify_mark):
        if modify_mark:
            self.c_pb_append.setVisible(False)
            self.c_pb_edit.setVisible(False)
            self.c_pb_delete.setVisible(False)
            self.c_pb_save.setVisible(True)
            self.c_pb_quit.setText("放  棄 (&Q)")
            self.c_tv_matvendorm.setContextMenuPolicy(Qt.NoContextMenu)            
            #修改時 filter 及開放欄位修改 

        else:
            self.c_pb_append.setVisible(self.appendstatus)
            self.c_pb_edit.setVisible(self.editstatus)
            self.c_pb_delete.setVisible(self.deletestatus)
            self.c_pb_save.setVisible(False)
            self.c_pb_quit.setText("離  開 (&Q)")
            self.c_tv_matvendorm.setContextMenuPolicy(Qt.CustomContextMenu)            
            #放棄修改/新增 欄位回復禁止編輯
#             self.c_le_tableviewL_filter.setEnabled(True)
            # 打開 Detail 的右鍵功能
            self.c_tv_matvendorm.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def F_FilterFrame(self):
        c_frame = QFrame(self)
        c_frame.setFrameShape(QFrame.NoFrame)
        c_frame.setFrameShadow(QFrame.Raised)
        c_frame.setStyleSheet(gv.gv_filter_bg_color)
        c_lb_mat_no_filter = QLabel("材料代號:",c_frame)
        c_lb_mat_no_filter.setGeometry(5, 10, 66, 26)
        c_lb_mat_nm_filter = QLabel("材料名稱:",c_frame)
        c_lb_mat_nm_filter.setGeometry(185, 10, 91, 26)
        self.c_le_mat_no_filter = udef_object.C_QLineEdit(c_frame, "c_le_mat_no",10,"",0, self.F_checkdata)
        self.c_le_mat_no_filter.setGeometry(70, 10, 96, 26)        
        self.c_le_mat_nm_filter = udef_object.C_QLineEdit(c_frame, "c_le_mat_no",40,"",0, self.F_checkdata)
        self.c_le_mat_nm_filter.setGeometry(255, 10, 431, 26)
        return c_frame

    def F_BrowserTvFrame(self):
        self.c_tv_matm = db.F_QTableView(self,"matm","",  ["1|材料代號", "2|材料名稱"], [0,3,4,5,6,7,8,9,10,11,12,13,14,15,16], [100,150],"S")
        self.c_tv_matm.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.c_tv_matm.clicked.connect(self.F_BrowserTvClicked)
        self.c_tv_matm.sortByColumn(1,Qt.AscendingOrder)
        return self.c_tv_matm
    
    def F_BrowserTvClicked(self,indexClicked):
        if self.c_pb_save.isVisible() or self.v_pop_status:
            QMessageBox.warning(self, "錯誤!!", "請先離開 {}  維護作業.........\n\n".format(lambda:"主編輯" if self.c_pb_save.isVisible( ) else "明細"))
            self.c_tv_matm.setCurrentIndex(self.v_modifyindex)          #恢後原值
        else:
            self.v_modifyindex = indexClicked
            row = self.v_modifyindex.row()
            self.c_le_pk_matm.setText(str(self.c_tv_s_userm.model().index(row, 0).data()))
            
            #self.c_le_factory_no.setText(str(self.c_tv_s_userm.model().index(row, 1).data()))
            # 以值找尋 Combobox's Tableview 返回 QModelIndex, 再由其尋找文字並將 Combobox 設成真正的位置,當然前提 combobox's tableview 已設計顯示該欄位
            # 由 KEY值找到 tableview's行,再由其取出值來定 combobox, 同時也定值 tableview 以便修改時儲存之用
            #factory_no_index = self.c_cbb_tv_factory_no.model().match(self.c_cbb_tv_factory_no.model().index(0, 0), Qt.DisplayRole,self.c_tv_s_userm.model().index(row, 1).data(), 1, Qt.MatchContains)
            #self.c_cbb_tv_factory_no.selectionModel().setCurrentIndex(factory_no_index[0],QItemSelectionModel.Select| QItemSelectionModel.Rows)
            #self.c_cbb_factory_no.setCurrentText(self.c_cbb_tv_factory_no.model().index(factory_no_index[0].row(),2).data())
            # 顯示點擊後的內容
            #self.c_le_user_id.setText(self.c_tv_s_userm.model().index(row, 2).data())

    def F_MasterFrame(self):
        c_frame = QFrame(self)
        c_frame.setFrameShape(QFrame.Box)
        c_frame.setFrameShadow(QFrame.Raised)
        c_frame.setLineWidth(1)             
        c_lb_mat_no = QLabel("材料編號:",c_frame)
        c_lb_mat_no.setGeometry(35, 15, 66, 26)
        c_lb_color_no = QLabel("顏色編號:",c_frame)
        c_lb_color_no.setGeometry(210, 15, 66, 26)
        c_lb_color_nm = QLabel(c_frame)
        c_lb_color_nm.setGeometry(375, 15, 156, 26)
        c_lb_color_nm.setStyleSheet("background-color: rgb(221, 221, 221);")
        c_lb_mat_nm = QLabel("材料名稱(中):",c_frame)
        c_lb_mat_nm.setGeometry(10, 45, 91, 26)        
        c_lb_mat_nm_en = QLabel("材料名稱(英):",c_frame)
        c_lb_mat_nm_en.setGeometry(10, 105, 91, 26)
        c_lb_kindd_nm = QLabel("單位名稱:",c_frame)
        c_lb_kindd_nm.setGeometry(35, 165, 66, 26)
        c_lb_preprdmat_mk = QLabel("加工材料:",c_frame)
        c_lb_preprdmat_mk.setGeometry(225, 165, 66, 26)
        c_lb_exceed_rec_mk = QLabel("超交允收:",c_frame)
        c_lb_exceed_rec_mk.setGeometry(400, 165, 66, 26)
        c_lb_onway_qty = QLabel("在途量:",c_frame)
        c_lb_onway_qty.setGeometry(50, 195, 51, 26)
        c_lb_safestk_qty = QLabel("安全存量:",c_frame)
        c_lb_safestk_qty.setGeometry(225, 195, 66, 26)
        c_lb_purchase_day = QLabel("購備期:",c_frame)
        c_lb_purchase_day.setGeometry(415, 195, 51, 26)
        c_lb_unit_price = QLabel("單價:",c_frame)
        c_lb_unit_price.setGeometry(65, 225, 36, 26)
        c_lb_stop_user = QLabel("停用人:",c_frame)
        c_lb_stop_user.setGeometry(240, 225, 51, 26)        
        c_lb_stop_date = QLabel("停用日期:",c_frame)
        c_lb_stop_date.setGeometry(400, 225, 66, 26)
        c_lb_modify_user = QLabel("異動人:",c_frame)
        c_lb_modify_user.setGeometry(50, 255, 51, 26)
        c_lb_modify_dt = QLabel("異動日期:",c_frame)
        c_lb_modify_dt.setGeometry(225, 255, 66, 26)
                                        
        self.c_le_mat_no = udef_object.C_QLineEdit(c_frame, "c_le_mat_no",10,"",1, self.F_checkdata)
        self.c_le_mat_no.setGeometry(100, 15, 96, 26)
        self.c_le_color_no = udef_object.C_QLineEdit(c_frame, "c_le_color_no",10,"",1, self.F_checkdata)
        self.c_le_color_no.setGeometry(275, 15, 96, 26)
        self.c_le_mat_nm = udef_object.C_QLineEdit(c_frame, "c_le_mat_nm",300,"",1, self.F_checkdata)
        self.c_le_mat_nm.setGeometry(100, 45, 431, 56)
        self.c_le_mat_nm_en = udef_object.C_QLineEdit(c_frame, "c_le_mat_nm_en",300,"",0, self.F_checkdata)
        self.c_le_mat_nm_en.setGeometry(100, 105, 431, 56)
        self.c_le_kindd_nm = udef_object.C_QLineEdit(c_frame, "c_le_kindd_nm",5,"",1, self.F_checkdata)
        self.c_le_kindd_nm.setGeometry(100, 165, 66, 26)
        self.c_le_preprdmat_mk = udef_object.C_QLineEdit(c_frame, "c_le_preprdmat_mk",5,"",1, self.F_checkdata)
        self.c_le_preprdmat_mk.setGeometry(290, 165, 66, 26)
        self.c_le_exceed_rec_mk = udef_object.C_QLineEdit(c_frame, "c_le_exceed_rec_mk",5,"",1, self.F_checkdata)
        self.c_le_exceed_rec_mk.setGeometry(465, 165, 21, 26)
        self.c_le_onway_qty = udef_object.C_QLineEdit(c_frame, "c_le_onway_qty",14,"999,999,999.99",0, self.F_checkdata)
        self.c_le_onway_qty.setGeometry(100, 195, 96, 26)
        self.c_le_safestk_qty = udef_object.C_QLineEdit(c_frame, "c_le_safestk_qty",14,"999,999,999.99",0, self.F_checkdata)
        self.c_le_safestk_qty.setGeometry(290, 195, 101, 26)
        self.c_le_purchase_day = udef_object.C_QLineEdit(c_frame, "c_le_purchase_day",3,"999",0, self.F_checkdata)
        self.c_le_purchase_day.setGeometry(465, 195, 31, 26)
        self.c_le_unit_price = udef_object.C_QLineEdit(c_frame, "c_le_unit_price",12,"999,999.9999",0, self.F_checkdata)
        self.c_le_unit_price.setGeometry(100, 225, 101, 26)
        self.c_le_stop_user = udef_object.C_QLineEdit(c_frame, "c_le_stop_user",20,"",0, self.F_checkdata)
        self.c_le_stop_user.setGeometry(290, 225, 101, 26)
        self.c_le_stop_date = udef_object.C_QLineEdit(c_frame, "c_le_stop_date",10,"9999/99/99",0, self.F_checkdata)
        self.c_le_stop_date.setGeometry(465, 225, 71, 26)
        self.c_le_modify_user = QLineEdit(c_frame)
        self.c_le_modify_user.setGeometry(100, 255, 101, 26)
        self.c_le_modify_dt = QLineEdit(c_frame)
        self.c_le_modify_dt.setGeometry(290, 255, 71, 26)

        self.c_le_modify_user.setReadOnly(True)
        self.c_le_modify_dt.setReadOnly(True)
        #TAB 順序
        c_frame.setTabOrder(self.c_le_mat_no, self.c_le_color_no)
        c_frame.setTabOrder(self.c_le_color_no,self.c_le_mat_nm)
        c_frame.setTabOrder(self.c_le_mat_nm,self.c_le_mat_nm_en)
        c_frame.setTabOrder(self.c_le_mat_nm_en,self.c_le_kindd_nm)
        c_frame.setTabOrder(self.c_le_kindd_nm,self.c_le_preprdmat_mk)        
        c_frame.setTabOrder(self.c_le_preprdmat_mk,self.c_le_exceed_rec_mk)
        c_frame.setTabOrder(self.c_le_exceed_rec_mk,self.c_le_onway_qty)
        c_frame.setTabOrder(self.c_le_onway_qty,self.c_le_safestk_qty)
        c_frame.setTabOrder(self.c_le_safestk_qty,self.c_le_purchase_day)
        c_frame.setTabOrder(self.c_le_purchase_day,self.c_le_unit_price)
        c_frame.setTabOrder(self.c_le_unit_price,self.c_le_stop_user)
        c_frame.setTabOrder(self.c_le_stop_user,self.c_le_stop_date)
        # Detail's frame
        # 建立 0 row * 3 column 的 Qtablewidget 
        #建立tablewidget 並且第一欄供應商代號 RELATION 到 VENDORM 可輸入及下拉選取
        self.c_tv_matvendorm = QTableWidget(0,3,c_frame)            
        self.c_tv_matvendorm.verticalHeader().setVisible(False)
        self.c_tv_matvendorm.setHorizontalHeaderLabels(["供應商","供應商名稱","停用日期"])
        self.c_tv_matvendorm.setColumnWidth(1,300)
        self.c_tv_matvendorm.setColumnWidth(2,140)
#         db.F_Tableview_kindd(self.c_tv_matvendorm,"02",2)   # 生成 tableview 的下拉資料,選擇後回傳值,再由 Relation 來顯示文字
        self.c_tv_matvendorm.setGeometry(3, 285, 545, 165)
        self.c_tv_matvendorm.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.c_tv_matvendorm.customContextMenuRequested.connect(lambda:db.C_PopMenu(self, self.c_tv_matvendorm,[],"F"))       
        return c_frame
    def F_PushButton(self):
        # PushButtom
        c_frame =QFrame()
        self.c_pb_append = QPushButton("新  增 (&A)", self)
        self.c_pb_edit = QPushButton("修  改 (&E)", self)
        self.c_pb_delete = QPushButton("刪  除 (&D)", self)
        self.c_pb_save = QPushButton("儲  存 (&S)", self)
        self.c_pb_save.setVisible(False)
        self.c_pb_quit = QPushButton("離  開 (Q)", self)
        # PushButtom
        self.c_pb_append.clicked.connect(self.F_pb_append)
        self.c_pb_edit.clicked.connect(self.F_pb_edit)
        self.c_pb_delete.clicked.connect(self.F_pb_delete)
        self.c_pb_save.clicked.connect(self.F_pb_save)
        self.c_pb_quit.clicked.connect(self.F_pb_quit)
        vbox3 = QVBoxLayout(c_frame)
        vbox3.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        vbox3.addWidget(self.c_pb_append)
        vbox3.addSpacing(20)
        vbox3.addWidget(self.c_pb_edit)
        vbox3.addSpacing(20)
        vbox3.addWidget(self.c_pb_delete)
        vbox3.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox3.addWidget(self.c_pb_save)
        vbox3.addSpacing(20)
        vbox3.addWidget(self.c_pb_quit)
        return c_frame
if __name__ == "__main__":
    app = QApplication(sys.argv)
    db.F_DBConnect()
    c_window = C_widget('AED')
    sys.exit(app.exec_())
