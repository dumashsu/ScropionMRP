# -*- coding: utf-8 -*-
# 打算由 treewidget 點選執行程式，不過 subwindow 卻在 treewidget 後方，若要可以用必需將 treewidget lower(),但一lower() 就不能選擇。所以卡關
'''
建立系統作業說明
1.開啟 pgAdmin 來匯入類別主檔的4筆資料,匯入時 pk 不要勾選, 分隔號選擇";" (可執行 system.py 來建立)
2.先執行 p_userm 建立使用者, 取其 pk 後更新 gv.gv_pk_s_userm 的值, 來做為登入者的設定
3.建立模組資料(p_modulem)
    a.建立9999 的系統維護模組, 並取出 pk
    b.開啟 pgAdmin 匯入"s_program.csv",匯入時pk和時間不要勾選,而格式請選擇";", 檔案內第一欄是"9999"的PK值, 若不一樣記得更改
4.建立程式資料(p_program)可參考 system.py 來建立或者手動輸入
5.建立使用者(p_userlimited)或群組(p_groupuser)權限, 群組需先在類別主(03)/明細中建立

'''
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QBrush, QColor, QIcon, QPixmap, QKeySequence
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QStatusBar, QMainWindow, QTextEdit, QHBoxLayout, \
                                                       QAction, QDialog, QDesktopWidget, QFrame, QMdiArea, QMdiSubWindow, QMessageBox, QLineEdit, QLabel, QDockWidget, \
                                                       QPushButton, QSplitter
import db
import gv
import sys
import udef_object
 
class  C_mainmenu(QMainWindow):
    def  __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.db = db.F_DBConnect()
        if self.db.lastError():
            self.close()
        self.c_sqlquery = QSqlQuery()
        self.setStyleSheet(gv.gv_bg_font)       #在 Pydev 上會造成 subwindow 最大化後關閉視窗,會卡住
        #self.setFont(gv.gv_font)
        self.setWindowTitle("S MRPII 作業")
        self.setGeometry((QDesktopWidget().availableGeometry().width() - 1024) / 2, (QDesktopWidget().availableGeometry().height() - 768) / 2, 1024, 768)
        self.widget = QWidget(self)
        main_splitter = QSplitter(Qt.Horizontal,self)
        self.c_te_widget = QTextEdit()
        self.c_te_widget.setReadOnly(True)
        self.c_te_widget.setFrameShape(QFrame.WinPanel)
        self.c_te_widget.setFrameShadow(QFrame.Raised)
        self.c_treewidget = QTreeWidget(self.widget)
        main_splitter.addWidget(self.c_treewidget)
        # Mainwindow's MDI 所有物件可以置其上，所以需配合 centralwidget 將其置中
        self.c_mdiarea = QMdiArea(self)
        #brush = QBrush(QColor(221, 221, 221))
        #brush.setStyle(Qt.NoBrush)
        #self.c_mdiarea.setBackground(brush)
        main_splitter.addWidget(self.c_mdiarea)

        #顯示圖檔
        #self.c_mdiarea.setBackground(QBrush(QPixmap(gv.gv_imagepath+"scorpion.jpeg")))
        main_splitter.setStretchFactor(1,4)
        self.setCentralWidget(main_splitter)        #self.widget)
        # status bar
        self.c_statusbar = QStatusBar(self)
        self.setStatusBar(self.c_statusbar)
        self.c_lb_statusbarl = QLabel()
        self.c_lb_statusbarr = QLabel(QDateTime().currentDateTime().toString("yyyy/MM/dd"))
        self.c_lb_statusbarl.setAlignment(Qt.AlignLeft)
        self.c_lb_statusbarr.setAlignment(Qt.AlignRight)
        self.c_statusbar.addWidget(self.c_lb_statusbarl,1)
        self.c_statusbar.addWidget(self.c_lb_statusbarr,1)
        self.sublist = []
        self.menuactionlist = []
        self.F_menubar()
        #self.F_login()
        self.F_treewidget()
        self.menubar.setVisible(True)
        self.c_treewidget.setVisible(True)
        self.show()
    def F_menubar(self):
        self.menubar = self.menuBar()
        menuSystem = self.menubar.addMenu("系統")
        self.menuWindows = self.menubar.addMenu("選單")
        menuHelp = self.menubar.addMenu("求助")
        #menuSystem's submenu
        menuSystem.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/menu.png'),"選單隱藏(&H)",
                                self,shortcut="Ctrl+H",statusTip="顯示/隱藏選單",triggered=self.F_am_hidemenu))
        menuSystem.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/changepassword.png'),"變更密碼(&P)",
                                self,shortcut="Ctrl+P",statusTip="變更密碼",triggered=self.F_am_changepassword))
        menuSystem.addSeparator()
        menuSystem.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/login.png'),"登出(&L)",
                                self,shortcut="Ctrl+L",statusTip="重新登入其它帳號",triggered=self.F_am_logout))
        menuSystem.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/quit.png'),"離開(&Q)",
                                self,shortcut="Ctrl+Q",statusTip="離開",triggered=self.F_login_cancel))
        menuHelp.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/cascadewindow2.png'), "視窗堆疊化(&A)",
                                self,shortcut="Ctrl+A",statusTip="堆疊顯示所有視窗",triggered=self.F_am_cascadewindow))
        menuHelp.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/titlewindow.png'), "視窗標題化(&T)",
                                self,shortcut="Ctrl+T",statusTip="標列顯示所有視窗",triggered=self.F_am_titlewindow))
        menuHelp.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/miniscreen.png'), "視窗最小化(&i)",
                                self,shortcut="Ctrl+N",statusTip="最小化顯示所有視窗",triggered=self.F_am_miniwindow))
        menuHelp.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/maxiscreen.png'), "視窗最大化(&M)",
                                self,shortcut="Ctrl+M",statusTip="最大化顯示所有視窗",triggered=self.F_am_maxiwindow))
        menuHelp.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/closewindow.png'), "關閉所有視窗(&O)",
                                self,shortcut="Ctrl+C",statusTip="關閉示所有視窗",triggered=self.F_am_closeallwindow))
        menuHelp.addSeparator()
        menuHelp.addAction(QAction(QIcon(gv.gv_imagepath+'mainwindow/help.png'),"幫助(&H)",
                                self,shortcut="F1",statusTip="幫助",triggered=self.F_am_help))
        self.menubar.addAction(menuSystem.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())
        self.menubar.addAction(menuHelp.menuAction())
        self.setMenuBar(self.menubar)
        self.menuWindows.triggered[QAction].connect(self.F_menuWindows)

    def F_menuWindows(self,actionName):
        for number in range(len(self.menuactionlist)):
            if self.menuactionlist[number].text() == actionName.text():
                self.c_mdiarea.setActiveSubWindow(self.sublist[number])
                break
    def F_am_changepassword(self):
        pass
    def F_am_hidemenu(self):
        self.c_treewidget.setVisible(not self.c_treewidget.isVisible())
    def F_am_logout(self):
        winnumber = len(self.menuactionlist)
        while winnumber > 0:
            winnumber -= 1
            self.c_mdiarea.setActiveSubWindow(self.sublist[winnumber])
            self.subclose("Quit")
        self.menubar.setVisible(False)
        self.c_treewidget.setVisible(False)
        self.F_login()
    def F_am_cascadewindow(self):
        for number in range(len(self.sublist)):
            self.c_mdiarea.setActiveSubWindow(self.sublist[number])
            self.sublist[number].setWindowState(Qt.WindowMaximized)
        self.c_mdiarea.cascadeSubWindows()
    def F_am_titlewindow(self):
        for number in range(len(self.sublist)):
            self.c_mdiarea.setActiveSubWindow(self.sublist[number])
            self.sublist[number].setWindowState(Qt.WindowMaximized)
        self.c_mdiarea.tileSubWindows()
    def F_am_miniwindow(self):
        for number in range(len(self.sublist)):
            self.c_mdiarea.setActiveSubWindow(self.sublist[number])
            self.sublist[number].setWindowState(Qt.WindowMinimized)
    def F_am_maxiwindow(self):
        for number in range(len(self.sublist)):
            self.c_mdiarea.setActiveSubWindow(self.sublist[number])
            self.sublist[number].setWindowState(Qt.WindowMaximized)
    def F_am_closeallwindow(self):
        # 不使用 CloseAllsubwindow 仍然會觸發 subclose 所以就一個個來刪
        winnumber = len(self.menuactionlist)
        while winnumber > 0:
            winnumber -= 1
            self.c_mdiarea.setActiveSubWindow(self.sublist[winnumber])
            self.subclose("Quit")
    def F_am_help(self):
        helpdialog = QDialog()
        helpdialog.resize(300,170)
        helpdialog_te = QTextEdit(helpdialog)
        hbox = QHBoxLayout(helpdialog)
        hbox.setContentsMargins(2,2,2,2)
        helpdialog_te.setText("S MRP2   1.0\n\n"
                                "以 Python 3.5 + PyQt5 + PostgreSQL 編寫,"
                                "程式免費提供個人學習,商業使用請先取得本人同意.\n\n"
                                "程式皆由網上學習再加個人數年電腦化經驗而成，若有錯誤也請不吝告知.\n"
                                "dumas.hsu@gmail.com")
        helpdialog_te.setReadOnly(True)
        hbox.addWidget(helpdialog_te)
        #helpdialog_te.move(0, 0)
        helpdialog.setWindowTitle("Help")
        helpdialog.setWindowModality(Qt.ApplicationModal)
        helpdialog.exec_()
    def F_login(self):
        self.loginnum = 1
        self.c_statusbar.showMessage("請輸入帳號和密碼!",3000)
        self.menubar.setVisible(False)
        self.c_treewidget.setVisible(False)
        self.c_dw = QDockWidget(self)
        self.c_dw.setWindowTitle("登錄作業!!")
        #self.c_dw.setFont(gv.gv_font)
        self.c_dw.setFeatures(QDockWidget.NoDockWidgetFeatures)  # | QDockWidget.DockWidgetClosable)
        self.c_dw.setAllowedAreas(Qt.NoDockWidgetArea)
        self.c_dw.setFloating(True)
        self.c_dw.changeEvent = self.F_login_cancel
        self.c_dw.activateWindow()      #取得 focus
        c_dw_frame = QFrame()
        c_dw_frame.setFrameShadow(QFrame.Raised)
        c_dw_frame.setFrameShape(QFrame.Box)
        c_lb_login = QLabel("帳號:", c_dw_frame)
        c_lb_login.setGeometry(105, 70, 35, 26)
        c_lb_paswd = QLabel("密碼:", c_dw_frame)
        c_lb_paswd.setGeometry(105, 120, 35, 26)
        self.c_le_login = udef_object.C_QLineEdit(c_dw_frame, "c_le_login", 15, "",0, self.F_checkdata)
        self.c_le_paswd = udef_object.C_QLineEdit(c_dw_frame, "c_le_paswd", 15, "",0, self.F_checkdata)
        self.c_le_paswd.setEchoMode(QLineEdit.Password)
        self.c_le_paswd.setGeometry(140, 120, 150, 26)
        self.c_le_login.setGeometry(140, 70, 150, 26)
        c_pb_ok = QPushButton("登錄(&L)", c_dw_frame)
        c_pb_ok.setGeometry(100, 200, 91, 24)
        c_pb_cancel = QPushButton("離開(&Q)", c_dw_frame)
        c_pb_cancel.setGeometry(210, 200, 91, 24)
        c_pb_ok.clicked.connect(self.F_login_ok)
        c_pb_cancel.clicked.connect(self.F_login_cancel)
        self.c_dw.setWidget(c_dw_frame)
        self.c_dw.show()
        self.c_dw.setGeometry((QDesktopWidget().availableGeometry().width() - 420) / 2, (QDesktopWidget().availableGeometry().height() - 300) / 2, 420, 300)
    def F_login_ok(self):
        self.c_sqlquery.exec_("SELECT * FROM s_userm WHERE user_id = '{}'".format(self.c_le_login.text()))
        if self.c_sqlquery.next():
            if self.c_le_paswd.text() == self.c_sqlquery.value(4):
                gv.gv_id = self.c_sqlquery.value(2)
                gv.gv_user = self.c_sqlquery.value(3)
                gv.gv_pk_s_userm = self.c_sqlquery.value(0)
                self.c_dw.close()
                self.F_treewidget()
                self.menubar.setVisible(True)
                self.c_treewidget.setVisible(True)
                self.c_lb_statusbarl.setText("使用者:{}({})".format(gv.gv_id,gv.gv_user))
                #self.c_statusbar.showMessage("請點擊功能或者由System中離開系統",3000)
                #self.c_le_modify_dt.setText(QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
            else:
                self.loginnum += 1
        else:
            self.loginnum += 1
            if self.loginnum > 3:
                QMessageBox.critical(self.c_dw, "錯誤!", "帳號/密碼錯誤\n\n已超出登錄次數..... 禁止登錄")
                self.F_login_cancel()
            else:
                QMessageBox.critical(self.c_dw,"錯誤!", "帳號/密碼錯誤，請重新登錄....")
                self.c_le_login.setFocus(Qt.TabFocusReason)
                self.c_le_login.selectAll()
    def F_login_cancel(self):
        self.db.close()
        self.close()
    def F_checkdata(self, objectName):
        temp_return = False
        if objectName == "c_le_login":
            if len(self.c_le_login.text()) == 0:
                temp_return = (True, "帳號不可為空...")
        elif objectName == "c_le_paswd":
            if len(self.c_le_paswd.text()) == 0:
                temp_return = (True, "密碼不可為空...")
        return temp_return

    def F_treewidget(self):
        # 將使用者和Group 讀取符合的 s_userlimited
        grouplimited = db.F_QSqlTableModel("s_groupuserm","pk_s_userm = {}".format(gv.gv_pk_s_userm),"")
        group_where = ""
        #依使用者ID取出群組,再併SQL'S where 條來讀取使用者群組資料
        for row in range(grouplimited.rowCount()):      
            group_where = group_where + " or pk_s_kindd={}".format(grouplimited.index(row,2).data())
        userlimited = db.F_QSqlTableModel("s_userlimited", "pk_s_userm = {}".format(gv.gv_pk_s_userm)+group_where, "")
        self.c_treewidget.clear()
        self.c_treewidget.setFrameShape(QFrame.WinPanel)
        self.c_treewidget.setFrameShadow(QFrame.Raised)
        self.c_treewidget.setHeaderHidden(True)
        #self.c_treewidget.setFont(gv.gv_font)
        self.c_treewidget.setColumnCount(5)
        self.c_treewidget.hideColumn(1)
        self.c_treewidget.hideColumn(2)
        self.c_treewidget.hideColumn(3)
        self.c_treewidget.hideColumn(4)
        self.c_treewidget.itemClicked.connect(self.F_treewidgetclicked)
        self.c_treewidget.itemDoubleClicked.connect(self.F_treewidgetdbclicked)
        menu_node = []
        menu_value = []
        self.c_sqlquery.exec("SELECT * FROM s_modulem ORDER BY module_seq ASC")
        #模組資料寫入 c_treewidget 內
        while self.c_sqlquery.next():
            menu_node.append(self.c_sqlquery.value(2))  # module_no
            temp_twi = QTreeWidgetItem(self.c_treewidget)
            temp_twi.setText(0, self.c_sqlquery.value(4))  # module_nm
            temp_twi.setText(1, self.c_sqlquery.value(5))  # module_memo
            menu_value.append(temp_twi)
        # 子系統的節點和程式選單1.程式名稱|2.程式說明|3.程式參數|4.程式視窗
        self.c_sqlquery.exec("SELECT * FROM s_programd ORDER BY program_no ASC, program_seq ASC, program_id ASC ")
        while self.c_sqlquery.next():
            # program_no 已存在 node 內, 取出存在的 node
            if self.c_sqlquery.value(2) in menu_node:  
                temp_parent = menu_value[menu_node.index(self.c_sqlquery.value(2))]
            # 沒有 node , 在 treewidget 中 找上一層資料即以 program_no 找 program_id(欄位4) 
            else:  
                temp_parent = self.c_treewidget.findItems(self.c_sqlquery.value(2), Qt.MatchFixedString | Qt.MatchRecursive, 4)
                if len(temp_parent) > 0:    # 找到上一層, 將這一層資料加入上一層的 node 中
                    temp_parent = temp_parent[0]
                    menu_node.append(self.c_sqlquery.value(2))
                    menu_value.append(temp_parent)
                else:           #找不到 program_no 無上層資料
                    QMessageBox.critical(self, "錯誤!!", "樹狀資料有問題，找不到上層({}-{})資料".format(self.c_sqlquery.value(0), self.c_sqlquery.value(2)))
                    break
            #程式生效且存在 User 檔案內 或者 程式代碼為空者(program_par 有子階)將資料加入
            if  self.c_sqlquery.value(8) and (userlimited.match(userlimited.index(0,3),Qt.DisplayRole,self.c_sqlquery.value(0), 1, Qt.MatchFixedString) or len(self.c_sqlquery.value(6)) == 0):
                temp_twi = QTreeWidgetItem(temp_parent)        # program_no
                temp_twi.setText(0, self.c_sqlquery.value(4))       # program_nm
                temp_twi.setText(1, self.c_sqlquery.value(9))       # program_memo
                temp_twi.setText(2, self.c_sqlquery.value(6))       # program_par
                temp_twi.setText(3, self.c_sqlquery.value(7))       # program_wintype  0.min  --  9.max
                temp_twi.setText(4, self.c_sqlquery.value(5))       # program_id
        return self.c_treewidget
    def F_treewidgetclicked(self,item):
        self.c_statusbar.showMessage(item.text(0),3000)
        self.c_te_widget.setText(item.text(1))

    def F_treewidgetdbclicked(self, item):
        if len(self.sublist) < 10 and len(item.text(2)) != 0:
            selected = -1
            # 由 menuactionlist.text() 找出 程式是否已開啟
            for number in range(len(self.menuactionlist)):
                if self.menuactionlist[number].text() == item.text(0):
                    selected = number
                    break
            if selected == -1:      # 新開啟的程式
                sub = QMdiSubWindow(self.c_mdiarea)    #,Qt.WindowCloseButtonHint|Qt.WindowMinMaxButtonsHint)
                sub.setWindowTitle(item.text(0))
                sub.setWindowIcon(QIcon(gv.gv_imagepath+"mainwindow/mrp2.png"))
                #sub.setWidget(QWidget())
                #sub.setAttribute(Qt.WA_Moved|Qt.WA_Resized|Qt.WA_DeleteOnClose)
                program_par = item.text(2).split("|")       #program_par 0.程式名程|1.class名稱|2.視窗大小|3.使用權AEDP
                imp = __import__(program_par[0])            #,fromlist=program_par[1])
                runclass = getattr(imp,program_par[1])
                sub.setWidget(runclass(program_par[3]))
                self.c_mdiarea.addSubWindow(sub)
                sub.closeEvent = self.subclose
                sub.show()

                if item.text(3) == '2':
                    sub.setWindowState(Qt.WindowMaximized)
                elif item.text(3) == '1':
                    sub_geometry = list(map(int,program_par[2].split(",")))
                    pointx = (self.c_mdiarea.frameGeometry().width()/2)
                    pointy = (self.c_mdiarea.frameGeometry().height()/2)
                    pointx = pointx - (sub_geometry[0] / 2)
                    if pointx < 0:pointx = 0
                    pointy = pointy - ((sub_geometry[1] +23) / 2)      #+23 增加 subwindwos's 框
                    if pointy < 0:pointy = 0
                    sub.setGeometry(pointx,pointy,sub_geometry[0],sub_geometry[1]+23)
                else:
                    pass
                # 未加入 Widget 不會重複但加入後會產生 QMdiArea::addSubWindow: window is already added,不加第一個subwindow monitor 會lag

                self.sublist.append(sub)
                self.menuactionlist.append(self.menuWindows.addAction(item.text(0)))
            else:
                self.sublist[selected].setFocus()
        elif len(self.sublist) >= 10:
            QMessageBox.warning(self,"警告!!!","運行視窗已超出限制(10)........")

    def subclose(self,closeevent):
        #if len(self.sublist) > 0:   # 預防由 mdi's closeallsubwindow
        # 由mdiwindosw 中的啟動 subwindow 來查找 sublist 中的位置再由其反讀到 menuactionlist's 位置
        subwindowstitle = self.c_mdiarea.activeSubWindow().windowTitle()
        # 由 menuactionlist.text() 找出 程式是否已開啟，使用 while 以免刪除後計數不同造成程式錯誤
        number = 0
        while number < len(self.menuactionlist):
            if self.menuactionlist[number].text() == subwindowstitle:
                self.c_mdiarea.setActiveSubWindow(self.sublist[number])
                #self.sublist[number].setFocus()     #設focus 以免誤關 其它 activewindow
                break
            number += 1
        # 刪除 subwindow-選單-選單list-subwindow's List
        self.c_mdiarea.removeSubWindow(self.sublist[number])
        self.menubar.removeAction(self.menuactionlist[number])
        self.menuactionlist[number].deleteLater()
        self.menuactionlist.pop(number)
        self.sublist.pop(number)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = C_mainmenu()
    sys.exit(app.exec_())
