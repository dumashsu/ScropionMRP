# -*- coding: utf-8 -*-
''' p_userm
說明:使用者基本資料維護作業,更新 s_userm/s_userd
主/從一同存檔

Tableview_Mater/Detail  範本程式
'''
from PyQt5.QtCore import QDateTime, Qt, QItemSelectionModel, \
             QFile, QVariant, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QRadioButton, QButtonGroup, QComboBox, QFileDialog, \
                            QAbstractItemView, QSizePolicy, QHBoxLayout, QVBoxLayout, QDesktopWidget, QSpacerItem, QSplitter
import db
import gv
import sys
import udef_object

class C_widget(QWidget):
    def __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setGeometry((QDesktopWidget().availableGeometry().width() - 800) / 2,(QDesktopWidget().availableGeometry().height() - 420) / 2, 800, 420)
        self.setStyleSheet(gv.gv_bg_font)
        self.c_sqlquery = QSqlQuery()
        self.setWindowTitle("使用者資料維護")
        main_hbox = QHBoxLayout(self)
        main_hbox.setContentsMargins(2, 2, 2, 2)
        main_hbox.setSpacing(2)
        main_splitter = QSplitter(Qt.Horizontal,self)
        main_splitter.addWidget(self.F_filter_tv_frame())       # widget 間才可以 splitter
        main_splitter.addWidget(self.F_masterform())
        main_splitter.addWidget(self.F_PushButton())
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1,11)
        main_splitter.setStretchFactor(2, 1)
        main_hbox.addWidget(main_splitter)                 #addLayout(vbox1)

        # 新增/修改/下拉 按紐的控制變數
        self.update_status = True
        self.v_pop_status = True

        # 首次進入則開啟第一筆資料
        if self.c_tv_s_userm.model().rowCount() > 0:
            self.c_tv_s_userm.selectionModel().setCurrentIndex(self.c_tv_s_userm.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
            self.F_filter_tv_clicked(self.c_tv_s_userm.model().index(0, 0))
        #初進入之狀態
        self.F_maintain(False)
        self.show()
    def F_filter_tv_frame(self):
        c_frame = QFrame()
        c_frame.setFrameShape(QFrame.Box)
        c_frame.setFrameShadow(QFrame.Raised)
        self.c_le_tableviewL_filter = QLineEdit()
        self.c_le_tableviewL_filter.returnPressed.connect(self.F_filter_tv)
        self.c_tv_s_userm = db.F_QTableView(self,"s_userm","",  ["2|使用者ID", "3|使用者名稱"], [0,1,4,5,6,7,8,9,10], [90,158],"S")
        self.c_tv_s_userm.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.c_tv_s_userm.clicked.connect(self.F_filter_tv_clicked)
        self.c_tv_s_userm.sortByColumn(2,Qt.AscendingOrder)
        vbox1 = QVBoxLayout(c_frame)
        vbox1.addWidget(self.c_le_tableviewL_filter)
        vbox1.addWidget(self.c_tv_s_userm)
        vbox1.setContentsMargins(0,0,0,0)
        vbox1.setSpacing(1)
        return c_frame
    def F_filter_tv(self):
        self.c_tv_s_userm.model().setFilter("user_id like '%{}%'".format(self.c_le_tableviewL_filter.text()))
        self.F_maintain(False)
        #清空 freeform 欄位
        #self.c_te_module_memo.setText("")
        self.c_le_pk_s_userm.setText("")
        self.c_le_factory_no.setText("")       
        self.c_le_user_id.setText("")
        self.c_le_user_nm.setText("")
        self.c_le_user_pswd.setText("")
        self.c_le_user_suspended.setText("")
        self.c_le_user_marked.setText("")
        self.c_le_modify_user.setText(gv.gv_user)
        self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
        self.c_pm_user_photo = QPixmap()

        if self.c_tv_s_userm.model().rowCount() > 0:
            self.c_tv_s_userm.selectionModel().setCurrentIndex(self.c_tv_s_userm.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
            self.F_filter_tv_clicked(self.c_tv_s_userm.model().index(0, 0))

    def F_filter_tv_clicked(self,indexClicked):
        if not self.c_pb_save.isVisible():
            row = indexClicked.row()
            self.c_le_pk_s_userm.setText(str(self.c_tv_s_userm.model().index(row, 0).data()))
            #self.c_le_factory_no.setText(str(self.c_tv_s_userm.model().index(row, 1).data()))
            # 以值找尋 Combobox's Tableview 返回 QModelIndex, 再由其尋找文字並將 Combobox 設成真正的位置,當然前提 combobox's tableview 已設計顯示該欄位
            # 由 KEY值找到 tableview's行,再由其取出值來定 combobox, 同時也定值 tableview 以便修改時儲存之用
            factory_no_index = self.c_cbb_tv_factory_no.model().match(self.c_cbb_tv_factory_no.model().index(0, 0), Qt.DisplayRole,self.c_tv_s_userm.model().index(row, 1).data(), 1, Qt.MatchContains)
            self.c_cbb_tv_factory_no.selectionModel().setCurrentIndex(factory_no_index[0],QItemSelectionModel.Select| QItemSelectionModel.Rows)
            self.c_cbb_factory_no.setCurrentText(self.c_cbb_tv_factory_no.model().index(factory_no_index[0].row(),2).data())

            self.c_le_user_id.setText(self.c_tv_s_userm.model().index(row, 2).data())
            self.c_le_user_nm.setText(self.c_tv_s_userm.model().index(row, 3).data())
            self.c_le_user_pswd.setText(self.c_tv_s_userm.model().index(row, 4).data())
            if self.c_tv_s_userm.model().index(row, 5).data() == 0:
                self.c_rb_user_suspended_Yes.setChecked(True)
            else:
                self.c_rb_user_suspended_No.setChecked(True)

            if self.c_tv_s_userm.model().index(row, 7).data() == '1':
                self.c_rb_user_marked_1.setChecked(True)
            else:
                self.c_rb_user_marked_9.setChecked(True)
            self.c_pm_user_photo.loadFromData(self.c_tv_s_userm.model().index(row, 10).data(),"JPEG")
            self.c_lb_user_photo.setPixmap(self.c_pm_user_photo)
            self.c_le_modify_user.setText(db.F_get_user_nm(self.c_tv_s_userm.model().index(row, 8).data()))
            self.c_le_modify_dt.setText(self.c_tv_s_userm.model().index(row, 9).data())
            # 顯示下方的 tableviewR
            self.c_tv_s_userd.model().setFilter("pk_s_userm = {}".format(self.c_tv_s_userm.model().index(row, 0).data()))

    def F_pb_append(self):
        if self.v_pop_status:
            self.F_maintain(True)
            self.update_status = True
            #清空橍位
            self.c_le_pk_s_userm.setText("")
            self.c_le_factory_no.setText("")
            self.c_le_user_id.setText("")
            self.c_le_user_nm.setText("")
            self.c_le_user_pswd.setText("")
            self.c_le_user_suspended.setText("")
            self.c_le_user_marked.setText("")
            self.c_rb_user_suspended_Yes.setChecked(True)
            self.c_rb_user_marked_1.setChecked(True)
            self.imgfile = ""
            self.c_le_modify_user.setText(gv.gv_user)
            self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
            self.c_le_user_id.setFocus()
            # 顯示下方的 tableviewR
            self.c_tv_s_userd.model().setFilter("pk_s_userm = {}".format('NULL'))
            self.c_tv_s_userd.setContextMenuPolicy(Qt.CustomContextMenu)
        else:
            QMessageBox.warning(self, "錯誤!!", "請先離開明細資料的維護作業.........\n\n")
    def F_pb_edit(self):
        #Tableview空值或和資料區 資料不一時禁止修改/刪除
        chk_tableviewL_data = self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 0).data()
        if (chk_tableviewL_data != None) and (chk_tableviewL_data == int(self.c_le_pk_s_userm.text())) :
            self.F_maintain(True)
            self.c_le_modify_user.setText(gv.gv_user)
            self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
            self.c_le_user_id.setFocus()
            self.c_le_user_id.selectAll()
            self.update_status = False
            self.c_tv_s_userd.setContextMenuPolicy(Qt.CustomContextMenu)
        else:
            QMessageBox.warning(self, "錯誤!!", "請先選擇左方欲修改或刪除的資料.....\n\n")
    def F_pb_delete(self):
        #Tableview空值或和資料區 資料不一時禁止修改/刪除
        chk_tableviewL_data = self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 0).data()
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
            row = self.c_tv_s_userm.model().rowCount()
            self.c_tv_s_userm.model().insertRow(row)
        else:
            row = self.c_tv_s_userm.currentIndex().row()
        self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 1), self.c_cbb_tv_factory_no.model().index(self.c_cbb_tv_factory_no.currentIndex().row(), 0).data())
        self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 2), self.c_le_user_id.text())
        self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 3), self.c_le_user_nm.text())
        self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 4), self.c_le_user_pswd.text())
        if self.c_rb_user_suspended_Yes.isChecked():
            self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 5), 0)
        else:
            self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 5), 1)
        if self.c_rb_user_marked_1.isChecked():
            self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 7), '1')
        else:
            self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 7), '9')
        self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 8), gv.gv_pk_s_userm)
        self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 9), self.c_le_modify_dt.text())
        # 新增且開啟圖檔，並予儲存, 修改時，若刪除圖檔需清空原本欄位
        if len(self.imgfile) > 0:
            imgfile = QFile(self.imgfile)
            imgfile.open(QIODevice.ReadOnly)
            b64img = QVariant(imgfile.readAll())
            self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 10), b64img)
        elif self.c_pm_user_photo.isNull():
            b64img = ""
            self.c_tv_s_userm.model().setData(self.c_tv_s_userm.model().index(row, 10), b64img)
        if not self.c_tv_s_userm.model().submitAll():
            QMessageBox.critical(self, "錯誤!!", "儲存失敗....\n\n" + self.c_tv_s_userm.model().lastError().text())
            self.c_tv_s_userm.model().revertAll()
            self.c_tv_s_userd.model().revertAll()
        else:
            # 新增儲存時，需取回主檔的 KEY,以便寫入明細檔
            if self.update_status:
                self.c_le_pk_s_userm.setText(str(self.c_tv_s_userm.model().query().lastInsertId()))
                rowR = self.c_tv_s_userd.model().rowCount()     #明細檔 popmenu 新增榼不會寫入KEY,所以手動寫入
                if rowR > 0:
                    for number in range(rowR):
                        self.c_tv_s_userd.model().setData(self.c_tv_s_userd.model().index(number, 1), int(self.c_le_pk_s_userm.text()))
            self.F_maintain(False)
            if not self.c_tv_s_userd.model().submitAll():
                QMessageBox.critical(self, "錯誤!!", "明細資料儲存失敗....\n\n" + self.c_tv_s_userm.model().lastError().text())
            else:
                temp_index = self.c_tv_s_userm.model().match(self.c_tv_s_userm.model().index(0, 0), Qt.DisplayRole,int(self.c_le_pk_s_userm.text()) , 1, Qt.MatchFixedString)
                self.c_tv_s_userm.selectionModel().setCurrentIndex(temp_index[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
                self.F_filter_tv_clicked(self.c_tv_s_userm.currentIndex())

    def F_pb_quit(self):
        if not self.c_pb_save.isVisible():
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
        else:
            self.c_tv_s_userd.setContextMenuPolicy(Qt.NoContextMenu)
            if self.c_le_factory_no.isModified() or  \
                    self.c_le_user_id.isModified() or \
                    self.c_le_user_nm.isModified() or \
                    self.c_le_user_pswd.isModified() :
                QM_replay = QMessageBox.question(self, "訊息!!!", "資料己被更改，是否放棄?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if QM_replay == QMessageBox.Yes:
                    arg = self.c_tv_s_userm.selectedIndexes()
                    if len(arg) >0: self.F_filter_tv_clicked(arg[0])
                    self.F_maintain(False)
            else:
                # 第一次未點選 Tableview 自動選擇 所以 currentIndex 無法取得該值
                arg = self.c_tv_s_userm.selectedIndexes()
                self.F_maintain(False)
                if len(arg) > 0:
                    self.F_filter_tv_clicked(arg[0])

    # def closeEvent(self, QCloseEvent):
    #     QM_replay = QMessageBox.question(self, "訊息!!!", "是否離開？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if QM_replay == QMessageBox.Yes:
    #         QCloseEvent.accept()
    #     else:
    #         QCloseEvent.ignore()

    def F_maintain(self,modify_mark):
        if modify_mark:
            self.c_pb_append.setVisible(False)
            self.c_pb_edit.setVisible(False)
            self.c_pb_delete.setVisible(False)
            self.c_pb_save.setVisible(True)
            self.c_pb_quit.setText("放  棄 (&Q)")
            self.c_pb_append_photo.setVisible(True)
            self.c_pb_delete_photo.setVisible(True)
            self.c_le_tableviewL_filter.setEnabled(False)
            self.c_le_pk_s_userm.setReadOnly(False)
            self.c_cbb_factory_no.setDisabled(False)

            self.c_le_user_id.setReadOnly(False)
            self.c_le_user_nm.setReadOnly(False)
            self.c_le_user_pswd.setReadOnly(False)
            self.c_rb_user_suspended_Yes.setDisabled(False)
            self.c_rb_user_suspended_No.setDisabled(False)
            self.c_rb_user_marked_1.setDisabled(False)
            self.c_rb_user_marked_9.setDisabled(False)

            self.c_tv_s_userm.setEnabled(False)
            #self.c_tv_s_userd.setEnabled(True)
            self.c_tv_s_userd.setEditTriggers(QAbstractItemView.DoubleClicked)
        else:
            self.c_pb_append.setVisible(self.appendstatus)
            self.c_pb_edit.setVisible(self.editstatus)
            self.c_pb_delete.setVisible(self.deletestatus)
            self.c_pb_save.setVisible(False)
            self.c_pb_quit.setText("離  開 (&Q)")
            self.c_pb_append_photo.setVisible(False)
            self.c_pb_delete_photo.setVisible(False)
            self.c_le_tableviewL_filter.setEnabled(True)
            self.c_le_pk_s_userm.setReadOnly(True)
            self.c_cbb_factory_no.setDisabled(True)
            self.c_le_user_id.setReadOnly(True)
            self.c_le_user_nm.setReadOnly(True)
            self.c_le_user_pswd.setReadOnly(True)
            self.c_rb_user_suspended_Yes.setDisabled(True)
            self.c_rb_user_suspended_No.setDisabled(True)
            self.c_rb_user_marked_1.setDisabled(True)
            self.c_rb_user_marked_9.setDisabled(True)

            self.c_tv_s_userm.setEnabled(True)
            #self.c_tv_s_userd.setEnabled(False)
            self.c_tv_s_userd.setEditTriggers(QAbstractItemView.NoEditTriggers)
    def F_pb_append_photo(self):
        photoname=QFileDialog.getOpenFileName(self,"請選擇圖檔","./","*.jpg")
        if self.c_pm_user_photo.load(photoname[0]):
            self.imgfile = photoname[0]
            self.c_lb_user_photo.setPixmap(self.c_pm_user_photo)
        else:
            QMessageBox.critical(self,"警告!","檔案讀取失敗!!")

    def F_pb_delete_photo(self):
        self.c_pm_user_photo=QPixmap()
        self.c_lb_user_photo.setPixmap(self.c_pm_user_photo)

    #@property
    def F_masterform(self):
        c_frame = QFrame(self)
        #c_frame.setGeometry(260, 5, 435, 385)
        c_frame.setFrameShape(QFrame.Box)
        c_frame.setFrameShadow(QFrame.Raised)
        c_frame.setLineWidth(1)
        self.c_lb_user_id = QLabel("使用者ID:",c_frame)
        self.c_lb_user_id.setGeometry(17, 20, 68, 26)
        self.c_lb_user_nm = QLabel("使用者:",c_frame)
        self.c_lb_user_nm.setGeometry(35, 50, 49, 26)
        self.c_lb_user_pswd = QLabel("密碼:",c_frame)
        self.c_lb_user_pswd.setGeometry(50, 80, 34, 26)
        self.c_lb_factory_no = QLabel("廠別代號:",c_frame)
        self.c_lb_factory_no.setGeometry(20, 110, 64, 26)
        self.c_lb_user_suspended = QLabel("停權註記:",c_frame)
        self.c_lb_user_suspended.setGeometry(20, 140, 64, 26)
        self.c_lb_modify_user = QLabel("異動人:",c_frame)
        self.c_lb_modify_user.setGeometry(35, 170, 49, 26)
        self.c_lb_user_marked = QLabel("用戶註記:",c_frame)
        self.c_lb_user_marked.setGeometry(240, 140, 64, 26)
        self.c_lb_modify_dt = QLabel("異動時間:",c_frame)
        self.c_lb_modify_dt.setGeometry(240, 170, 66, 26)
        self.c_le_pk_s_userm = QLineEdit(c_frame)
        self.c_le_factory_no = QLineEdit(c_frame)
        self.c_cbb_factory_no = QComboBox(c_frame)
        self.c_cbb_factory_no.setGeometry(85, 110, 136, 26)

        self.c_le_user_id = udef_object.C_QLineEdit(c_frame, "c_le_user_id",20,"",1, self.F_checkdata)
        self.c_le_user_id.setGeometry(85, 20, 161, 26)
        self.c_le_user_nm =  udef_object.C_QLineEdit(c_frame, "c_le_user_nm",30,"",1, self.F_checkdata)
        self.c_le_user_nm.setGeometry(85, 50, 211, 26)
        self.c_le_user_pswd =  udef_object.C_QLineEdit(c_frame, "c_le_user_pswd",15,"",1, self.F_checkdata)
        self.c_le_user_pswd.setGeometry(85, 80, 186, 26)
        self.c_le_user_pswd.setEchoMode(QLineEdit.Password)

        self.c_le_user_suspended = QLineEdit(c_frame)
        self.c_rb_user_suspended_Yes = QRadioButton("Yes",c_frame)
        self.c_rb_user_suspended_No = QRadioButton("No",c_frame)
        self.c_rb_user_suspended_Yes.setGeometry(85, 140, 50, 26)
        self.c_rb_user_suspended_No.setGeometry(140, 140, 40, 26)
        self.c_bg_user_suspended = QButtonGroup(c_frame)
        self.c_bg_user_suspended.addButton(self.c_rb_user_suspended_Yes)
        self.c_bg_user_suspended.addButton(self.c_rb_user_suspended_No)

        self.c_le_user_marked = QLineEdit(c_frame)
        #self.c_le_user_marked.setGeometry(305, 140, 101, 26)
        self.c_rb_user_marked_1 = QRadioButton("使用",c_frame)
        self.c_rb_user_marked_9 = QRadioButton("管理", c_frame)
        self.c_rb_user_marked_1.setGeometry(305,140,50,26)
        self.c_rb_user_marked_9.setGeometry(360,140,50, 26)
        self.c_bg_user_marked = QButtonGroup(c_frame)
        self.c_bg_user_marked.addButton(self.c_rb_user_marked_1)
        self.c_bg_user_marked.addButton(self.c_rb_user_marked_9)

        self.c_le_modify_user = QLineEdit(c_frame)
        self.c_le_modify_user.setGeometry(85, 170, 116, 26)
        self.c_le_modify_dt = QLineEdit(c_frame)
        self.c_le_modify_dt.setGeometry(305, 170, 125, 26)
        self.c_pm_user_photo = QPixmap()
        self.c_lb_user_photo = QLabel(c_frame)
        self.c_lb_user_photo.setPixmap(self.c_pm_user_photo)
        self.c_lb_user_photo.setGeometry(305, 15, 96, 116)
        self.c_lb_user_photo.setFrameShape(QFrame.Box)
        self.c_lb_user_photo.setFrameShadow(QFrame.Raised)
        self.imgfile = ""

        self.c_le_factory_no.setVisible(False)
        self.c_le_user_suspended.setVisible(False)
        self.c_le_user_marked.setVisible(False)
        self.c_le_pk_s_userm.setVisible(False)
        self.c_le_modify_user.setDisabled(True)
        self.c_le_modify_dt.setDisabled(True)
        # 記錄變更註記
        self.c_pb_append_photo = QPushButton("+", c_frame)
        self.c_pb_append_photo.setGeometry(402, 90, 20, 20)
        self.c_pb_delete_photo = QPushButton("-", c_frame)
        self.c_pb_delete_photo.setGeometry(402, 111, 20, 20)
        #TAB 順序
        c_frame.setTabOrder(self.c_le_user_id, self.c_le_user_nm)
        c_frame.setTabOrder(self.c_le_user_nm, self.c_le_user_pswd)
        c_frame.setTabOrder(self.c_le_user_pswd, self.c_cbb_factory_no)
        c_frame.setTabOrder(self.c_cbb_factory_no, self.c_rb_user_suspended_Yes)
        c_frame.setTabOrder(self.c_rb_user_suspended_Yes, self.c_rb_user_suspended_No)
        c_frame.setTabOrder(self.c_rb_user_suspended_No, self.c_rb_user_marked_1)
        c_frame.setTabOrder(self.c_rb_user_marked_1, self.c_rb_user_marked_9)
        c_frame.setTabOrder(self.c_rb_user_marked_9, self.c_lb_user_photo)

        self.c_cbb_tv_factory_no = db.F_Tableview_kindd(self,"00",2)                    #產生 Factory's Combobox 使用的tableview
        self.c_cbb_factory_no.setModel(self.c_cbb_tv_factory_no.model())      #設置 combobox's tableview 
        self.c_cbb_factory_no.setView(self.c_cbb_tv_factory_no)                             #顯示combobox's view
        self.c_cbb_factory_no.setModelColumn(2)                                                             # 設定 combobox 除顯示欄位也供  setCurrentTXT
        self.c_cbb_factory_no.setEditable(True)                                                                   # 欄位可編輯
        #Detail(TableviewR)
        self.c_tv_s_userd = db.F_QTableView(c_frame,"s_userd","",  ["2|明細資料", "3|資料內容"], [0,1], [100,325],"R",["2|s_kindd|pk_s_kindd|kindd_nm"])
        db.F_Tableview_kindd(self.c_tv_s_userd,"02",2)   # 在 tableview 第 2 欄 資料的下拉
        self.c_tv_s_userd.setGeometry(3, 205, 430, 178)
        self.c_tv_s_userd.setContextMenuPolicy(Qt.NoContextMenu)
        self.c_tv_s_userd.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.c_tv_s_userd.customContextMenuRequested.connect(lambda:db.C_PopMenu(self, self.c_tv_s_userd,["1|{}".format(self.c_le_pk_s_userm.text())],"H"))       
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
        self.c_pb_append_photo.clicked.connect(self.F_pb_append_photo)
        self.c_pb_delete_photo.clicked.connect(self.F_pb_delete_photo)

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
    def F_checkdata(self,temp_objectName):
        temp_return = False
        if temp_objectName == "c_le_user_id":
            if len(self.c_le_user_id.text()) == 0:
                temp_return=(True, "使用者 ID 不可為空....")
            else:
                self.c_sqlquery.exec_("SELECT * FROM s_userm WHERE user_id = '{}'".format(self.c_le_user_id.text()))
                if self.c_sqlquery.next():                   #  不管新增/修改 資料只有一筆
                    if self.update_status:
                        temp_return = (True, "使用者 ID 已存在，不可重複!")
                    elif self.c_sqlquery.value(0) != self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 0).data():
                        temp_return = (True, "使用者 ID 已存在，不可重複!!",self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 2).data())
        elif temp_objectName == "c_le_user_nm":
            if len(self.c_le_user_nm.text()) == 0:
                self.c_le_user_nm.setText(self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 3).data())
                temp_return=(True, "使用者不可為空....")
        else:       #temp_objectName == "c_le_user_pswd"
            if len(self.c_le_user_pswd.text()) == 0:
                self.c_le_user_pswd.setText(self.c_tv_s_userm.model().index(self.c_tv_s_userm.currentIndex().row(), 4).data())
                temp_return=(True, "密碼 不可為空....")
        return temp_return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db.F_DBConnect()
    c_window = C_widget('AED')
    sys.exit(app.exec_())
