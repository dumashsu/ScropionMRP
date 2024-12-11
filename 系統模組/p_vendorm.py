# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout,QLineEdit,QLabel,QComboBox,QTextEdit,QFrame, QSplitter,\
                                                       QTableView,QPushButton,QSpacerItem,QSizePolicy
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
        self.setGeometry((QDesktopWidget().availableGeometry().width()-900)/2,(QDesktopWidget().availableGeometry().height()-480)/2,900,480)
        self.setWindowTitle("供應商資料維護")
        splitter_buttom = QSplitter(Qt.Horizontal)       
        self.c_tableview_vendrom = db.F_QTableView(splitter_buttom,"vendorm","",["1|編號","2|簡稱"],[0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],[80,150],"S")
        splitter_center = QSplitter(Qt.Vertical)               
        splitter_vendord_s = QSplitter(Qt.Horizontal)
        self.c_tableView_vendord = db.F_QTableView(splitter_vendord_s,"vendord","",["2|連絡人"],[0,1],[120],"S")
        self.v_tableView_vendors = db.F_QTableView(splitter_vendord_s,"vendors","",["2|明細資料", "3|資料內容"], [0,1], [130,200],"R",["2|s_kindd|pk_s_kindd|kindd_nm"])
        splitter_vendord_s.setStretchFactor(0,1)
        splitter_vendord_s.setStretchFactor(1,2)
        splitter_center.addWidget(self.F_create_mainfraem())
        splitter_center.addWidget(splitter_vendord_s)       
        splitter_center.setStretchFactor(0,4)
        splitter_center.setStretchFactor(1,4)        
        splitter_buttom.addWidget(self.c_tableview_vendrom)        
        splitter_buttom.addWidget(splitter_center)
        splitter_buttom.addWidget(self.F_create_pushbutton())      
        splitter_buttom.setStretchFactor(0,4)
        splitter_buttom.setStretchFactor(1,5)
        splitter_buttom.setStretchFactor(2,1)        
        main_vbox = QVBoxLayout()
        main_vbox.setContentsMargins(1, 1, 1, 1)
        main_vbox.setSpacing(1)
        main_vbox.addWidget(self.F_create_filterframe())
        main_vbox.addWidget(splitter_buttom)
        main_vbox.setStretch(0,1)
        main_vbox.setStretch(1,12)       
        self.setLayout(main_vbox)
        self.show()
        self.updatestatus = False
        self.F_maintance(False)
    def F_create_filterframe(self):
        temp_frame = QFrame()
        temp_frame.setStyleSheet(gv.gv_filter_bg_color)
        c_lb_no_filter = QLabel("供應商編號:",temp_frame)
        c_lb_no_filter.setGeometry(5, 5, 81, 26)
        self.c_le_no_filter = udef_object.C_QLineEdit(temp_frame,"self.c_le_no_filter",10,"",0,self.F_checkdata)
        self.c_le_no_filter.setGeometry(85, 5, 113, 26)
        c_lb_nm_filter = QLabel("簡稱:",temp_frame)
        c_lb_nm_filter.setGeometry(215, 5, 36, 26)
        self.c_le_nm_filter = udef_object.C_QLineEdit(temp_frame,"self.c_le_nm_filter",20,"",0,self.F_checkdata)
        self.c_le_nm_filter.setGeometry(250, 5, 96, 26)
        return temp_frame
    def F_create_mainfraem(self):
        temp_mainframe = QFrame()       #self.splitter_center)
        temp_mainframe.setFrameShape(QFrame.StyledPanel)
        temp_mainframe.setFrameShadow(QFrame.Raised)
        c_lb_no = QLabel("供應商編號:",temp_mainframe)
        c_lb_no.setGeometry(10, 10, 81, 26)
        c_lb_nm = QLabel("簡稱:",temp_mainframe)
        c_lb_nm.setGeometry(425, 10, 36, 26)      
        c_lb_f_nm = QLabel("全名:",temp_mainframe)
        c_lb_f_nm.setGeometry(55, 40, 36, 26)
        c_lb_uni_no = QLabel("統一編號:",temp_mainframe)
        c_lb_uni_no.setGeometry(25, 70, 66, 26)
        c_lb_type = QLabel("類別:",temp_mainframe)
        c_lb_type.setGeometry(245, 70, 36, 26)        
        c_lb_kind = QLabel("性質:",temp_mainframe)
        c_lb_kind.setGeometry(425, 70, 36, 26)
        c_lb_purchasepolicy = QLabel("採購政策:",temp_mainframe)
        c_lb_purchasepolicy.setGeometry(25, 100, 66, 26)
        c_lb_tradeticket = QLabel("交易票據:",temp_mainframe)
        c_lb_tradeticket.setGeometry(215, 100, 66, 26)
        c_lb_ticketrate = QLabel("票據比率:",temp_mainframe)
        c_lb_ticketrate.setGeometry(395, 100, 66, 26)
        c_lb_taxsource = QLabel("稅金來源:",temp_mainframe)
        c_lb_taxsource.setGeometry(25, 130, 66, 26)                                
        c_lb_taxrate = QLabel("稅金比率:",temp_mainframe)
        c_lb_taxrate.setGeometry(215, 130, 66, 26)
        c_lb_deductrate = QLabel("扣款比率:",temp_mainframe)
        c_lb_deductrate.setGeometry(395, 130, 66, 26)
        c_lb_payment = QLabel("交易方式:",temp_mainframe)
        c_lb_payment.setGeometry(25, 160, 66, 26)
        c_lb_payday = QLabel("付款天數:",temp_mainframe)
        c_lb_payday.setGeometry(215, 160, 66, 26)
        c_lb_coin = QLabel("交易幣別:",temp_mainframe)
        c_lb_coin.setGeometry(395, 160, 66, 26)
        c_lb_manager = QLabel("負責人:",temp_mainframe)
        c_lb_manager.setGeometry(40, 190, 51, 26)       
        c_lb_expirydate = QLabel("停用日期:",temp_mainframe)
        c_lb_expirydate.setGeometry(215, 190, 66, 26)
        c_lb_address = QLabel("地址:",temp_mainframe)
        c_lb_address.setGeometry(55, 215, 36, 26)
        c_lb_modify_user = QLabel("異動人:",temp_mainframe)
        c_lb_modify_user.setGeometry(40, 275, 49, 26)
        c_lb_modify_dt = QLabel("異動時間:",temp_mainframe)
        c_lb_modify_dt.setGeometry(365, 275, 66, 26)       
        self.c_cbb_type = db.F_Tableview_kindd(QComboBox(temp_mainframe),"A9")
        self.c_cbb_type.setGeometry(280, 70, 80, 26)
        self.c_cbb_kind =  db.F_Tableview_kindd(QComboBox(temp_mainframe),"B1")
        self.c_cbb_kind.setGeometry(460, 70, 80, 26)
        self.c_cbb_purchasepolicy =  db.F_Tableview_kindd(QComboBox(temp_mainframe),"P1")
        self.c_cbb_purchasepolicy.setGeometry(90, 100,90, 26)
        self.c_cbb_tradeticket =  db.F_Tableview_kindd(QComboBox(temp_mainframe),"B2")
        self.c_cbb_tradeticket.setGeometry(280, 100, 100, 26)
        self.c_cbb_taxsource =  db.F_Tableview_kindd(QComboBox(temp_mainframe),"B3")
        self.c_cbb_taxsource.setGeometry(90, 130, 115, 26)
        self.c_cbb_payment =  db.F_Tableview_kindd(QComboBox(temp_mainframe),"B4")
        self.c_cbb_payment.setGeometry(90, 160, 115, 26)
        self.c_cbb_coin =  db.F_Tableview_kindd(QComboBox(temp_mainframe),"A1")
        self.c_cbb_coin.setGeometry(460, 160, 90, 26)
        self.c_le_no = udef_object.C_QLineEdit(temp_mainframe,"self.c_le_no",10,"",1,self.F_checkdata)
        self.c_le_no.setGeometry(90, 10, 113, 26)
        self.c_le_nm = udef_object.C_QLineEdit(temp_mainframe,"self.c_le_nm",20,"",1,self.F_checkdata)
        self.c_le_nm.setGeometry(460, 10, 96, 26)
        self.c_le_f_nm = udef_object.C_QLineEdit(temp_mainframe,"self.c_le_f_nm",100,"",1,self.F_checkdata)
        self.c_le_f_nm.setGeometry(90, 40, 471, 26)
        self.c_le_uni_no = QLineEdit(temp_mainframe)
        self.c_le_uni_no.setGeometry(90, 70, 101, 26)        
        self.c_le_ticketrate = QLineEdit(temp_mainframe)
        self.c_le_ticketrate.setGeometry(460, 100, 31, 26)
        self.c_le_taxrate = QLineEdit(temp_mainframe)
        self.c_le_taxrate.setGeometry(280, 130, 26, 26)
        self.c_le_taxrate.setText("")
        self.c_le_deductrate = QLineEdit(temp_mainframe)
        self.c_le_deductrate.setGeometry(460, 130, 31, 26)
        self.c_le_deductrate.setText("")
        self.c_le_payday = QLineEdit(temp_mainframe)
        self.c_le_payday.setGeometry(280, 160, 41, 26)
        self.c_le_payday.setText("")
        self.c_le_manager = QLineEdit(temp_mainframe)
        self.c_le_manager.setGeometry(90, 190, 101, 26)
        self.c_le_manager.setText("")
        self.c_le_expirydate = QLineEdit(temp_mainframe)
        self.c_le_expirydate.setGeometry(280, 190, 101, 26)
        self.c_le_expirydate.setText("")      
        self.c_te_address = QTextEdit(temp_mainframe)
        self.c_te_address.setGeometry(90, 220, 466, 51)
        self.c_le_modify_user = QLineEdit(temp_mainframe)
        self.c_le_modify_user.setGeometry(90, 275, 116, 26)
        self.c_le_modify_dt = QLineEdit(temp_mainframe)
        self.c_le_modify_dt.setGeometry(430, 275, 125, 26)
        self.c_le_modify_user.setReadOnly(True)        
        self.c_le_modify_dt.setReadOnly(True)
        return temp_mainframe
    def F_view_mainframe(self):
        pass
    def F_checkdata(self,temp_objectName):
        temp_return = False
        # if temp_objectName == "c_le_user_id":
        #     if len(self.c_le_user_id.text() == 0:
        #         temp_return=(True, "使用者 ID 不可為空....")
        #     else:
        #         self.c_sqlquery.exec_("SELECT * FROM s_userm WHERE user_id = '{}'".format(self.c_le_user_id.text())
        #         if self.c_sqlquery.next():                   #  不管新增/修改 資料只有一筆
        #             if self.update_status:
        #                 temp_return = (True, "使用者 ID 已存在，不可重複!")
        #             elif self.c_sqlquery.value(0) != self.c_tableviewL.model().index(self.c_tableviewL.currentIndex().row(), 0).data():
        #                 temp_return = (True, "使用者 ID 已存在，不可重複!!",self.c_tableviewL.model().index(self.c_tableviewL.currentIndex().row(), 2).data()
        return temp_return
    def F_create_pushbutton(self):
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
            self.c_pb_quit.setText("放  棄 (&Q)")
        else:
            self.c_pb_append.setVisible(self.appendstatus)
            self.c_pb_edit.setVisible(self.editstatus)
            self.c_pb_delete.setVisible(self.deletestatus)
            self.c_pb_save.setVisible(False)
            #self.c_le_brand_no.setReadOnly(True)
            #self.c_le_brand_nm.setReadOnly(True)
            #self.c_le_brand_payday.setReadOnly(True)
            #self.c_te_delivery_address.setReadOnly(True)
            #self.c_te_pack_desc.setReadOnly(True)
            self.c_pb_quit.setText("離  開 (&Q)")
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     db.F_DBConnect()
#     window = C_widget("AED")
#     sys.exit(app.exec_())