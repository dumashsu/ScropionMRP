# -*- coding: utf-8 -*-
'''
F_s_program()
寫入 s_program 使用, pk_s_module 必需和 s_module's  的PK值一樣(也就後面寫入 2 )
第一層 profram_no 也必需和 s_module's  module_no 一樣(也就是開始的 1000/2000)

F_s_kindm()
寫入 s_kindm 的必需資料

'''
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import QDateTime
import db,gv
db.F_DBConnect()
query = QSqlQuery()

'''
 建立 s_kindm/s_kindd 主明細資料
 建立主檔 s_kindm, 
 若是'00'再判別明細是否有資料,無建立以便 s_userm 使用
 若是'03'再判別明細是否有資料,無建立
'''
def F_s_kindm():
    l_kindm_no = (['00','廠別代號'],['01','部門'],['02','明細資料(EMail/Tel...)'],['03',"群組名稱"])
    for temp_seq in range(len(l_kindm_no)):
        query.exec_("select * from s_kindm where kindm_no = '{}'".format(l_kindm_no[temp_seq][0]))
        if query.numRowsAffected() == 0 :       #無資料就新增
            query.exec_("INSERT INTO s_kindm (kindm_no, kindm_nm) VALUES ('{}','{}')".format(l_kindm_no[temp_seq][0],l_kindm_no[temp_seq][1]))
            
        if l_kindm_no[temp_seq][0] in '0003' :
            if query.numRowsAffected() == 0:
                s_kindm_pk = query.lastInsertId()
            else:
                query.next()
                s_kindm_pk = query.value(0)
            query.exec_("select * from s_kindd where pk_s_kindm = {} ".format(s_kindm_pk))
            # 依類別主檔的代號來建立明細資料
            if query.numRowsAffected() == 0 :  
                if  l_kindm_no[temp_seq][0] == '00' :
                    query.exec_("INSERT INTO s_kindd (pk_s_kindm, kindd_nm,kindd_f_nm) VALUES ('{}','system','Factory(自訂廠別供系統管理者使用)')".format(s_kindm_pk))
                elif   l_kindm_no[temp_seq][0] == '03' :      
                    query.exec_("INSERT INTO s_kindd (pk_s_kindm, kindd_nm,kindd_f_nm) VALUES ('{}','system','系統管理者')".format(s_kindm_pk))
                    
'''
建立系統管理者帳號, 廠別由 s_kindm's '00' 資料而來"
不存在建立, 存在 變更 gv_的變數值  
 再設置使用者為系統管理者的群組'03'-system, 方便在後面建立系統選單時可同步設置權限
'''
def F_s_userm():
    query.exec_("select * from s_userm where user_id = 'dumas'")
    if query.numRowsAffected() == 0 :       #無資料就新增
        query.exec_("select * from s_kindd where pk_s_kindm in (select pk_s_kindm  from s_kindm where kindm_no = '00') ")
        query.next()
        factory_no = query.value(0)
        query.exec_("INSERT INTO s_userm (factory_no,user_id,user_nm,user_pswd,user_suspended,user_marked,modify_dt) VALUES ('{}','dumas','Dumas Hsu','5711438',1,'9')".\
                    format(factory_no,QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss")))
        gv.gv_pk_s_userm = query.lastInsertId()
        gv.gv_user = 'Dumas Hsu'
        gv.gv_id = 'dumas'
    else:
        query.next()
        gv.gv_pk_s_userm = query.value(0)
        gv.gv_user = query.value(3)
        gv.gv_id = query.value(2)
        
    #找類別明細檔中的system 群組, 取出 PK
    query.exec_("select * from s_kindd where kindd_nm = 'system'")
    query.next()
    pk_s_kindd = query.value(0)
    query.exec_("SELECT * FROM s_groupuserm WHERE pk_s_userm ={}".format(gv.gv_pk_s_userm))
    if query.numRowsAffected() == 0:
        query.exec_("INSERT INTO s_groupuserm (pk_s_userm,pk_s_kindd) VALUES ({},{})".format(gv.gv_pk_s_userm,pk_s_kindd))        
'''
新增系統模組,不存在寫入, 存在記錄 pk
'''        
def F_s_modulem():
    query.exec_("SELECT * from s_modulem WHERE module_no = '9999'")
    if query.numRowsAffected() == 0 :       #無資料就新增
        query.exec_("INSERT INTO s_modulem (module_seq,module_no,module_s_nm,module_nm,modify_user,modify_dt) VALUES (9999,'9999','系統維護','系統維護',{},'{}')" \
                    .format(gv.gv_pk_s_userm,QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss")))
    else:
        query.next()
        
'''
先建立系統管理者群組
新增系統選單, 先找 系統模組的PK, 再一一寫入 s_program_no 再同時再建立系統管理的群組及群組權限
'''         
def F_s_program():
    listdata = []
    #_program_id/program_no
    #第一層的 program_no 必需相同於 module_no 
    listdata.append(["9999",10,"類別名稱主檔維護","99991000","p_kindm|C_WindowWidget|550,250|AEDP","1"])
    listdata.append(["9999",20,"類別資料維護","99992000","p_kindd|C_widget|750,250|AEDFp","1"])
    listdata.append(["9999",30,"使用者基本資料維護作業","99993000","p_userm|C_widget|800,420|AEDFP","1"])
    listdata.append(["9999",40,"模組資料維護","99994000","p_modulem|C_widget|840,380|AED","1"])
    listdata.append(["9999",50,"選單資料維護","99995000","p_program|C_widget|800,380|AEDP","1"])
    listdata.append(["9999",60,"群組使用者維護作業","99996000","p_groupuser|C_widget|690,500|AEDFP","1"])
    listdata.append(["9999",70,"使用者權限作業","99997000","p_userlimited|C_widget|830,380|AEDFP","1"])
    query.exec_("SELECT * from s_modulem WHERE module_no = '9999'")
    query.next()
    t_pk_s_modulem = query.value(0)    
    query.exec_("select * from s_kindd where kindd_nm = 'system'")
    query.next()
    pk_s_kindd = query.value(0)
    for number in range(len(listdata)):
        sql = "INSERT INTO s_programd (pk_s_modulem,program_no,program_seq,program_nm,program_id,program_par,program_wintype,program_effective,modify_user,modify_dt) VALUES \
                    ({},?,?,?,?,?,?,1,{},'{}')".format(t_pk_s_modulem,gv.gv_pk_s_userm,QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
        if query.prepare(sql):
            query.bindValue(0, listdata[number][0])
            query.bindValue(1, listdata[number][1])
            query.bindValue(2, listdata[number][2])
            query.bindValue(3, listdata[number][3])
            query.bindValue(4, listdata[number][4])
            query.bindValue(5, listdata[number][5])            
            query.exec_()
            pk_s_programd = query.lastInsertId()
            #類別明細檔已建立system 群組,再建立該選單的群組權限
            if pk_s_kindd != 0:
                query.exec_("SELECT * FROM s_userlimited WHERE pk_s_kindd ={} and pk_s_programd = {}".format(pk_s_kindd,pk_s_programd))
                if query.numRowsAffected() == 0:
                    query.exec_("INSERT INTO s_userlimited (pk_s_kindd,pk_s_programd,limited_append,limited_edit,limited_delete,limited_find,limited_print) VALUES({},{},1,1,1,1,1".\
                                    format(pk_s_kindd,pk_s_programd))
'''
建立 SMRP 的程式菜單
先建立系統模組並取出系統編號, 再由系統編號來一一建立子菜單
'''
def F_s_program_4_SMRP():
    # 雙迴圈, 第一層寫系統名稱(s_modulem), 第二層寫該系統的選單(s_program)
    l_module = []
    l_module.append([1000,'1000','BOM系統','BOM系統'])
    l_module.append([2000,'2000','業務系 統','業務系統'])
    l_program = []      # 第一欄, 記錄 和 l_module 之關係
    l_program.append([1000,"1000",1,"BOM系統基本作業","10001000","","0",1])
    l_program.append([1000,"1000",6,"BOM作業","10002000","","0",1])
    l_program.append([1000,"1000",7,"列印作業","10003000","","",1])
    l_program.append([1000,"10001000",10,"品牌資料建立","10001100","p_brandm|C_widget|780,320|AED","1",1])
    l_program.append([1000,"10001000",15,"品牌客戶資料維護","10001110","p_customm|C_widget|800,610|AEDP","1",1])
    l_program.append([1000,"10001000",20,"供應商資料維護","10001200","p_vendorm|C_widget|922,480|AEDP","1",1])
    l_program.append([1000,"10001000",30,"採購分類資料建立","10001300","","0",1])
    l_program.append([1000,"10001000",40,"部位資料建立","10001400","","0",1])
    l_program.append([1000,"10001000",50,"品名資料建立","10001500","","0",1])
    l_program.append([1000,"10001000",60,"SIZE種類建立","10001600","","0",1])
    l_program.append([1000,"10001000",70,"SIZE明細資料建立","10001700","","0",1])
    l_program.append([1000,"10001000",80,"海關基本資料","10001500","","0",1])
    l_program.append([1000,"10001000",90,"材料基本資料","10001600","","0",1])
    l_program.append([1000,"10001500",1,"海關索引資料建立","10001510","","",1])
    l_program.append([1000,"10001500",2,"海關商品資料建立","10001520","","",1])
    l_program.append([1000,"10001600",1,"單位資料建立","10001610","","",1])
    l_program.append([1000,"10001600",2,"規格資料建立","10001620","","",1])
    l_program.append([1000,"10001600",3,"顏色資料維護","10001630","p_colorm|C_widget|800,400|AEDP","1",1])
    l_program.append([1000,"10001600",4,"材料基本資料建立","10001640","","",1])
    l_program.append([1000,"10001600",5,"加工代號資料建立","10001650","","",1])
    l_program.append([1000,"10001600",6,"加工材料建立","10001660","","",1])
    l_program.append([1000,"10002000",1,"型體基本資料建立","10002100","","",1])
    l_program.append([1000,"10002000",2,"型體BOM資料建立","10002200","","",1])
    l_program.append([1000,"10002000",3,"型體斬刀用量維護","10002300","","",1])
    l_program.append([1000,"10002000",4,"型體免用量維護","10002400","","",1])
    l_program.append([1000,"10002000",5,"BOM轉入作業","10002500","","",1])
    l_program.append([1000,"10002000",6,"型體分段SIZE指定作業","10002600","","",1])
    l_program.append([2000,"2000",1,"業務系統基本作業","20001000","","0",1])        
    for module_row in range(len(l_module)):
        query.exec_("SELECT * from s_modulem WHERE module_no = '{}'".format(l_module[module_row][0]))
        if query.numRowsAffected() == 0 :       #無資料就新增
            query.exec_("INSERT INTO s_modulem (module_seq,module_no,module_s_nm,module_nm,modify_user,modify_dt) VALUES ({},'{}','{}','{}',{},'{}')" \
                        .format(l_module[module_row][0],l_module[module_row][1],l_module[module_row][2],l_module[module_row][3], gv.gv_pk_s_userm,QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss")))            
            t_pk_s_modulem = query.lastInsertId()
        else:
            query.next()
            t_pk_s_modulem = query.value(0)       
        for program_row in range(len(l_program)):
            if l_program[program_row][0] == l_module[module_row][0]:
                sql = "INSERT INTO s_programd (pk_s_modulem,program_no,program_seq,program_nm,program_id,program_par,program_wintype,program_effective,modify_user,modify_dt) VALUES \
                        ({},?,?,?,?,?,?,1,{},'{}')".format(t_pk_s_modulem,gv.gv_pk_s_userm,QDateTime().currentDateTime().toString("yyyy/MM/dd HH:mm:ss"))
                if query.prepare(sql):
                    query.bindValue(0, l_program[program_row][1])
                    query.bindValue(1, l_program[program_row][2])
                    query.bindValue(2, l_program[program_row][3])
                    query.bindValue(3, l_program[program_row][4])
                    query.bindValue(4, l_program[program_row][5])
                    query.bindValue(5, l_program[program_row][6])            
                    query.exec_()    
                
# 執行程式
F_s_kindm()
F_s_userm()
F_s_modulem()
F_s_program()
#F_s_program_4_SMRP()