#!/usr/bin/python
#coding:UTF-8
import MySQLdb
import decimal
import sys
import imp
sys.path.append("..")
sys.path.append("../..")
import tmall_data_analyse.settings as settings
 
imp.reload(sys)
#sys.setdefaultencoding('utf-8')


db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                        user=settings.DATABASES.get(
                            'default').get('USER'),
                        passwd=settings.DATABASES.get(
                            'default').get('PASSWORD'),
                        db=settings.DATABASES.get('default').get('NAME'),
                        charset="utf8",
                        local_infile=1)
con = db.cursor()
con.execute("SELECT SUBSTR(in_out_time FROM 1 FOR 7) from load_transaction_info GROUP BY SUBSTR(in_out_time FROM 1 FOR 7)")
monthlist = con.fetchall()
con.execute("TRUNCATE TABLE t_fee_detail_monthly_info;")

for month in monthlist:
    con.execute("TRUNCATE TABLE tmp_load_transaction_info_monthly;")
    str1 = "INSERT into tmp_load_transaction_info_monthly SELECT * from load_transaction_info WHERE paper_type = '交易出库' and  SUBSTR(in_out_time FROM 1 FOR 7)=\'%s\'"%(month)
    print(str1)
    con.execute(str1)
    con.execute("TRUNCATE TABLE tmp_load_tmallso_info_monthly;")
    str2 = "INSERT into tmp_load_tmallso_info_monthly SELECT * from load_tmallso_info WHERE SUBSTR(paid_time FROM 1 FOR 7)=\'%s\'"%(month)
    print(str2)
    con.execute(str2)
    con.execute("TRUNCATE TABLE tmp_fee_info_monthly;")
    str3 = "INSERT into tmp_fee_info_monthly SELECT * from t_fee_info WHERE SUBSTR(fee_time FROM 1 FOR 7)=\'%s\'"%(month)
    print(str3)
    con.execute(str3)
    db.commit()
    con.execute("UPDATE tmp_load_transaction_info_monthly SET outter_order_id = REPLACE(REPLACE(outter_order_id, CHAR(10), ''), CHAR(13),'');")
    con.execute("SELECT sum(b.actual_paid) FROM tmp_load_transaction_info_monthly a LEFT JOIN tmp_load_tmallso_info_monthly b on a.outter_order_id = b.order_id")
    actual_paid = con.fetchall()
    con.execute("SELECT sum(b.refund) FROM tmp_load_transaction_info_monthly a LEFT JOIN tmp_load_tmallso_info_monthly b on a.outter_order_id = b.order_id")
    refund = con.fetchall()
    
    con.execute("SELECT sum(ifnull(b.logisitic_tax,0)),sum(ifnull(b.logisitic_service,0)),sum(ifnull(b.alipay_service,0)),sum(ifnull(b.tmall,0)),sum(ifnull(b.juhuasuan,0)) FROM tmp_load_transaction_info_monthly a LEFT JOIN tmp_fee_info_monthly b on a.outter_order_id = b.order_id")
    amount = con.fetchall()

    reslist = list(month+actual_paid[0]+amount[0]+refund[0])
    print(reslist)
    print("---------------------------------------",type(reslist),'len  --->',len(reslist))

    exestr = "insert into t_fee_detail_monthly_info (fee_time,out_stock,cainiao_tax,cainiao_service,alipay,tmall,juhuasuan,refund) values(\'%s\',%s,%s,%s,%s,%s,%s,%s)"%(str(reslist[0]),str(reslist[1]),str(reslist[2]),str(reslist[3]),str(reslist[4]),str(reslist[5]),str(reslist[6]),str(reslist[7]))
    print(exestr)
    con.execute(exestr)
    db.commit()
    print("t_fee_detail_monthly_info-->插入一条")

print("t_fee_detail_monthly_info-->插入完成")





