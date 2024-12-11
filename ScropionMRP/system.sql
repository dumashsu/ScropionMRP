

/* Create Tables */

-- S_Flowchart(流程基本資料檔)
CREATE TABLE S_Flowchart
(
	-- pk_s_flowchart(主鍵值_流程基本資料主檔) : pk_s_flowchart(主鍵值_流程基本資料主檔)
	pk_s_flowchart serial NOT NULL UNIQUE,
	-- flowchart_no(流程編號) : flowchart_no(流程編號)
	flowchart_no varchar(10) UNIQUE,
	-- flowchart_nm(流程名稱) : flowchart_nm(流程名稱)
	flowchart_nm varchar(50) NOT NULL,
	-- flowchart_nm_en(流程英文名稱) : flowchart_nm_en(流程英文名稱)
	flowchart_nm_en varchar(50),
	-- flowchart_valid(生效註記) : flowchart_valid(生效註記)
	flowchart_valid boolean,
	-- flowchart_memo(備註說明) : flowchart_memo(備註說明)
	flowchart_memo varchar(1000),
	-- factory_no(廠別代號) : factory_no(廠別代號) from kindd
	factory_no int,
	PRIMARY KEY (pk_s_flowchart)
) WITHOUT OIDS;


-- S_Flowchartd(流程明細檔)
CREATE TABLE S_Flowchartd
(
	-- pk_s_flowchartd(主鍵值_流程明細檔) : pk_s_flowchartd(主鍵值_流程明細檔)
	pk_s_flowchartd serial NOT NULL UNIQUE,
	-- pk_s_flowchart(主鍵值_流程基本資料主檔) : pk_s_flowchart(主鍵值_流程基本資料主檔)
	pk_s_flowchart int NOT NULL,
	-- father_seq(父階流水號) : father_seq(父階流水號)
	father_seq numeric(2) NOT NULL,
	-- pk_userId_father(父階使用者ID) : pk_userId_father(父階使用者ID)
	pk_userId_father numeric NOT NULL,
	-- son_seq(子階流水號) : son_seq(子階流水號)
	son_seq numeric(2) NOT NULL,
	-- pk_s_userid_son(子階使用者ID) : pk_s_userid_son(子階使用者ID)
	pk_s_userid_son numeric NOT NULL,
	-- factory_no(上階廠別代號) : factory_no(上階廠別代號)
	factory_no int,
	PRIMARY KEY (pk_s_flowchartd)
) WITHOUT OIDS;


-- S_GROUPUSERM(使用者群組)
CREATE TABLE S_GROUPUSERM
(
	-- pk_s_groupuserm(主鍵值_使用者群組) : pk_s_groupuserm(主鍵值_使用者群組)
	pk_s_groupuserm serial NOT NULL UNIQUE,
	-- pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)
	pk_s_userm int NOT NULL UNIQUE,
	-- pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)
	pk_s_kindd int NOT NULL UNIQUE,
	PRIMARY KEY (pk_s_groupuserm)
) WITHOUT OIDS;


-- S_KINDD(類別明細檔)
CREATE TABLE S_KINDD
(
	-- pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)
	pk_s_kindd serial NOT NULL UNIQUE,
	-- pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)
	pk_s_kindm int NOT NULL,
	-- kindd_nm(類別明細名稱) : kindd_nm(類別明細名稱)
	-- EG:SKYPE/WECHAT.....
	kindd_nm varchar(30),
	-- kindd_f_nm(類別明細全名) : kindd_f_nm(類別明細全名)
	kindd_f_nm varchar(100),
	-- kindd_col1(各類別自訂使用) : kindd_col1(各類別自訂使用)
	kindd_col1 varchar(20),
	-- kindd_col2(各註記自訂使用) : kindd_col2(各註記自訂使用)
	kindd_col2 varchar(30),
	-- kindd_col3(各註記自訂使用) : kindd_col3(各註記自訂使用)
	kindd_col3 varchar(50),
	PRIMARY KEY (pk_s_kindd),
	UNIQUE (pk_s_kindd)
) WITHOUT OIDS;


-- S_KINDM(類別主檔)
CREATE TABLE S_KINDM
(
	-- pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)
	pk_s_kindm serial NOT NULL UNIQUE,
	-- kindm_no(類別種類) : 00.廠別
	-- 01.部門
	-- 02.使用者明細檔(Mail/Line...)
	-- 03.帳號群組明細
	kindm_no varchar(2) NOT NULL UNIQUE,
	-- kindm_nm(類別種類名稱) : kindm_nm(類別種類名稱)
	kindm_nm varchar(30),
	PRIMARY KEY (pk_s_kindm)
) WITHOUT OIDS;


-- S_Language(語言名稱檔)
CREATE TABLE S_Languagenm
(
	-- pk_s_language(主鍵值_語言名稱檔) : pk_s_language(主鍵值_語言名稱檔)
	pk_s_language serial NOT NULL UNIQUE,
	-- language_nm(語言名稱) : language_nm(語言名稱)
	language_nm varchar(10) NOT NULL UNIQUE,
	PRIMARY KEY (pk_s_language)
) WITHOUT OIDS;


-- S_Modulem(模組資料主檔)
CREATE TABLE S_Modulem
(
	-- pk_s_modulem(主鍵值_模組資料主檔) : pk_s_modulem(主鍵值_模組資料主檔)
	pk_s_modulem serial NOT NULL UNIQUE,
	-- module_Seq(模組排序號) : module_Seq(模組排序號)
	module_Seq numeric(4) NOT NULL UNIQUE,
	-- module_No(模組代號) : module_No(模組代號)
	module_No varchar(4) NOT NULL UNIQUE,
	-- module_s_nm(模組簡稱) : module_s_nm(模組簡稱)
	module_s_nm varchar(30) NOT NULL,
	-- module_Nm(模組名稱) : module_Nm(模組名稱)
	module_Nm varchar(50) NOT NULL,
	-- module_memo(模組說明) : module_memo(模組說明)
	module_memo text,
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial NOT NULL,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23),
	PRIMARY KEY (pk_s_modulem)
) WITHOUT OIDS;


-- S_MultiLanguage(多國語言檔)
CREATE TABLE S_MultiLanguage
(
	-- pk_s_multilanguage(主鍵值_多國語言檔) : pk_s_multilanguage(主鍵值_多國語言檔)
	pk_s_multilanguage serial NOT NULL UNIQUE,
	-- pk_s_language(主鍵值_語言名稱檔) : pk_s_language(主鍵值_語言名稱檔)
	pk_s_language int NOT NULL,
	-- language_source(原始語文) : language_source(原始語文)
	language_source varchar(200) NOT NULL,
	-- language_target(目的語文) : language_target(目的語文)
	language_target varchar(200),
	PRIMARY KEY (pk_s_multilanguage)
) WITHOUT OIDS;


-- S_Programd(模組選單明細檔)
CREATE TABLE S_Programd
(
	-- pk_s_programd(主鍵值_模組選單明細檔) : pk_s_programd(主鍵值_模組選單明細檔)
	pk_s_programd serial NOT NULL UNIQUE,
	-- pk_s_modulem(主鍵值_模組資料主檔) : pk_s_modulem(主鍵值_模組資料主檔)
	pk_s_modulem int NOT NULL,
	-- program_no(選單代號) : program_no(選單代號)
	-- 前 4 碼為模組代號
	program_no varchar(8),
	-- program_seq(選單流水號) : program_seq(選單流水號)
	program_seq numeric(4),
	-- program_nm(選單名稱) : program_nm(選單名稱)
	program_nm varchar(50),
	-- program_id(選單程式名稱) : program_id(選單程式名稱)
	program_id varchar(8),
	-- program_par(程式參數) : program_par(程式參數)
	program_par varchar(50),
	-- program_wintype(視窗型態) : 0.最小
	-- 
	-- 9.最大
	program_wintype varchar(1),
	-- program_effective(選單生效註記) : program_effective(選單生效註記)
	program_effective bigint,
	-- program_memo(選單說明) : program_memo(選單說明)
	program_memo text,
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23),
	PRIMARY KEY (pk_s_programd)
) WITHOUT OIDS;


-- S_USERD(使用者明細檔)
CREATE TABLE S_USERD
(
	-- pk_s_userd(主鍵值_使用者明細檔) : pk_s_userd(主鍵值_使用者明細檔)
	pk_s_userd serial NOT NULL,
	-- pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)
	pk_s_userm int NOT NULL,
	-- pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)
	pk_s_kindd int NOT NULL,
	-- user_kindd_nm(類別明細內容) : user_kindd_nm(類別明細內容)
	user_kindd_nm varchar(50) NOT NULL,
	PRIMARY KEY (pk_s_userd)
) WITHOUT OIDS;


-- S_USERLIMITED(使用者權限檔)
CREATE TABLE S_USERLIMITED
(
	-- pk_s_userlimited(主鍵值_使用者權限) : pk_s_userlimited(主鍵值)
	pk_s_userlimited serial NOT NULL UNIQUE,
	-- pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)
	pk_s_userm int,
	-- pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)
	pk_s_kindd int,
	-- pk_s_programd(主鍵值_模組選單明細檔) : pk_s_programd(主鍵值_模組選單明細檔)
	pk_s_programd int NOT NULL,
	-- limited_append(新增) : limited_append(新增)
	limited_append varchar(1),
	-- limited_edit(修改) : limited_edit(修改)
	limited_edit varchar(1),
	-- limited_delete(刪除) : limited_delete(刪除)
	limited_delete varchar(1),
	-- limited_find(查詢) : limited_find(查詢)
	limited_find varchar(1),
	-- limited_print(列印) : limited_print(列印)
	limited_print varchar(1),
	PRIMARY KEY (pk_s_userlimited)
) WITHOUT OIDS;


-- S_USERM(使用者主檔)
CREATE TABLE S_USERM
(
	-- pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)
	pk_s_userm serial NOT NULL UNIQUE,
	-- FACTORY_NO(廠別代號) : Factory_no(廠別代號) 由 KINDD 而來
	FACTORY_NO int NOT NULL,
	-- user_id(使用者ID) : user_id(使用者ID)
	user_id varchar(20) NOT NULL UNIQUE,
	-- user_nm(使用者名稱) : user_nm(使用者名稱)
	user_nm varchar(30) NOT NULL,
	-- user_pswd(使用者密碼) : user_pswd(使用者密碼)
	user_pswd varchar(15) NOT NULL,
	-- user_suspended(停權) : user_suspended(停權)
	-- 0:Yes
	-- 1:No
	user_suspended bigint DEFAULT 0,
	-- user_factory_mk(跨廠註記) : user_factory_mk(跨廠註記)
	user_factory_mk boolean,
	-- user_marked(使用者註記) : user_marked(使用者註記)
	-- 1.一般使用者
	-- 9.超級使用者
	-- 
	-- 
	user_marked char(1) DEFAULT '1',
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23),
	-- user_photo(相片) : user_photo(相片)
	user_photo bytea,
	PRIMARY KEY (pk_s_userm)
) WITHOUT OIDS;



/* Create Foreign Keys */

ALTER TABLE S_Flowchartd
	ADD CONSTRAINT FK_Flowchart_d FOREIGN KEY (pk_s_flowchart)
	REFERENCES S_Flowchart (pk_s_flowchart)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE customm
	ADD FOREIGN KEY (customm_type)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE customs
	ADD FOREIGN KEY (pk_s_kindd)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE partm
	ADD FOREIGN KEY (pk_s_kindd)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE SIZES
	ADD FOREIGN KEY (pk_s_kindd)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_GROUPUSERM
	ADD FOREIGN KEY (pk_s_kindd)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_USERD
	ADD FOREIGN KEY (pk_s_kindd)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_USERLIMITED
	ADD FOREIGN KEY (pk_s_kindd)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_USERM
	ADD FOREIGN KEY (FACTORY_NO)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendorm
	ADD FOREIGN KEY (vendorm_taxsource)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendorm
	ADD FOREIGN KEY (vendorm_kind)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendorm
	ADD FOREIGN KEY (vendorm_payment)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendorm
	ADD FOREIGN KEY (vendorm_type)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendorm
	ADD FOREIGN KEY (vendorm_coin)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendorm
	ADD FOREIGN KEY (vendorm_tradeticket)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendorm
	ADD FOREIGN KEY (vendorm_purchasepolicy)
	REFERENCES S_KINDD (pk_s_kindd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE matm
	ADD FOREIGN KEY (pk_s_kindm)
	REFERENCES S_KINDM (pk_s_kindm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_KINDD
	ADD CONSTRAINT FK_PK_S_KINDM_D FOREIGN KEY (pk_s_kindm)
	REFERENCES S_KINDM (pk_s_kindm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendors
	ADD FOREIGN KEY (pk_s_kindm)
	REFERENCES S_KINDM (pk_s_kindm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_MultiLanguage
	ADD FOREIGN KEY (pk_s_language)
	REFERENCES S_Languagenm (pk_s_language)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_Programd
	ADD FOREIGN KEY (pk_s_modulem)
	REFERENCES S_Modulem (pk_s_modulem)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_USERLIMITED
	ADD FOREIGN KEY (pk_s_programd)
	REFERENCES S_Programd (pk_s_programd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_GROUPUSERM
	ADD FOREIGN KEY (pk_s_userm)
	REFERENCES S_USERM (pk_s_userm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_USERD
	ADD FOREIGN KEY (pk_s_userm)
	REFERENCES S_USERM (pk_s_userm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE S_USERLIMITED
	ADD FOREIGN KEY (pk_s_userm)
	REFERENCES S_USERM (pk_s_userm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



/* Create Indexes */

CREATE INDEX ID_Flowchart_1 ON S_Flowchart (flowchart_no);
CREATE INDEX ID_FLOWCHARTD ON S_Flowchartd (pk_s_flowchartd);
CREATE INDEX ID_KINDD ON S_KINDD (pk_s_kindd);
CREATE UNIQUE INDEX ID_S_MODULEM ON S_Modulem (module_Seq);
CREATE UNIQUE INDEX ID_Multilanguage ON S_MultiLanguage (pk_s_multilanguage, language_source);



/* Comments */

COMMENT ON TABLE S_Flowchart IS 'S_Flowchart(流程基本資料檔)';
COMMENT ON COLUMN S_Flowchart.pk_s_flowchart IS 'pk_s_flowchart(主鍵值_流程基本資料主檔) : pk_s_flowchart(主鍵值_流程基本資料主檔)';
COMMENT ON COLUMN S_Flowchart.flowchart_no IS 'flowchart_no(流程編號) : flowchart_no(流程編號)';
COMMENT ON COLUMN S_Flowchart.flowchart_nm IS 'flowchart_nm(流程名稱) : flowchart_nm(流程名稱)';
COMMENT ON COLUMN S_Flowchart.flowchart_nm_en IS 'flowchart_nm_en(流程英文名稱) : flowchart_nm_en(流程英文名稱)';
COMMENT ON COLUMN S_Flowchart.flowchart_valid IS 'flowchart_valid(生效註記) : flowchart_valid(生效註記)';
COMMENT ON COLUMN S_Flowchart.flowchart_memo IS 'flowchart_memo(備註說明) : flowchart_memo(備註說明)';
COMMENT ON COLUMN S_Flowchart.factory_no IS 'factory_no(廠別代號) : factory_no(廠別代號) from kindd';
COMMENT ON TABLE S_Flowchartd IS 'S_Flowchartd(流程明細檔)';
COMMENT ON COLUMN S_Flowchartd.pk_s_flowchartd IS 'pk_s_flowchartd(主鍵值_流程明細檔) : pk_s_flowchartd(主鍵值_流程明細檔)';
COMMENT ON COLUMN S_Flowchartd.pk_s_flowchart IS 'pk_s_flowchart(主鍵值_流程基本資料主檔) : pk_s_flowchart(主鍵值_流程基本資料主檔)';
COMMENT ON COLUMN S_Flowchartd.father_seq IS 'father_seq(父階流水號) : father_seq(父階流水號)';
COMMENT ON COLUMN S_Flowchartd.pk_userId_father IS 'pk_userId_father(父階使用者ID) : pk_userId_father(父階使用者ID)';
COMMENT ON COLUMN S_Flowchartd.son_seq IS 'son_seq(子階流水號) : son_seq(子階流水號)';
COMMENT ON COLUMN S_Flowchartd.pk_s_userid_son IS 'pk_s_userid_son(子階使用者ID) : pk_s_userid_son(子階使用者ID)';
COMMENT ON COLUMN S_Flowchartd.factory_no IS 'factory_no(上階廠別代號) : factory_no(上階廠別代號)';
COMMENT ON TABLE S_GROUPUSERM IS 'S_GROUPUSERM(使用者群組)';
COMMENT ON COLUMN S_GROUPUSERM.pk_s_groupuserm IS 'pk_s_groupuserm(主鍵值_使用者群組) : pk_s_groupuserm(主鍵值_使用者群組)';
COMMENT ON COLUMN S_GROUPUSERM.pk_s_userm IS 'pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)';
COMMENT ON COLUMN S_GROUPUSERM.pk_s_kindd IS 'pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)';
COMMENT ON TABLE S_KINDD IS 'S_KINDD(類別明細檔)';
COMMENT ON COLUMN S_KINDD.pk_s_kindd IS 'pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)';
COMMENT ON COLUMN S_KINDD.pk_s_kindm IS 'pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)';
COMMENT ON COLUMN S_KINDD.kindd_nm IS 'kindd_nm(類別明細名稱) : kindd_nm(類別明細名稱)
EG:SKYPE/WECHAT.....';
COMMENT ON COLUMN S_KINDD.kindd_f_nm IS 'kindd_f_nm(類別明細全名) : kindd_f_nm(類別明細全名)';
COMMENT ON COLUMN S_KINDD.kindd_col1 IS 'kindd_col1(各類別自訂使用) : kindd_col1(各類別自訂使用)';
COMMENT ON COLUMN S_KINDD.kindd_col2 IS 'kindd_col2(各註記自訂使用) : kindd_col2(各註記自訂使用)';
COMMENT ON COLUMN S_KINDD.kindd_col3 IS 'kindd_col3(各註記自訂使用) : kindd_col3(各註記自訂使用)';
COMMENT ON TABLE S_KINDM IS 'S_KINDM(類別主檔)';
COMMENT ON COLUMN S_KINDM.pk_s_kindm IS 'pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)';
COMMENT ON COLUMN S_KINDM.kindm_no IS 'kindm_no(類別種類) : 00.廠別
01.部門
02.使用者明細檔(Mail/Line...)
03.帳號群組明細';
COMMENT ON COLUMN S_KINDM.kindm_nm IS 'kindm_nm(類別種類名稱) : kindm_nm(類別種類名稱)';
COMMENT ON TABLE S_Languagenm IS 'S_Language(語言名稱檔)';
COMMENT ON COLUMN S_Languagenm.pk_s_language IS 'pk_s_language(主鍵值_語言名稱檔) : pk_s_language(主鍵值_語言名稱檔)';
COMMENT ON COLUMN S_Languagenm.language_nm IS 'language_nm(語言名稱) : language_nm(語言名稱)';
COMMENT ON TABLE S_Modulem IS 'S_Modulem(模組資料主檔)';
COMMENT ON COLUMN S_Modulem.pk_s_modulem IS 'pk_s_modulem(主鍵值_模組資料主檔) : pk_s_modulem(主鍵值_模組資料主檔)';
COMMENT ON COLUMN S_Modulem.module_Seq IS 'module_Seq(模組排序號) : module_Seq(模組排序號)';
COMMENT ON COLUMN S_Modulem.module_No IS 'module_No(模組代號) : module_No(模組代號)';
COMMENT ON COLUMN S_Modulem.module_s_nm IS 'module_s_nm(模組簡稱) : module_s_nm(模組簡稱)';
COMMENT ON COLUMN S_Modulem.module_Nm IS 'module_Nm(模組名稱) : module_Nm(模組名稱)';
COMMENT ON COLUMN S_Modulem.module_memo IS 'module_memo(模組說明) : module_memo(模組說明)';
COMMENT ON COLUMN S_Modulem.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN S_Modulem.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE S_MultiLanguage IS 'S_MultiLanguage(多國語言檔)';
COMMENT ON COLUMN S_MultiLanguage.pk_s_multilanguage IS 'pk_s_multilanguage(主鍵值_多國語言檔) : pk_s_multilanguage(主鍵值_多國語言檔)';
COMMENT ON COLUMN S_MultiLanguage.pk_s_language IS 'pk_s_language(主鍵值_語言名稱檔) : pk_s_language(主鍵值_語言名稱檔)';
COMMENT ON COLUMN S_MultiLanguage.language_source IS 'language_source(原始語文) : language_source(原始語文)';
COMMENT ON COLUMN S_MultiLanguage.language_target IS 'language_target(目的語文) : language_target(目的語文)';
COMMENT ON TABLE S_Programd IS 'S_Programd(模組選單明細檔)';
COMMENT ON COLUMN S_Programd.pk_s_programd IS 'pk_s_programd(主鍵值_模組選單明細檔) : pk_s_programd(主鍵值_模組選單明細檔)';
COMMENT ON COLUMN S_Programd.pk_s_modulem IS 'pk_s_modulem(主鍵值_模組資料主檔) : pk_s_modulem(主鍵值_模組資料主檔)';
COMMENT ON COLUMN S_Programd.program_no IS 'program_no(選單代號) : program_no(選單代號)
前 4 碼為模組代號';
COMMENT ON COLUMN S_Programd.program_seq IS 'program_seq(選單流水號) : program_seq(選單流水號)';
COMMENT ON COLUMN S_Programd.program_nm IS 'program_nm(選單名稱) : program_nm(選單名稱)';
COMMENT ON COLUMN S_Programd.program_id IS 'program_id(選單程式名稱) : program_id(選單程式名稱)';
COMMENT ON COLUMN S_Programd.program_par IS 'program_par(程式參數) : program_par(程式參數)';
COMMENT ON COLUMN S_Programd.program_wintype IS 'program_wintype(視窗型態) : 0.最小

9.最大';
COMMENT ON COLUMN S_Programd.program_effective IS 'program_effective(選單生效註記) : program_effective(選單生效註記)';
COMMENT ON COLUMN S_Programd.program_memo IS 'program_memo(選單說明) : program_memo(選單說明)';
COMMENT ON COLUMN S_Programd.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN S_Programd.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE S_USERD IS 'S_USERD(使用者明細檔)';
COMMENT ON COLUMN S_USERD.pk_s_userd IS 'pk_s_userd(主鍵值_使用者明細檔) : pk_s_userd(主鍵值_使用者明細檔)';
COMMENT ON COLUMN S_USERD.pk_s_userm IS 'pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)';
COMMENT ON COLUMN S_USERD.pk_s_kindd IS 'pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)';
COMMENT ON COLUMN S_USERD.user_kindd_nm IS 'user_kindd_nm(類別明細內容) : user_kindd_nm(類別明細內容)';
COMMENT ON TABLE S_USERLIMITED IS 'S_USERLIMITED(使用者權限檔)';
COMMENT ON COLUMN S_USERLIMITED.pk_s_userlimited IS 'pk_s_userlimited(主鍵值_使用者權限) : pk_s_userlimited(主鍵值)';
COMMENT ON COLUMN S_USERLIMITED.pk_s_userm IS 'pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)';
COMMENT ON COLUMN S_USERLIMITED.pk_s_kindd IS 'pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)';
COMMENT ON COLUMN S_USERLIMITED.pk_s_programd IS 'pk_s_programd(主鍵值_模組選單明細檔) : pk_s_programd(主鍵值_模組選單明細檔)';
COMMENT ON COLUMN S_USERLIMITED.limited_append IS 'limited_append(新增) : limited_append(新增)';
COMMENT ON COLUMN S_USERLIMITED.limited_edit IS 'limited_edit(修改) : limited_edit(修改)';
COMMENT ON COLUMN S_USERLIMITED.limited_delete IS 'limited_delete(刪除) : limited_delete(刪除)';
COMMENT ON COLUMN S_USERLIMITED.limited_find IS 'limited_find(查詢) : limited_find(查詢)';
COMMENT ON COLUMN S_USERLIMITED.limited_print IS 'limited_print(列印) : limited_print(列印)';
COMMENT ON TABLE S_USERM IS 'S_USERM(使用者主檔)';
COMMENT ON COLUMN S_USERM.pk_s_userm IS 'pk_s_userm(主鍵值_使用者主檔) : pk_s_userm(主鍵值_使用者主檔)';
COMMENT ON COLUMN S_USERM.FACTORY_NO IS 'FACTORY_NO(廠別代號) : Factory_no(廠別代號) 由 KINDD 而來';
COMMENT ON COLUMN S_USERM.user_id IS 'user_id(使用者ID) : user_id(使用者ID)';
COMMENT ON COLUMN S_USERM.user_nm IS 'user_nm(使用者名稱) : user_nm(使用者名稱)';
COMMENT ON COLUMN S_USERM.user_pswd IS 'user_pswd(使用者密碼) : user_pswd(使用者密碼)';
COMMENT ON COLUMN S_USERM.user_suspended IS 'user_suspended(停權) : user_suspended(停權)
0:Yes
1:No';
COMMENT ON COLUMN S_USERM.user_factory_mk IS 'user_factory_mk(跨廠註記) : user_factory_mk(跨廠註記)';
COMMENT ON COLUMN S_USERM.user_marked IS 'user_marked(使用者註記) : user_marked(使用者註記)
1.一般使用者
9.超級使用者

';
COMMENT ON COLUMN S_USERM.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN S_USERM.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON COLUMN S_USERM.user_photo IS 'user_photo(相片) : user_photo(相片)';



