# -*- coding:utf-8 -*-
import pymysql
host = '192.168.56.101'
dbuser = 'dbusername'
dbpass = 'dbpasswd'
dbname = 'credit'
db = pymysql.connect(host, dbuser, dbpass, dbname, charset='utf8')
cursor = db.cursor()
def init_database():
    drop_user_info_sql = "DROP TABLE IF EXISTS `user_info`;"
    drop_user_status_sql = "DROP TABLE IF EXISTS `user_status`;"
    drop_transfer_sql = "DROP TABLE IF EXISTS `transfer`;"
    drop_product_info_sql = "DROP TABLE IF EXISTS `product_info`;"
    drop_credit_info_sql = "DROP TABLE IF EXISTS `credit_info`;"
    drop_credit_bill_sql = "DROP TABLE IF EXISTS `credit_bill`;"
    create_user_info_sql = "CREATE TABLE `user_info` (" \
                           "`user_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '用户ID'," \
                           "`user_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户名'," \
                           "`user_passwd` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户密码'," \
                           "`user_card_id` int(0) NULL DEFAULT NULL COMMENT '信用卡号'," \
                           "PRIMARY KEY (`user_id`))" \
                           " ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
    create_user_status_sql = "CREATE TABLE `user_status` (`user_name` varchar(32) DEFAULT NULL COMMENT '用户名'," \
                             "`user_fail_count` varchar(32) DEFAULT NULL COMMENT '用户登录失败次数'," \
                             "`user_last_fail_time` varchar(32) DEFAULT NULL COMMENT '用户最近登录失败时间'," \
                             "`user_status` varchar(32) DEFAULT NULL COMMENT '用户当前状态') ENGINE=InnoDB CHARSET=utf8;"
    create_transfer_sql = "CREATE TABLE `transfer` (`transfer_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '转账ID'," \
                          "`transfer_people` varchar(32) DEFAULT NULL COMMENT '转账发起人'," \
                          "`transfer_to` varchar(32) DEFAULT NULL COMMENT '转账接收人'," \
                          "`transfer_amount` int(11) DEFAULT NULL COMMENT '转账金额'," \
                          "`transfer_date` varchar(32) DEFAULT NULL COMMENT '转账时间'," \
                          "`transfer_status` varchar(32) DEFAULT NULL COMMENT '转账状态'," \
                          "`transfer_description` varchar(128) DEFAULT NULL COMMENT '转账描述'" \
                          ",PRIMARY KEY (`transfer_id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
    create_product_info_sql = "CREATE TABLE `product_info` (`product_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '产品编号'," \
                              "`product_class` varchar(32) DEFAULT NULL COMMENT '产品大类'," \
                              "`product_name` varchar(32) DEFAULT NULL COMMENT '产品名称'," \
                              "`product_unit_price` varchar(32) DEFAULT NULL COMMENT '产品单价'," \
                              "`product_count` varchar(32) DEFAULT NULL COMMENT '产品数量'," \
                              "PRIMARY KEY (`product_id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
    create_credit_info_sql = "CREATE TABLE `credit_info` (`credit_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '信用卡表ID'," \
                             "`credit_user_name` varchar(32) DEFAULT NULL COMMENT '信用卡归属用户'," \
                             "`credit_card_number` varchar(32) DEFAULT NULL COMMENT '信用卡号'," \
                             "`credit_sum` varchar(32) DEFAULT NULL COMMENT '额度'," \
                             "`credit_balance` varchar(32) DEFAULT NULL COMMENT '余额'," \
                             "`credit_payment` varchar(32) DEFAULT NULL COMMENT '当前消费金额'," \
                             "`credit_amount` varchar(32) DEFAULT NULL COMMENT '信用卡下月还款金额'," \
                             "`credit_interest_rate` varchar(32) DEFAULT NULL COMMENT '利息率'," \
                             "`credit_interest` varchar(32) DEFAULT NULL COMMENT '利息'" \
                             ",PRIMARY KEY (`credit_id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
    create_credit_bill_sql = "CREATE TABLE `credit_bill` (`credit_bill_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '账单ID'," \
                             "`credit_bill_user_name` varchar(32) DEFAULT NULL COMMENT '账单用户'," \
                             "`credit_bill_description` varchar(512) DEFAULT NULL COMMENT '账单描述'," \
                             "`credit_bill_type` varchar(32) DEFAULT NULL COMMENT '账单类型'," \
                             "`credit_bill_trade_date` varchar(32) DEFAULT NULL COMMENT '交易日期'," \
                             "`credit_bill_trade_detail` varchar(1024) DEFAULT NULL COMMENT '交易明细'," \
                             "`credit_bill_trade_note` varchar(32) DEFAULT NULL COMMENT '交易备注'" \
                             ",PRIMARY KEY (`credit_bill_id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
    print("\033[36;1++++++begin init database++++++\033[0m")
    cursor.execute(drop_user_info_sql)
    print("\033[36;1m drop table user_info success \033[0m")
    cursor.execute(drop_user_status_sql)
    print("\033[36;1m drop table user_status success\033[0m")
    cursor.execute(drop_transfer_sql)
    print("\033[36;1m drop table transfer success\033[0m")
    cursor.execute(drop_product_info_sql)
    print("\033[36;1m drop table product_info success\033[0m")
    cursor.execute(drop_credit_info_sql)
    print("\033[36;1m drop table credit_info success\033[0m")
    cursor.execute(drop_credit_bill_sql)
    print("\033[36;1m drop table credit_bill success\033[0m")
    cursor.execute(create_user_info_sql)
    print("\033[36;1m create table user_info success\033[0m")
    cursor.execute(create_user_status_sql)
    print("\033[36;1m create table user_status success\033[0m")
    cursor.execute(create_transfer_sql)
    print("\033[36;1m create table transfer success\033[0m")
    cursor.execute(create_product_info_sql)
    print("\033[36;1m create table product_info success\033[0m")
    cursor.execute(create_credit_info_sql)
    print("\033[36;1m create table credit_info success\033[0m")
    cursor.execute(create_credit_bill_sql)
    print("\033[36;1m create table credit_bill success\033[0m")
    db.commit()
    print("\033[36;1m+++++init database success+++++\033[0m")
    print("\033[36;1m+++++++end init database+++++++\033[0m")
def init_userinfo():
    init_userinfo_sql = "delete from user_info;"
    init_user_status_sql = "delete from user_status;"
    init_credit_info_sql = "delete from credit_info;"
    create_admin_user_sql= "insert into user_info (user_name,user_passwd,user_card_id) values" \
                           "('admin','admin','666666');"
    create_admin_credit_info_sql = "insert into user_status (user_name,user_fail_count,user_last_fail_time," \
                                   "user_status) values ('admin','0','None','unlocked');"
    create_admin_user_status_sql = "insert into credit_info (credit_user_name,credit_card_number," \
                                   "credit_sum,credit_balance,credit_payment,credit_amount,credit_interest_rate," \
                                   "credit_interest) values ('admin','666666','99999999','99999999','0','0','0.05','0');"
    cursor.execute(init_userinfo_sql)
    cursor.execute(init_user_status_sql)
    cursor.execute(init_credit_info_sql)
    cursor.execute(create_admin_user_sql)
    cursor.execute(create_admin_credit_info_sql)
    cursor.execute(create_admin_user_status_sql)
    db.commit()
    print("\033[36;1m init user_info success\ninit user_status success\ninit credit_info success\033[0m")

def init_user_status():
    update_user_status_sql = "update user_status set user_fail_count='0',user_last_fail_time='',user_status='unlocked';"
    cursor.execute(update_user_status_sql)
    db.commit()
    print("\033[36;1m init user_status success \033[0m")
def init_shop_mall():
    product_list = ['电脑办公', '食品生鲜', '酒水饮料', '时鲜果蔬']
    computer_list = ['macbook', 'thinkpad', 'huawei', 'dellalien']
    computer_price_list = ['12999', '9999', '6999', '8999']
    computer_list_num = ['1000', '1000', '1000', '1000']
    food_list = ['freshbeef', 'freshmilk', 'freshegg', 'freshfish']
    food_price_list = ['30', '10', '50', '10']
    food_list_num = ['1000', '1000', '1000', '1000']
    drink_list = ['frebeer', 'red-wine', 'frejuice', 'purewater']
    drink_price_list = ['20', '500', '50', '20']
    drink_list_num = ['1000', '1000', '1000', '1000']
    vagatables_list = ['freapple', 'banana', 'orange', 'fregrape']
    vagatables_price_list = ['30', '10', '10', '45']
    vagatables_list_num = ['1000', '1000', '1000', '1000']
    init_sql = "delete from product_info; "
    cursor.execute(init_sql)
    db.commit()
    for p in product_list:
        if p == '电脑办公':
            for c in computer_list:
                p_class = p
                p_name = c
                p_price = computer_price_list[computer_list.index(c)]
                p_num = computer_list_num[computer_list.index(c)]
                init_computer_list_sql = "insert into product_info (product_class,product_name,product_unit_price," \
                                         "product_count) values ('%s','%s','%s','%s');" % (
                                         p_class, p_name, p_price, p_num)
                cursor.execute(init_computer_list_sql)
                db.commit()
                #print(p, '\t', c, '\t', computer_price_list[computer_list.index(c)], '\t',
                #      computer_list_num[computer_list.index(c)])
        elif p == '食品生鲜':
            for f in food_list:
                p_class = p
                p_name = f
                p_price = food_price_list[food_list.index(f)]
                p_num = food_list_num[food_list.index(f)]
                init_computer_list_sql = "insert into product_info (product_class,product_name,product_unit_price," \
                                         "product_count) values ('%s','%s','%s','%s');" % (
                                         p_class, p_name, p_price, p_num)
                cursor.execute(init_computer_list_sql)
                db.commit()
                # print(p, '\t', f, '\t', food_price_list[food_list.index(f)], '\t',  food_list_num[food_list.index(f)])
        elif p == '酒水饮料':
            for d in drink_list:
                p_class = p
                p_name = d
                p_price = drink_price_list[drink_list.index(d)]
                p_num = drink_list_num[drink_list.index(d)]
                init_computer_list_sql = "insert into product_info (product_class,product_name,product_unit_price," \
                                         "product_count) values ('%s','%s','%s','%s');" % (
                                         p_class, p_name, p_price, p_num)
                cursor.execute(init_computer_list_sql)
                db.commit()
                # print(p, '\t', d, '\t', drink_price_list[drink_list.index(d)], '\t', drink_list_num[drink_list.index(d)])
        else:
            for v in vagatables_list:
                p_class = p
                p_name = v
                p_price = vagatables_price_list[vagatables_list.index(v)]
                p_num = vagatables_list_num[vagatables_list.index(v)]
                init_computer_list_sql = "insert into product_info (product_class,product_name,product_unit_price," \
                                         "product_count) values ('%s','%s','%s','%s');" % (
                                         p_class, p_name, p_price, p_num)
                cursor.execute(init_computer_list_sql)
                db.commit()
                # print(p, '\t', v, '\t', vagatables_price_list[vagatables_list.index(v)], '\t', vagatables_list_num[vagatables_list.index(v)])
    return (print("\033[36;1m init shop_mall sucess\033[0m"))
if __name__ == '__main__':
    print("++++++++++++++++++++++++")
    print("++++++++init item+++++++")
    print("--1----init database--des:init all database tables like user shop mall etc")
    print("--2----init userinfo--des:delete userinfo")
    print("--3----init user status--des:unlock user")
    print("--4----init shop mall--des:init shop mall")
    print("--9----exit init script--des:exit script")
    print("++++++++++++++++++++++++")
    choice = input("please input init choice:")
    if choice == '1':
        init_database()
        init_shop_mall()
        init_userinfo()
    elif choice == '2':
        init_userinfo()
    elif choice == '3':
        init_user_status()
    elif choice == '4':
        init_shop_mall()
    elif choice == '9':
        exit()
