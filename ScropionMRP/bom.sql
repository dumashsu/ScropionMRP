

/* Create Tables */

-- brandm(品牌資料)
CREATE TABLE brandm
(
	-- pk_brandm(主鍵值_品牌主檔) : pk_brandm(主鍵值_品牌主檔)
	pk_brandm serial NOT NULL UNIQUE,
	-- brand_no(品牌編號) : brand_no(品牌編號)
	brand_no varchar(10) NOT NULL UNIQUE,
	-- brand_nm(品牌名稱) : brand_nm(品牌名稱)
	-- 
	brand_nm varchar(30) NOT NULL,
	-- brand_payday(收款天數) : brand_payday(收款天數)
	brand_payday numeric(3) NOT NULL,
	-- delivery_address(送貨地址) : delivery_address(送貨地址)
	delivery_address varchar(100),
	-- pack_desc(包裝說明) : pack_desc(包裝說明)
	pack_desc varchar(200),
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23),
	PRIMARY KEY (pk_brandm)
) WITHOUT OIDS;


-- colorm(顏色主檔) : COLORM(顏色主檔)
CREATE TABLE colorm
(
	-- pk_colorm(主鍵值_顏色主檔) : pk_colorm(主鍵值_顏色主檔)
	pk_colorm serial NOT NULL UNIQUE,
	-- color_no(顏色代號) : color_no(顏色代號)
	color_no varchar(10) NOT NULL,
	-- color_nm(顏色名稱) : color_nm(顏色名稱)
	-- 
	color_nm varchar(200) NOT NULL,
	-- color_nm_en(英文顏色名稱) : color_nm_en(英文顏色名稱)
	color_nm_en varchar(200),
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial NOT NULL,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23) NOT NULL,
	CONSTRAINT PK_COLORM PRIMARY KEY (pk_colorm, color_no)
) WITHOUT OIDS;


-- customd(客戶連絡人明細檔)
CREATE TABLE customd
(
	-- pk_customd(主鍵值_客戶連絡人明細檔) : pk_customd(主鍵值_客戶連絡人明細檔)
	pk_customd serial NOT NULL UNIQUE,
	-- pk_customm(主鍵值_客戶主檔) : pk_customm(主鍵值_客戶主檔)
	pk_customm int NOT NULL,
	-- customd_contact(客戶連絡人) : customd_contractor(客戶連絡人)
	customd_contact varchar(30) NOT NULL,
	PRIMARY KEY (pk_customd)
) WITHOUT OIDS;


-- customdbrandm
CREATE TABLE customdbrandm
(
	-- pk_custombrandm(主鍵值_客戶明細品牌資料) : pk_custombrandm(主鍵值_客戶明細品牌資料)
	pk_custombrandm serial NOT NULL UNIQUE,
	-- pk_customd(主鍵值_客戶連絡人明細檔) : pk_customd(主鍵值_客戶連絡人明細檔)
	pk_customd int NOT NULL,
	-- pk_brandm(主鍵值_品牌主檔) : pk_brandm(主鍵值_品牌主檔)
	pk_brandm int NOT NULL,
	PRIMARY KEY (pk_custombrandm)
) WITHOUT OIDS;


-- customm(客戶主檔)
CREATE TABLE customm
(
	-- pk_customm(主鍵值_客戶主檔) : pk_customm(主鍵值_客戶主檔)
	pk_customm serial NOT NULL UNIQUE,
	-- customm_no(客戶編號) : customm_no(客戶編號)
	customm_no varchar(15) NOT NULL UNIQUE,
	-- customm_nm(客戶簡稱) : customm_nm(客戶簡稱)
	customm_nm varchar(20) NOT NULL,
	-- customm_type(客戶類別) : custom_type(客戶類別)
	customm_type int NOT NULL,
	-- customm_f_nm(客戶全名) : customm_f_nm(客戶全名)
	customm_f_nm varchar(100),
	-- customm_f_nm_en(客戶英文名稱) : customm_f_nm_en(客戶英文名稱)
	customm_f_nm_en varchar(100),
	-- customm_manager(負責人) : customm_manager(負責人)
	customm_manager varchar(20),
	-- customm_stopdate(停用日期) : customm_stopdate(停用日期)
	customm_stopdate char(8),
	-- cutsomm_address(客戶地址) : cutsomm_address(客戶地址)
	cutsomm_address varchar(200),
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23),
	PRIMARY KEY (pk_customm)
) WITHOUT OIDS;


-- customs(連絡人明細資料)
CREATE TABLE customs
(
	-- pk_customs(連絡人明細資料) : pk_customs(連絡人明細資料)
	pk_customs serial NOT NULL UNIQUE,
	-- pk_customd(主鍵值_客戶連絡人明細檔) : pk_customd(主鍵值_客戶連絡人明細檔)
	pk_customd int NOT NULL,
	-- pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)
	pk_s_kindd int NOT NULL,
	-- customs_nm(連絡人明細) : customs_nm(連絡人明細)
	customs_nm varchar(30) NOT NULL,
	PRIMARY KEY (pk_customs)
) WITHOUT OIDS;


-- matm(材料主檔) : MATM(材料主檔)
CREATE TABLE matm
(
	-- pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)
	pk_matm serial NOT NULL UNIQUE,
	-- mat_no(材料代號) : mat_no(材料代號)
	mat_no varchar(10) NOT NULL UNIQUE,
	-- mat_nm(材料名稱) : mat_nm(材料名稱)
	mat_nm varchar(300) NOT NULL,
	-- mat_nm_en(材料英文名稱) : mat_nm_en(材料英文名稱)
	mat_nm_en varchar(300) NOT NULL,
	-- pk_colorm(主鍵值_顏色主檔) : pk_colorm(主鍵值_顏色主檔)
	pk_colorm int NOT NULL,
	-- pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)
	pk_s_kindm int NOT NULL,
	-- reprdmat_mk(加工材料) : reprdmat_mk(加工材料)
	preprdmat_mk boolean,
	-- exceed_rec_mk(超交允收) : exceed_rec_mk(超交允收)
	exceed_rec_mk boolean,
	-- onway_qty(在途量) : onway_qty(在途量)
	onway_qty numeric(20,6),
	-- safestk_qty(安全存量) : safestk_qty(安全存量)
	safestk_qty numeric(20,6),
	-- purchase_day(購買週期) : purchase_day(購買週期)
	purchase_day numeric(3,0),
	-- unit_price(單價) : unit_price(單價)
	unit_price numeric(11,4),
	-- stop_user(停用人) : stop_user(停用人)
	stop_user varchar(18),
	-- stop_date(停用日期) : stop_date(停用日期)
	stop_date varchar(8),
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial NOT NULL,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23) NOT NULL,
	CONSTRAINT PK_MATIDM PRIMARY KEY (pk_matm)
) WITHOUT OIDS;


-- matvendorm(材料供應商主檔)
CREATE TABLE matvendorm
(
	-- pk_matvendorm(主鍵值_材料供應商主檔) : pk_matvendorm(主鍵值_材料供應商主檔)
	pk_matvendorm serial NOT NULL UNIQUE,
	-- pk_vendorm(主鍵值_供應商主檔) : pk_vendorm(主鍵值_供應商主檔)
	pk_vendorm int NOT NULL UNIQUE,
	-- pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)
	pk_matm int NOT NULL UNIQUE,
	PRIMARY KEY (pk_matvendorm)
) WITHOUT OIDS;


-- partm(部位主檔) : PARTM(部位主檔)
CREATE TABLE partm
(
	-- pk_partm(主鍵值_部位主檔) : pk_partm(主鍵值_部位主檔)
	pk_partm serial NOT NULL UNIQUE,
	-- pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)
	pk_s_kindd int NOT NULL UNIQUE,
	-- part_no(部位代號) : part_no(部位代號)
	part_no varchar(10) NOT NULL UNIQUE,
	-- part_nm(部位名稱) : part_nm(部位名稱)
	part_nm varchar(100) NOT NULL,
	-- part_nm_en(英文部位名稱) : part_nm_en(英文部位名稱)
	part_nm_en varchar(100),
	-- part_mk(主副料註記) : part_mk(主副料註記)
	part_mk boolean,
	-- part_addrte_mk(加成註記) : part_addrte_mk(加成註記)
	part_addrte_mk boolean,
	-- stop_date(停用日期) : stop_date(停用日期)
	stop_date varchar(8),
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial NOT NULL,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23) NOT NULL,
	CONSTRAINT PK_PARTM PRIMARY KEY (pk_partm)
) WITHOUT OIDS;


-- preprdmatd(加工材料結構明細檔) : PREMATIDM(加工材料結構檔)
CREATE TABLE preprdmatd
(
	-- pk_preprdmatd(主鍵值_加工材料結構明細檔) : pk_preprdmatd(主鍵值_加工材料結構明細檔)
	pk_preprdmatd serial NOT NULL UNIQUE,
	-- pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)
	pk_matm int NOT NULL UNIQUE,
	-- preprd_rate(加工比率) : preprd_rate(加工比率)
	preprd_rate numeric(6,4) NOT NULL,
	-- preprd_buymat_mk(代料) : preprd_buymat_mk(代料)
	preprd_buymat_mk boolean NOT NULL,
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial NOT NULL,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23) NOT NULL,
	-- pk_preprdmatm(主鍵值_加工材料結構主檔) : pk_preprdmatm(主鍵值_加工材料結構主檔)
	pk_preprdmatm int NOT NULL UNIQUE,
	CONSTRAINT PK_PREMATIDM PRIMARY KEY (pk_preprdmatd)
) WITHOUT OIDS;


-- preprdmatm(加工材料結樠主檔) : preprdmatm(加工材料結樠主檔)
CREATE TABLE preprdmatm
(
	-- pk_preprdmatm(主鍵值_加工材料結構主檔) : pk_preprdmatm(主鍵值_加工材料結構主檔)
	pk_preprdmatm serial NOT NULL UNIQUE,
	-- pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)
	pk_matm int NOT NULL UNIQUE,
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23),
	CONSTRAINT PK_PREMATIDD PRIMARY KEY (pk_preprdmatm)
) WITHOUT OIDS;


-- SIZES : SIZES(SIZE明細檔)
CREATE TABLE SIZES
(
	-- pk_sizes(主鍵值_SIZE主檔) : pk_sizes(主鍵值_SIZE主檔)
	pk_sizes serial NOT NULL UNIQUE,
	-- pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)
	pk_s_kindd int NOT NULL UNIQUE,
	-- size_run(SIZE編號) : size_run(SIZE編號)
	size_run varchar(20) NOT NULL,
	-- size_idx(SIZE排序號) : size_idx(SIZE排序號)
	size_idx numeric(8,2) NOT NULL,
	CONSTRAINT PK_SIZES PRIMARY KEY (pk_sizes)
) WITHOUT OIDS;


-- vendord(供應商明細)
CREATE TABLE vendord
(
	-- pk_vendord(主鍵值_供應商明細檔) : pk_vendord(主鍵值_供應商明細檔)
	pk_vendord serial NOT NULL UNIQUE,
	-- pk_vendorm(主鍵值_供應商主檔) : pk_vendorm(主鍵值_供應商主檔)
	pk_vendorm int NOT NULL,
	-- vendord_contact(連絡人)
	vendord_contact varchar(30),
	PRIMARY KEY (pk_vendord)
) WITHOUT OIDS;


-- vendorm(供應商主檔) : VENDORM(供應商主檔)
CREATE TABLE vendorm
(
	-- pk_vendorm(主鍵值_供應商主檔) : pk_vendorm(主鍵值_供應商主檔)
	pk_vendorm serial NOT NULL UNIQUE,
	-- vendorm_no(供應商編號) : 供應商編號
	vendorm_no varchar(10) NOT NULL UNIQUE,
	-- vendorm_nm(供應商簡稱) : vendorm_nm(供應商簡稱)
	vendorm_nm varchar(20) NOT NULL,
	-- vendorm_f_nm(供應商全名) : 供應商全名
	vendorm_f_nm varchar(50),
	-- vendorm_uni_no(統一編號) : 統一編號
	vendorm_uni_no varchar(20),
	-- vendorm_type(供應商類別) : 供應商類別
	vendorm_type int NOT NULL,
	-- vendorm_kind(供應商性質) : 供應商性質
	vendorm_kind int NOT NULL,
	-- vendorm_purchasepolicy(採購政策) : 採購政策
	vendorm_purchasepolicy int,
	-- vendorm_tradeticket(交易票據) : 交易票據
	vendorm_tradeticket int,
	-- vendorm_ticketrate(票據比率) : 票據比率
	vendorm_ticketrate numeric(5,2),
	-- vendorm_taxsource(稅金來源) : 稅金來源
	vendorm_taxsource int,
	-- vendorm_taxrate(稅金比率) : 稅金比率
	vendorm_taxrate numeric(5,2),
	-- vendorm_deductrate(扣款比率) : 扣款比率
	vendorm_deductrate numeric(5,2),
	-- vendorm_payment(交易方式) : 交易方式
	vendorm_payment int,
	-- vendorm_payday(付款天數) : 付款天數
	vendorm_payday numeric(4,0),
	-- vendorm_coin(交易幣別) : 交易幣別
	vendorm_coin int,
	-- vendorm_manager(負責人) : 負責人
	vendorm_manager varchar(20),
	-- vendorm_expirydate(停用日期) : 停用日期
	vendorm_expirydate varchar(8),
	-- vendorm_sourcemark(資料來源) : 資料來源
	vendorm_sourcemark char(1) NOT NULL,
	-- vendorm_address(地址) : vendorm_address(地址)
	vendorm_address varchar(100),
	-- modify_USER(異動人) : modify_USER(異動人)
	modify_USER serial NOT NULL,
	-- modify_dt(異動時間) : modify_dt(異動時間)
	-- currentDateTime().toString('yyyy/MM/dd HH:mm:ss:zzz')
	modify_dt varchar(23) NOT NULL,
	CONSTRAINT PK_VENDORM PRIMARY KEY (pk_vendorm)
) WITHOUT OIDS;


-- vendormm(供應商主檔)
CREATE TABLE vendormm
(
	-- pk_vendromm(主鍵值_供應商主檔) : pk_vendromm(主鍵值_供應商主檔)
	pk_vendromm serial NOT NULL UNIQUE,
	-- vendorm_no(供應商編號) : vendorm_no(供應商編號)
	vendorm_no varchar(10) NOT NULL UNIQUE,
	-- vendorm_nm(供應商簡稱) : vendorm_nm(供應商簡稱)
	vendorm_nm varchar(20),
	-- vendorm_f_nm(供應商全名) : vendorm_f_nm(供應商全名)
	vendorm_f_nm varchar(50),
	-- uni_no(統一編號) : uni_no(統一編號)
	uni_no varchar(20),
	-- vendorm_type(供應商類別) : vendorm_type(供應商類別)
	-- from kindd A9
	vendorm_type int,
	PRIMARY KEY (pk_vendromm)
) WITHOUT OIDS;


-- vendors(連絡人明細資料)
CREATE TABLE vendors
(
	-- pk_vendors(主鍵值_連絡人明細資料) : pk_vendors(主鍵值_連絡人明細資料)
	pk_vendors serial NOT NULL UNIQUE,
	-- pk_vendord(主鍵值_供應商明細檔) : pk_vendord(主鍵值_供應商明細檔)
	pk_vendord int NOT NULL,
	-- pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)
	pk_s_kindm int NOT NULL,
	-- vendors_nm(連絡人明細資料) : vendors_nm(連絡人明細資料)
	vendors_nm varchar(30),
	PRIMARY KEY (pk_vendors)
) WITHOUT OIDS;



/* Create Foreign Keys */

ALTER TABLE customdbrandm
	ADD FOREIGN KEY (pk_brandm)
	REFERENCES brandm (pk_brandm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE matm
	ADD FOREIGN KEY (pk_colorm)
	REFERENCES colorm (pk_colorm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE customdbrandm
	ADD FOREIGN KEY (pk_customd)
	REFERENCES customd (pk_customd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE customs
	ADD FOREIGN KEY (pk_customd)
	REFERENCES customd (pk_customd)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE customd
	ADD FOREIGN KEY (pk_customm)
	REFERENCES customm (pk_customm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE matvendorm
	ADD FOREIGN KEY (pk_matm)
	REFERENCES matm (pk_matm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE preprdmatd
	ADD FOREIGN KEY (pk_matm)
	REFERENCES matm (pk_matm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE preprdmatm
	ADD FOREIGN KEY (pk_matm)
	REFERENCES matm (pk_matm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE preprdmatd
	ADD FOREIGN KEY (pk_preprdmatm)
	REFERENCES preprdmatm (pk_preprdmatm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendors
	ADD FOREIGN KEY (pk_vendord)
	REFERENCES vendord (pk_vendord)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE matvendorm
	ADD FOREIGN KEY (pk_vendorm)
	REFERENCES vendorm (pk_vendorm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE vendord
	ADD FOREIGN KEY (pk_vendorm)
	REFERENCES vendorm (pk_vendorm)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



/* Create Indexes */

-- 同一客戶只可同一連絡人
CREATE UNIQUE INDEX id_pk_customm_customd_contract ON customd (customd_contact);
CREATE UNIQUE INDEX ID_MATM ON matm (pk_matm, pk_colorm);
CREATE UNIQUE INDEX id_partm ON partm (part_no);
CREATE UNIQUE INDEX id_preprdmatd ON preprdmatd (pk_matm);
CREATE INDEX id_sizes ON SIZES (pk_s_kindd);



/* Comments */

COMMENT ON TABLE brandm IS 'brandm(品牌資料)';
COMMENT ON COLUMN brandm.pk_brandm IS 'pk_brandm(主鍵值_品牌主檔) : pk_brandm(主鍵值_品牌主檔)';
COMMENT ON COLUMN brandm.brand_no IS 'brand_no(品牌編號) : brand_no(品牌編號)';
COMMENT ON COLUMN brandm.brand_nm IS 'brand_nm(品牌名稱) : brand_nm(品牌名稱)
';
COMMENT ON COLUMN brandm.brand_payday IS 'brand_payday(收款天數) : brand_payday(收款天數)';
COMMENT ON COLUMN brandm.delivery_address IS 'delivery_address(送貨地址) : delivery_address(送貨地址)';
COMMENT ON COLUMN brandm.pack_desc IS 'pack_desc(包裝說明) : pack_desc(包裝說明)';
COMMENT ON COLUMN brandm.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN brandm.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE colorm IS 'colorm(顏色主檔) : COLORM(顏色主檔)';
COMMENT ON COLUMN colorm.pk_colorm IS 'pk_colorm(主鍵值_顏色主檔) : pk_colorm(主鍵值_顏色主檔)';
COMMENT ON COLUMN colorm.color_no IS 'color_no(顏色代號) : color_no(顏色代號)';
COMMENT ON COLUMN colorm.color_nm IS 'color_nm(顏色名稱) : color_nm(顏色名稱)
';
COMMENT ON COLUMN colorm.color_nm_en IS 'color_nm_en(英文顏色名稱) : color_nm_en(英文顏色名稱)';
COMMENT ON COLUMN colorm.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN colorm.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE customd IS 'customd(客戶連絡人明細檔)';
COMMENT ON COLUMN customd.pk_customd IS 'pk_customd(主鍵值_客戶連絡人明細檔) : pk_customd(主鍵值_客戶連絡人明細檔)';
COMMENT ON COLUMN customd.pk_customm IS 'pk_customm(主鍵值_客戶主檔) : pk_customm(主鍵值_客戶主檔)';
COMMENT ON COLUMN customd.customd_contact IS 'customd_contact(客戶連絡人) : customd_contractor(客戶連絡人)';
COMMENT ON TABLE customdbrandm IS 'customdbrandm';
COMMENT ON COLUMN customdbrandm.pk_custombrandm IS 'pk_custombrandm(主鍵值_客戶明細品牌資料) : pk_custombrandm(主鍵值_客戶明細品牌資料)';
COMMENT ON COLUMN customdbrandm.pk_customd IS 'pk_customd(主鍵值_客戶連絡人明細檔) : pk_customd(主鍵值_客戶連絡人明細檔)';
COMMENT ON COLUMN customdbrandm.pk_brandm IS 'pk_brandm(主鍵值_品牌主檔) : pk_brandm(主鍵值_品牌主檔)';
COMMENT ON TABLE customm IS 'customm(客戶主檔)';
COMMENT ON COLUMN customm.pk_customm IS 'pk_customm(主鍵值_客戶主檔) : pk_customm(主鍵值_客戶主檔)';
COMMENT ON COLUMN customm.customm_no IS 'customm_no(客戶編號) : customm_no(客戶編號)';
COMMENT ON COLUMN customm.customm_nm IS 'customm_nm(客戶簡稱) : customm_nm(客戶簡稱)';
COMMENT ON COLUMN customm.customm_type IS 'customm_type(客戶類別) : custom_type(客戶類別)';
COMMENT ON COLUMN customm.customm_f_nm IS 'customm_f_nm(客戶全名) : customm_f_nm(客戶全名)';
COMMENT ON COLUMN customm.customm_f_nm_en IS 'customm_f_nm_en(客戶英文名稱) : customm_f_nm_en(客戶英文名稱)';
COMMENT ON COLUMN customm.customm_manager IS 'customm_manager(負責人) : customm_manager(負責人)';
COMMENT ON COLUMN customm.customm_stopdate IS 'customm_stopdate(停用日期) : customm_stopdate(停用日期)';
COMMENT ON COLUMN customm.cutsomm_address IS 'cutsomm_address(客戶地址) : cutsomm_address(客戶地址)';
COMMENT ON COLUMN customm.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN customm.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE customs IS 'customs(連絡人明細資料)';
COMMENT ON COLUMN customs.pk_customs IS 'pk_customs(連絡人明細資料) : pk_customs(連絡人明細資料)';
COMMENT ON COLUMN customs.pk_customd IS 'pk_customd(主鍵值_客戶連絡人明細檔) : pk_customd(主鍵值_客戶連絡人明細檔)';
COMMENT ON COLUMN customs.pk_s_kindd IS 'pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)';
COMMENT ON COLUMN customs.customs_nm IS 'customs_nm(連絡人明細) : customs_nm(連絡人明細)';
COMMENT ON TABLE matm IS 'matm(材料主檔) : MATM(材料主檔)';
COMMENT ON COLUMN matm.pk_matm IS 'pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)';
COMMENT ON COLUMN matm.mat_no IS 'mat_no(材料代號) : mat_no(材料代號)';
COMMENT ON COLUMN matm.mat_nm IS 'mat_nm(材料名稱) : mat_nm(材料名稱)';
COMMENT ON COLUMN matm.mat_nm_en IS 'mat_nm_en(材料英文名稱) : mat_nm_en(材料英文名稱)';
COMMENT ON COLUMN matm.pk_colorm IS 'pk_colorm(主鍵值_顏色主檔) : pk_colorm(主鍵值_顏色主檔)';
COMMENT ON COLUMN matm.pk_s_kindm IS 'pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)';
COMMENT ON COLUMN matm.preprdmat_mk IS 'reprdmat_mk(加工材料) : reprdmat_mk(加工材料)';
COMMENT ON COLUMN matm.exceed_rec_mk IS 'exceed_rec_mk(超交允收) : exceed_rec_mk(超交允收)';
COMMENT ON COLUMN matm.onway_qty IS 'onway_qty(在途量) : onway_qty(在途量)';
COMMENT ON COLUMN matm.safestk_qty IS 'safestk_qty(安全存量) : safestk_qty(安全存量)';
COMMENT ON COLUMN matm.purchase_day IS 'purchase_day(購買週期) : purchase_day(購買週期)';
COMMENT ON COLUMN matm.unit_price IS 'unit_price(單價) : unit_price(單價)';
COMMENT ON COLUMN matm.stop_user IS 'stop_user(停用人) : stop_user(停用人)';
COMMENT ON COLUMN matm.stop_date IS 'stop_date(停用日期) : stop_date(停用日期)';
COMMENT ON COLUMN matm.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN matm.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE matvendorm IS 'matvendorm(材料供應商主檔)';
COMMENT ON COLUMN matvendorm.pk_matvendorm IS 'pk_matvendorm(主鍵值_材料供應商主檔) : pk_matvendorm(主鍵值_材料供應商主檔)';
COMMENT ON COLUMN matvendorm.pk_vendorm IS 'pk_vendorm(主鍵值_供應商主檔) : pk_vendorm(主鍵值_供應商主檔)';
COMMENT ON COLUMN matvendorm.pk_matm IS 'pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)';
COMMENT ON TABLE partm IS 'partm(部位主檔) : PARTM(部位主檔)';
COMMENT ON COLUMN partm.pk_partm IS 'pk_partm(主鍵值_部位主檔) : pk_partm(主鍵值_部位主檔)';
COMMENT ON COLUMN partm.pk_s_kindd IS 'pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)';
COMMENT ON COLUMN partm.part_no IS 'part_no(部位代號) : part_no(部位代號)';
COMMENT ON COLUMN partm.part_nm IS 'part_nm(部位名稱) : part_nm(部位名稱)';
COMMENT ON COLUMN partm.part_nm_en IS 'part_nm_en(英文部位名稱) : part_nm_en(英文部位名稱)';
COMMENT ON COLUMN partm.part_mk IS 'part_mk(主副料註記) : part_mk(主副料註記)';
COMMENT ON COLUMN partm.part_addrte_mk IS 'part_addrte_mk(加成註記) : part_addrte_mk(加成註記)';
COMMENT ON COLUMN partm.stop_date IS 'stop_date(停用日期) : stop_date(停用日期)';
COMMENT ON COLUMN partm.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN partm.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE preprdmatd IS 'preprdmatd(加工材料結構明細檔) : PREMATIDM(加工材料結構檔)';
COMMENT ON COLUMN preprdmatd.pk_preprdmatd IS 'pk_preprdmatd(主鍵值_加工材料結構明細檔) : pk_preprdmatd(主鍵值_加工材料結構明細檔)';
COMMENT ON COLUMN preprdmatd.pk_matm IS 'pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)';
COMMENT ON COLUMN preprdmatd.preprd_rate IS 'preprd_rate(加工比率) : preprd_rate(加工比率)';
COMMENT ON COLUMN preprdmatd.preprd_buymat_mk IS 'preprd_buymat_mk(代料) : preprd_buymat_mk(代料)';
COMMENT ON COLUMN preprdmatd.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN preprdmatd.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON COLUMN preprdmatd.pk_preprdmatm IS 'pk_preprdmatm(主鍵值_加工材料結構主檔) : pk_preprdmatm(主鍵值_加工材料結構主檔)';
COMMENT ON TABLE preprdmatm IS 'preprdmatm(加工材料結樠主檔) : preprdmatm(加工材料結樠主檔)';
COMMENT ON COLUMN preprdmatm.pk_preprdmatm IS 'pk_preprdmatm(主鍵值_加工材料結構主檔) : pk_preprdmatm(主鍵值_加工材料結構主檔)';
COMMENT ON COLUMN preprdmatm.pk_matm IS 'pk_matm(主鍵值_材料主檔) : pk_matm(材料主檔)';
COMMENT ON COLUMN preprdmatm.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN preprdmatm.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE SIZES IS 'SIZES : SIZES(SIZE明細檔)';
COMMENT ON COLUMN SIZES.pk_sizes IS 'pk_sizes(主鍵值_SIZE主檔) : pk_sizes(主鍵值_SIZE主檔)';
COMMENT ON COLUMN SIZES.pk_s_kindd IS 'pk_s_kindd(主鍵值_類別明細) : pk_s_kindd(主鍵值_類別明細)';
COMMENT ON COLUMN SIZES.size_run IS 'size_run(SIZE編號) : size_run(SIZE編號)';
COMMENT ON COLUMN SIZES.size_idx IS 'size_idx(SIZE排序號) : size_idx(SIZE排序號)';
COMMENT ON TABLE vendord IS 'vendord(供應商明細)';
COMMENT ON COLUMN vendord.pk_vendord IS 'pk_vendord(主鍵值_供應商明細檔) : pk_vendord(主鍵值_供應商明細檔)';
COMMENT ON COLUMN vendord.pk_vendorm IS 'pk_vendorm(主鍵值_供應商主檔) : pk_vendorm(主鍵值_供應商主檔)';
COMMENT ON COLUMN vendord.vendord_contact IS 'vendord_contact(連絡人)';
COMMENT ON TABLE vendorm IS 'vendorm(供應商主檔) : VENDORM(供應商主檔)';
COMMENT ON COLUMN vendorm.pk_vendorm IS 'pk_vendorm(主鍵值_供應商主檔) : pk_vendorm(主鍵值_供應商主檔)';
COMMENT ON COLUMN vendorm.vendorm_no IS 'vendorm_no(供應商編號) : 供應商編號';
COMMENT ON COLUMN vendorm.vendorm_nm IS 'vendorm_nm(供應商簡稱) : vendorm_nm(供應商簡稱)';
COMMENT ON COLUMN vendorm.vendorm_f_nm IS 'vendorm_f_nm(供應商全名) : 供應商全名';
COMMENT ON COLUMN vendorm.vendorm_uni_no IS 'vendorm_uni_no(統一編號) : 統一編號';
COMMENT ON COLUMN vendorm.vendorm_type IS 'vendorm_type(供應商類別) : 供應商類別';
COMMENT ON COLUMN vendorm.vendorm_kind IS 'vendorm_kind(供應商性質) : 供應商性質';
COMMENT ON COLUMN vendorm.vendorm_purchasepolicy IS 'vendorm_purchasepolicy(採購政策) : 採購政策';
COMMENT ON COLUMN vendorm.vendorm_tradeticket IS 'vendorm_tradeticket(交易票據) : 交易票據';
COMMENT ON COLUMN vendorm.vendorm_ticketrate IS 'vendorm_ticketrate(票據比率) : 票據比率';
COMMENT ON COLUMN vendorm.vendorm_taxsource IS 'vendorm_taxsource(稅金來源) : 稅金來源';
COMMENT ON COLUMN vendorm.vendorm_taxrate IS 'vendorm_taxrate(稅金比率) : 稅金比率';
COMMENT ON COLUMN vendorm.vendorm_deductrate IS 'vendorm_deductrate(扣款比率) : 扣款比率';
COMMENT ON COLUMN vendorm.vendorm_payment IS 'vendorm_payment(交易方式) : 交易方式';
COMMENT ON COLUMN vendorm.vendorm_payday IS 'vendorm_payday(付款天數) : 付款天數';
COMMENT ON COLUMN vendorm.vendorm_coin IS 'vendorm_coin(交易幣別) : 交易幣別';
COMMENT ON COLUMN vendorm.vendorm_manager IS 'vendorm_manager(負責人) : 負責人';
COMMENT ON COLUMN vendorm.vendorm_expirydate IS 'vendorm_expirydate(停用日期) : 停用日期';
COMMENT ON COLUMN vendorm.vendorm_sourcemark IS 'vendorm_sourcemark(資料來源) : 資料來源';
COMMENT ON COLUMN vendorm.vendorm_address IS 'vendorm_address(地址) : vendorm_address(地址)';
COMMENT ON COLUMN vendorm.modify_USER IS 'modify_USER(異動人) : modify_USER(異動人)';
COMMENT ON COLUMN vendorm.modify_dt IS 'modify_dt(異動時間) : modify_dt(異動時間)
currentDateTime().toString(''yyyy/MM/dd HH:mm:ss:zzz'')';
COMMENT ON TABLE vendormm IS 'vendormm(供應商主檔)';
COMMENT ON COLUMN vendormm.pk_vendromm IS 'pk_vendromm(主鍵值_供應商主檔) : pk_vendromm(主鍵值_供應商主檔)';
COMMENT ON COLUMN vendormm.vendorm_no IS 'vendorm_no(供應商編號) : vendorm_no(供應商編號)';
COMMENT ON COLUMN vendormm.vendorm_nm IS 'vendorm_nm(供應商簡稱) : vendorm_nm(供應商簡稱)';
COMMENT ON COLUMN vendormm.vendorm_f_nm IS 'vendorm_f_nm(供應商全名) : vendorm_f_nm(供應商全名)';
COMMENT ON COLUMN vendormm.uni_no IS 'uni_no(統一編號) : uni_no(統一編號)';
COMMENT ON COLUMN vendormm.vendorm_type IS 'vendorm_type(供應商類別) : vendorm_type(供應商類別)
from kindd A9';
COMMENT ON TABLE vendors IS 'vendors(連絡人明細資料)';
COMMENT ON COLUMN vendors.pk_vendors IS 'pk_vendors(主鍵值_連絡人明細資料) : pk_vendors(主鍵值_連絡人明細資料)';
COMMENT ON COLUMN vendors.pk_vendord IS 'pk_vendord(主鍵值_供應商明細檔) : pk_vendord(主鍵值_供應商明細檔)';
COMMENT ON COLUMN vendors.pk_s_kindm IS 'pk_s_kindm(主鍵值_KINDM) : pk_s_kindm(主鍵值_KINDM)';
COMMENT ON COLUMN vendors.vendors_nm IS 'vendors_nm(連絡人明細資料) : vendors_nm(連絡人明細資料)';



