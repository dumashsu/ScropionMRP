# -*- coding: utf-8 -*-
'''
程式/資料說明:
第一層的模組代號需由 p_modulem 中而來, 若有子層該子層的模組代號為上一層的程式ID
program_par欄位格式如下:
    4 個參數, 每個參數之間用"|"區隔
    a.程式名稱(ex:p_program)
    b.該程式的Class名稱
    c.視窗尺寸(寬,高)
    d.程式權限新增/修改/刪除/查詢/列印,各以AEDFP來代表組成

若要匯入資料代替人手工建立, 請參考 s_program.py及mainmenu.py 說明    
'''
from PyQt5.Qt import Qt, QCursor
from PyQt5.QtCore import QDateTime, QItemSelectionModel
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QTreeWidget, QTreeWidgetItem, QDesktopWidget, QLineEdit, QLabel, QTextEdit, QCheckBox, QMessageBox, \
                            QMenu, QComboBox, QHBoxLayout, QSplitter
import db
import gv
import sys
import udef_object


class  C_widget(QWidget):
    def  __init__(self,limited,parent=None):
        QWidget.__init__(self,parent)
        gv.F_define_button(self,limited)
        self.setStyleSheet(gv.gv_bg_font)
        #視窗置中
        self.setGeometry((QDesktopWidget().availableGeometry().width()-800)/2,(QDesktopWidget().availableGeometry().height()-380)/2,800,380)
        self.setWindowTitle("選單資料維護")
        main_hbox = QHBoxLayout(self)
        main_hbox.setContentsMargins(2, 2, 2, 2)
        main_hbox.setSpacing(2)
        #左邊 Treewidget
        main_spliter = QSplitter(Qt.Horizontal)
        main_spliter.addWidget(self.F_treewidget())
        main_spliter.addWidget(self.F_freeform())
        main_spliter.setStretchFactor(0,1)
        main_spliter.setStretchFactor(1,3)
        main_hbox.addWidget(main_spliter)   #.setLayout(main_hbox)
        self.maintain_status = False
        self.update_status = True
        self.maintance()
        # 首次進入則開啟第一筆資料
        if self.c_treewidget.model().rowCount() > 0:
            self.c_treewidget.selectionModel().setCurrentIndex(self.c_treewidget.model().index(0, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows)
            self.F_viewclicked(self.c_treewidget.currentItem())
        self.show()

    def F_viewclicked(self,item):
        # 傳入 item, column
        #修改狀態下 不可改變 treeview's 值，若非則隨點擊的值來顯示明細資料
        if self.maintain_status:
            QMessageBox.critical(self, "錯誤!!", "資料編緝中，請先儲存或放棄...\n\n")
            self.c_treewidget.setCurrentItem(self.v_modifyindex)
        else:
            self.v_modifyindex = self.c_treewidget.currentItem()
            if item.parent() is None:
                self.c_le_program_no.setText("")
                self.c_le_program_seq.setText("")
                self.c_le_program_nm.setText("")
                self.c_le_program_id.setText("")
                self.c_le_program_par.setText("")
                self.c_cbb_program_wintype.setCurrentIndex(1)
                self.c_cb_program_effective.setChecked(False)
                self.c_te_program_memo.setText("")
                self.c_le_modify_user.setText(gv.gv_user)
                self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
            else:
                self.c_sqlquery.exec_("SELECT * FROM s_programd WHERE pk_s_programd = {}".format(int(item.text(1))))
                if self.c_sqlquery.next():
                    self.c_le_program_no.setText(self.c_sqlquery.value(2))
                    self.c_le_program_seq.setText("%d" % self.c_sqlquery.value(3))
                    self.c_le_program_nm.setText(self.c_sqlquery.value(4))
                    self.c_le_program_id.setText(self.c_sqlquery.value(5))
                    self.c_le_program_par.setText(self.c_sqlquery.value(6))
                    self.c_cbb_program_wintype.setCurrentIndex(self.c_cbb_program_wintype.findText(self.c_sqlquery.value(7),Qt.MatchContains))
                    self.c_cb_program_effective.setChecked(True if self.c_sqlquery.value(8) else False)
                    self.c_te_program_memo.setText(self.c_sqlquery.value(9))
                    self.c_le_modify_user.setText(db.F_get_user_nm(self.c_sqlquery.value(10)))
                    self.c_le_modify_dt.setText(self.c_sqlquery.value(11))
    def F_PopMenu(self, v_viewpos):
        v_viewpos.menu = QMenu()
        v_viewpos.menu.setStyleSheet(gv.gv_bg_font)
        if not self.maintain_status:
            pop_append = v_viewpos.menu.addAction("新增")
            pop_append.triggered.connect(self.F_pop_append)
            pop_edit = v_viewpos.menu.addAction("修改")
            pop_edit.triggered.connect(self.F_pop_edit)
            pop_delete = v_viewpos.menu.addAction("刪除")
            pop_delete.triggered.connect(self.F_pop_delete)
            v_viewpos.menu.addSeparator()
            pop_exit = v_viewpos.menu.addAction("離開")
            pop_exit.triggered.connect(self.F_pop_quit)
            pop_append.setVisible(self.appendstatus)
            pop_edit.setVisible(self.editstatus)
            pop_delete.setVisible(self.deletestatus)
        else:
            pop_save = v_viewpos.menu.addAction("儲存")
            pop_save.triggered.connect(self.F_pop_save)

            pop_exit = v_viewpos.menu.addAction("放棄")
            pop_exit.triggered.connect(self.F_pop_quit)
        v_viewpos.menu.exec_(QCursor.pos())
    #點選右鍵新增
    def F_pop_append(self):
        self.maintain_status = True
        self.update_status = True
        self.maintance()
        self.c_le_program_no.setText(self.v_modifyindex.text(3))
        self.c_le_program_seq.setText("")
        self.c_le_program_nm.setText("")
        self.c_le_program_id.setText("")
        self.c_le_program_par.setText("")
        self.c_cbb_program_wintype.setCurrentIndex(1)
        self.c_cb_program_effective.setChecked(False)
        self.c_te_program_memo.setText("")

    #點選右鍵修改
    def F_pop_edit(self):
        if self.v_modifyindex.data(1,0) == None:
            QMessageBox.warning(self, "警告!!", "模組資料禁止修改...請至模組維護作業\n\n" )
        else:
            self.update_status = False
            self.maintain_status = True
            self.maintance()

    #點選右鍵刪除
    def F_pop_delete(self):
        #self.maintance()
        if self.v_modifyindex.data(1,0) == None:
            QMessageBox.warning(self, "警告!!", "模組資料禁止刪除...請至模組維護作業\n\n")
        else:
            if self.v_modifyindex.childCount() == 0:        #無子項目方可刪除
                QM_replay = QMessageBox.question(self, "訊息!!!", "請再次確認是否刪除?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if QM_replay == QMessageBox.Yes:
                    sql = "DELETE FROM s_programd WHERE pk_s_programd = {}".format(int(self.v_modifyindex.text(1)))
                    if not self.c_sqlquery.prepare(sql):
                        QMessageBox.critical(self, "錯誤!!", "刪除失敗....\n\n" + self.c_sqlquery.lastError().text())
                    else:
                        self.c_sqlquery.exec_()
                        self.v_modifyindex.parent().removeChild(self.v_modifyindex)
                        self.v_modifyindex = self.c_treewidget.currentItem()
                        self.F_viewclicked(self.v_modifyindex)
            else:
                QMessageBox.warning(self, "警告！！", "尚有子項目禁止刪除....\n\n" )

    def F_pop_save(self,index):
        if self.update_status:
            sql = "INSERT INTO s_programd (pk_s_modulem,program_no,program_seq,program_nm,program_id,program_par,program_wintype,program_effective,program_memo,modify_user,modify_dt) VALUES " \
                  "(:pk_s_modulem,:program_no,:program_seq,:program_nm,:program_id,:program_par,:program_wintype,:program_effective,:program_memo,:modify_user,:modify_dt)"
        else:
            sql = "UPDATE s_programd SET " \
                  "program_no = :program_no, " \
                  "program_seq = :program_seq, " \
                  "program_nm = :program_nm," \
                  "program_id = :program_id," \
                  "program_par = :program_par," \
                  "program_wintype = :program_wintype," \
                  "program_effective = :program_effective," \
                  "program_memo = :program_memo," \
                  "modify_user = :modify_user," \
                  "modify_dt = :modify_dt " \
                  "WHERE pk_s_programd = {}".format(int(self.c_treewidget.currentItem().data(1, 0)))
        if self.c_sqlquery.prepare(sql):
            self.c_sqlquery.bindValue(":pk_s_modulem",self.v_modifyindex.data(2, 0))
            self.c_sqlquery.bindValue(":program_no",self.c_le_program_no.text())
            self.c_sqlquery.bindValue(":program_seq",self.c_le_program_seq.text())
            self.c_sqlquery.bindValue(":program_nm",self.c_le_program_nm.text())
            self.c_sqlquery.bindValue(":program_id",self.c_le_program_id.text())
            self.c_sqlquery.bindValue(":program_par",self.c_le_program_par.text())
            self.c_sqlquery.bindValue(":program_wintype",str(self.c_cbb_program_wintype.currentIndex()))
            self.c_sqlquery.bindValue(":program_effective",1 if self.c_cb_program_effective.isChecked() else 0)
            self.c_sqlquery.bindValue(":program_memo",self.c_te_program_memo.toPlainText())
            self.c_sqlquery.bindValue(":modify_user",gv.gv_pk_s_userm)
            self.c_sqlquery.bindValue(":modify_dt",self.c_le_modify_dt.text())

            if not self.c_sqlquery.exec_():
                QMessageBox.critical(self, "錯誤!!", "儲存失敗.資料有誤.....\n\n" + self.c_sqlquery.lastError().text())
            else:
                self.maintain_status = False
                self.maintance()
                if self.update_status:
                    # 依 program_no 找節點，找到歸屬它，沒有則以 parent()，欄位若關閉 會找不到
                    temp_parent = self.c_treewidget.findItems(self.c_le_program_no.text(), Qt.MatchFixedString | Qt.MatchRecursive, 3)
                    if len(temp_parent) == 0:
                        temp_twi = QTreeWidgetItem(self.v_modifyindex)
                    else:
                        if temp_parent[0].parent() == None:  # 第一層新增無上一層，故以本身為第一層
                            temp_twi = QTreeWidgetItem(temp_parent[0])
                        else:
                            temp_twi = QTreeWidgetItem(temp_parent[0].parent())
                    temp_twi.setText(0, self.c_le_program_nm.text())
                    temp_twi.setText(1, str(self.c_sqlquery.lastInsertId()))        #取回新增之 ID
                    temp_twi.setText(2, self.v_modifyindex.data(2, 0))
                    temp_twi.setText(3, self.c_le_program_no.text())
                    self.c_treewidget.setCurrentItem(temp_twi)
                    self.c_treewidget.expand(self.c_treewidget.currentIndex())
                    self.F_viewclicked(temp_twi)
                else:
                    if self.v_modifyindex.data(3, 0) != self.c_le_program_no.text():  # program_no 變更，樹也需變更 為取得原相關Key值故先新增後刪除
                        temp_parent = self.c_treewidget.findItems(self.c_le_program_no.text(), Qt.MatchFixedString | Qt.MatchRecursive, 3)
                        if len(temp_parent) == 0:
                            temp_twi = QTreeWidgetItem(self.v_modifyindex)
                        else:
                            if temp_parent[0].parent() == None:  # 第一層新增無上一層，故以本身為第一層
                                temp_twi = QTreeWidgetItem(temp_parent[0])
                            else:
                                temp_twi = QTreeWidgetItem(temp_parent[0].parent())
                        temp_twi.setText(0, self.c_le_program_nm.text())
                        temp_twi.setText(1, self.v_modifyindex.data(1, 0))
                        temp_twi.setText(2, self.v_modifyindex.data(2, 0))
                        temp_twi.setText(3, self.c_le_program_no.text())
                        self.v_modifyindex.parent().removeChild(self.v_modifyindex)  # 刪除
                        self.c_treewidget.setCurrentItem(temp_twi)
                        self.c_treewidget.expand(self.c_treewidget.currentIndex())
                        self.F_viewclicked(temp_twi)
                    else:
                        self.v_modifyindex.setText(0, self.c_le_program_nm.text())
        else:
            QMessageBox.critical(self, "錯誤!!", "儲存失敗.\n\n" + self.c_sqlquery.lastError().text())
    def F_pop_quit(self):
        if self.maintain_status:
            self.maintain_status = False
            self.maintance()
            self.F_viewclicked(self.v_modifyindex)
        else:
            if self.parent() == None:
                self.close()
            else:
                self.parent().close()
    # def closeEvent(self, QCloseEvent):
    #     QM_replay = QMessageBox.question(self, "訊息!!!", "是否離開？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if QM_replay == QMessageBox.Yes:
    #         QCloseEvent.accept()
    #     else:
    #         QCloseEvent.ignore()
    def maintance(self):
        if self.maintain_status:
            self.c_le_program_no.setReadOnly(False)
            self.c_le_program_seq.setReadOnly(False)
            self.c_le_program_nm.setReadOnly(False)
            self.c_le_program_id.setReadOnly(False)
            self.c_le_program_par.setReadOnly(False)
            self.c_cbb_program_wintype.setDisabled(False)
            self.c_cb_program_effective.setDisabled(False)
            self.c_te_program_memo.setReadOnly(False)
            self.c_le_program_no.setFocus()
            self.c_le_modify_user.setText(gv.gv_user)
            self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
        else:    #查詢
            self.c_le_program_no.setReadOnly(True)
            self.c_le_program_seq.setReadOnly(True)
            self.c_le_program_nm.setReadOnly(True)
            self.c_le_program_id.setReadOnly(True)
            self.c_le_program_par.setReadOnly(True)
            self.c_cbb_program_wintype.setDisabled(True)
            self.c_cb_program_effective.setDisabled(True)
            self.c_te_program_memo.setReadOnly(True)
        # 設舊值好輸入錯誤時可還原
        self.src_program_id = self.c_le_program_id.text()
        self.src_program_nm = self.c_le_program_nm.text()
    def F_treewidget(self):
        self.c_treewidget = QTreeWidget(self)
        self.c_treewidget.setColumnCount(5)
        self.c_treewidget.hideColumn(1)
        self.c_treewidget.hideColumn(2)
        self.c_treewidget.hideColumn(3)
        self.c_treewidget.hideColumn(4)
        self.c_treewidget.setHeaderHidden(True)
        #self.setStyleSheet(gv.gv_bg_font)
        #self.c_treewidget.setMaximumWidth(360)
        #self.c_treewidget.setGeometry(5, 5, 360, 370)

        temp_menunode = []
        temp_menuvalue = []
        self.c_sqlquery = QSqlQuery()
        self.c_sqlquery.exec("SELECT * FROM s_modulem ORDER BY module_seq ASC")
        while self.c_sqlquery.next():
            temp_menunode.append(self.c_sqlquery.value(2))          #module_no
            temp_twi = QTreeWidgetItem(self.c_treewidget)
            temp_twi.setText(0,self.c_sqlquery.value(4))        #module_nm
            temp_twi.setText(2,str(self.c_sqlquery.value(0)))   #pk_s_modulem
            temp_twi.setText(3,self.c_sqlquery.value(2))        #modulem_no
            temp_menuvalue.append(temp_twi)
        # 子系統的節點和程式選單
        self.c_sqlquery.exec("SELECT * FROM s_programd ORDER BY program_no ASC, program_seq ASC, program_id ASC")
        while self.c_sqlquery.next():
            if self.c_sqlquery.value(2) in temp_menunode:               # program_no 已存在 node 內
                temp_parent = temp_menuvalue[temp_menunode.index(self.c_sqlquery.value(2))]
            else:                                                   # 沒有 node 但需先找到上一層 porgram_id
                temp_parent = self.c_treewidget.findItems(self.c_sqlquery.value(2), Qt.MatchFixedString | Qt.MatchRecursive, 4)
                if len(temp_parent) > 0:
                    temp_parent = temp_parent[0]
                    temp_menunode.append(self.c_sqlquery.value(2))
                    temp_menuvalue.append(temp_parent)
                else:
                    QMessageBox.critical(self,"錯誤!!","樹狀資料有問題，找不到上層({}-{})資料".format(self.c_sqlquery.value(0),self.c_sqlquery.value(2)))
                    break
            temp_twi = QTreeWidgetItem(temp_parent)             # program_no
            temp_twi.setText(0, self.c_sqlquery.value(4))       # program_nm
            temp_twi.setText(1, str(self.c_sqlquery.value(0)))  # pk_s_programd
            temp_twi.setText(2, str(self.c_sqlquery.value(1)))  # pk_s_modulem
            temp_twi.setText(3, self.c_sqlquery.value(2))       # program_no           新增時使用
            temp_twi.setText(4,self.c_sqlquery.value(5))        # program_id
        self.c_treewidget.itemClicked.connect(self.F_viewclicked)
        self.c_treewidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.c_treewidget.customContextMenuRequested.connect(self.F_PopMenu)
        return self.c_treewidget

    def F_freeform(self):
        c_frame = QFrame(self)
        #c_frame.setGeometry(365, 5, 430, 370)
        c_frame.setFrameShape(QFrame.Box)
        c_frame.setFrameShadow(QFrame.Raised)
        c_frame.setLineWidth(1)
        # self.c_lb_module_no = QLabel("模組代號:",c_frame)
        # self.c_lb_module_no.setGeometry(10, 10, 71, 26)
        self.c_lb_program_no = QLabel("選單代號:",c_frame)
        self.c_lb_program_no.setGeometry(10, 10, 71, 26)
        self.c_lb_program_seq = QLabel("排列序號:",c_frame)
        self.c_lb_program_seq.setGeometry(305, 40, 71, 26)
        self.c_lb_program_id = QLabel("程式ID:", c_frame)
        self.c_lb_program_id.setGeometry(24, 40, 71, 26)
        self.c_lb_program_nm = QLabel("程式名稱:",c_frame)
        self.c_lb_program_nm.setGeometry(10, 70, 71, 26)
        self.c_lb_program_nm.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.c_lb_program_par = QLabel("程式參數:",c_frame)
        self.c_lb_program_par.setGeometry(10, 100, 71, 26)
        self.c_lb_program_wintype = QLabel("視窗型態:",c_frame)
        self.c_lb_program_wintype.setGeometry(10, 130, 71, 26)
        self.c_lb_program_memo = QLabel("說        明:",c_frame)
        self.c_lb_program_memo.setGeometry(10, 160, 71, 26)
        self.c_lb_modify_user = QLabel("異動人:",c_frame)
        self.c_lb_modify_user.setGeometry(25, 335, 49, 26)
        self.c_lb_modify_dt = QLabel("異動時間:", c_frame)
        self.c_lb_modify_dt.setGeometry(230, 335, 66, 26)

        self.c_le_program_no = udef_object.C_QLineEdit(c_frame, "c_le_program_no",8,"",1, self.F_checkdata)    #QLineEdit(c_frame)
        self.c_le_program_no.setGeometry(75, 10, 96, 26)
        self.c_le_program_no.setObjectName("c_le_program_no")
        self.c_le_program_id = udef_object.C_QLineEdit(c_frame, "c_le_program_id",8,"",1, self.F_checkdata)         #QLineEdit(c_frame)
        self.c_le_program_id.setGeometry(75, 40, 144, 26)
        self.c_le_program_id.setObjectName("c_le_program_id")
        self.c_le_program_seq = udef_object.C_QLineEdit(c_frame, "c_le_program_seq",4,"9999",1, self.F_checkdata)
        self.c_le_program_seq.setGeometry(370, 40, 48, 26)
        self.c_le_program_seq.setObjectName("c_le_program_seq")
        self.c_le_program_nm = udef_object.C_QLineEdit(c_frame, "c_le_program_nm",50,"",1, self.F_checkdata)
        self.c_le_program_nm.setGeometry(75, 70, 346, 26)
        self.c_le_program_nm.setObjectName("c_le_program_nm")
        self.c_le_program_par = udef_object.C_QLineEdit(c_frame, "c_le_program_par",50,"",1, self.F_checkdata)
        self.c_le_program_par.setGeometry(75, 100, 346, 26)
        self.c_le_program_par.setObjectName("c_le_program_par")
        self.c_cbb_program_wintype = QComboBox(c_frame)
        self.c_cbb_program_wintype.addItem("0.最小化")
        self.c_cbb_program_wintype.addItem("1.自訂視窗")
        self.c_cbb_program_wintype.addItem("2.最大化")
        self.c_cbb_program_wintype.setCurrentIndex(1)     # defaule   1.自訂視窗
        self.c_cbb_program_wintype.setGeometry(75, 130, 141, 26)
        self.c_cb_program_effective = QCheckBox("生效註記",c_frame)
        self.c_cb_program_effective.setGeometry(325, 130, 91, 24)
        self.c_cb_program_effective.setLayoutDirection(Qt.LeftToRight)
        self.c_te_program_memo = QTextEdit(c_frame)
        self.c_te_program_memo.setGeometry(75, 165, 346, 166)
        self.c_te_program_memo.setObjectName("c_te_program_memo")
        self.c_le_modify_user = QLineEdit(c_frame)
        self.c_le_modify_user.setGeometry(75, 335, 116, 26)
        self.c_le_modify_dt = QLineEdit(c_frame)
        self.c_le_modify_dt.setGeometry(295, 335, 125, 26)

        self.c_le_modify_user.setDisabled(True)
        self.c_le_modify_dt.setDisabled(True)

        #TAB 順序
        # c_frame.setTabOrder(self.c_le_module_no, self.c_le_module_nm)
        # c_frame.setTabOrder(self.c_le_module_nm, self.c_le_program_no)
        c_frame.setTabOrder(self.c_le_program_no, self.c_le_program_id)
        c_frame.setTabOrder(self.c_le_program_id, self.c_le_program_seq)
        c_frame.setTabOrder(self.c_le_program_seq, self.c_le_program_nm)
        c_frame.setTabOrder(self.c_le_program_nm, self.c_le_program_par)
        c_frame.setTabOrder(self.c_le_program_par, self.c_cbb_program_wintype)
        c_frame.setTabOrder(self.c_cbb_program_wintype, self.c_cb_program_effective)
        c_frame.setTabOrder(self.c_cb_program_effective, self.c_te_program_memo)
        c_frame.setTabOrder(self.c_te_program_memo, self.c_le_modify_user)
        c_frame.setTabOrder(self.c_le_modify_user, self.c_le_modify_dt)

        c_frame.setContextMenuPolicy(Qt.CustomContextMenu)
        c_frame.customContextMenuRequested.connect(self.F_PopMenu)
        # freeform 欄位和顯示, 內部變數調用時需加位 class 名稱
        return c_frame
    def F_checkdata(self,objectName):    #各欄位需檢查的判斷式寫在這理
        #return False
        temp_return = False
        if objectName == "c_le_program_seq":
            temp_return=False if self.c_le_program_seq.text().isnumeric() else (True,"請輸入數字....")
        elif objectName == "c_le_program_no":
            return False if len(self.c_le_program_no.text())!=0 else (True, "選單代號不可為空....")
        elif objectName == "c_le_program_id":
            if len(self.c_le_program_id.text()) == 0:
                temp_return=(True, "程式ID不可為空....")
            else:
                self.c_sqlquery.exec_("SELECT * FROM s_programd WHERE program_id = '{}'".format(self.c_le_program_id.text()))
                if self.c_sqlquery.numRowsAffected() > 0:
                    if self.update_status:      #新增
                        temp_return = (True,"程式ID已存在，不可重複!")
                    else:
                        while self.c_sqlquery.next():       # 找到相同的內容，並過濾自已本身的值，若不同表示重複
                            if self.c_sqlquery.value(0) != int(self.c_treewidget.currentItem().data(1, 0)):
                                temp_return = (True,"程式ID已存在，不可重複!!",self.src_program_id)
                                break
                else:
                    temp_return = False
        elif  objectName == "c_le_program_nm":
            if len(self.c_le_program_nm.text()) == 0:
                temp_return=(True, "程式名稱不可為空....")
            else:
                self.c_sqlquery.exec_("SELECT * FROM s_programd WHERE program_nm = '{}'".format(self.c_le_program_nm.text()))
                if self.c_sqlquery.numRowsAffected() > 0:
                    if self.update_status:      #新增
                        temp_return = (True,"程式名稱已存在，不可重複!")
                    else:
                        while self.c_sqlquery.next():       # 找到相同的內容，並過濾自已本身的主KEY，若有值表重複
                            if self.c_sqlquery.value(0) != int(self.c_treewidget.currentItem().data(1, 0)):
                                temp_return = (True,"程式名稱已存在，不可重複!! %d" % self.c_sqlquery.value(0),self.src_program_nm)
                                break
                else:
                    temp_return = False
        return temp_return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db.F_DBConnect()
    window = C_widget('AED')
    sys.exit(app.exec_())