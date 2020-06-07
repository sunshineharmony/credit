# -*- coding:utf-8 -*-
import getpass
import random
import pymysql
import datetime
host = '192.168.56.101'
dbuser = 'dbusername'
dbpass = 'dbpasswd'
dbname = 'credit'
db = pymysql.connect(host, dbuser, dbpass, dbname, charset='utf8')
cursor = db.cursor()

def en_sign_up(user, password, cardid):
    query_sql = "select * from user_info where user_name='%s';" % user
    create_userinfo_sql = "insert into user_info (user_name,user_passwd,user_card_id)" \
                          "values('%s','%s','%s');" % (user, password, cardid)
    create_user_status_sql = "insert into user_status (user_name,user_fail_count,user_status) values('%s','0','%s');" % (user, 'unlocked')
    create_credit_info_sql = "insert into credit_info (credit_user_name,credit_card_number," \
                             "credit_sum,credit_balance,credit_payment,credit_amount,credit_interest_rate," \
                             "credit_interest) values('%s','%s','50000','50000','0','0','0.05','0');" % (
                                 user, cardid)
    cursor.execute(query_sql)
    db.commit()
    re = cursor.execute(query_sql)
    if re == 0:
        cursor.execute(create_userinfo_sql)
        print("\033[36;1m update table user_info success\033[0m")
        cursor.execute(create_user_status_sql)
        print("\033[36;1m update table user_status success\033[0m")
        cursor.execute(create_credit_info_sql)
        print("\033[36;1m update table credit_info success\033[0m")
        db.commit()
        print("\033[36;1m create user %s success\033[0m" % user)
    else:
        print("user %s is  exist"% user)


def en_login(user, auth):
    if user == 'admin':
        query_sql = "select * from user_info where user_name='%s';" % user
        count_sql = "select count(*) from user_info where user_name='%s';" % user
        query_user_status_sql = "select * from user_status where user_name='%s';" % user
        user_status_list = []
        cursor.execute(query_user_status_sql)
        for ss in cursor.fetchall():
            user_status_list.append(ss[1])
            user_status_list.append(ss[2])
            user_status_list.append(ss[3])
        cursor.execute(count_sql)
        db.commit()
        for data in cursor.fetchall():
            if data[0] != 0:
                if user_status_list[2] == 'unlocked':
                    cursor.execute(query_sql)
                    db.commit()
                    for record in cursor.fetchall():
                        if int(user_status_list[0]) < 3:
                            if auth == record[2]:
                                print("\033[46;1m login success\033[0m")
                                print("\033[46;1m Welcome administrator login\033[0m")
                                unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                                  " where user_name='%s';" % (user)
                                cursor.execute(unlock_user_sql)
                                db.commit()
                                while True:
                                    print("\033[36;1mUser information center\033[0m")
                                    print("\033[37;1m1 User information management   \033[0m")

                                    print("\033[37;1m9 exit credit center\033[0m")
                                    v = input("please input your choice:")
                                    if v == '1':
                                        while True:
                                            print(" \033[46;1mUser information center\033[0m")
                                            print("\033[37;1m1\tquery user info   \033[0m")
                                            print("\033[37;1m2\tdelete user info  \033[0m")
                                            print("\033[37;1m3\tchange user passwd  \033[0m")
                                            print("\033[37;1m4\texit user information center  \033[0m")
                                            c = input("please input your choice:")
                                            if c == '1':
                                                en_query_info(user)
                                            elif c == '2':
                                                print("System existing users :")
                                                query_user_sql = "select user_name from user_info where user_name not in ('%s');"% user
                                                cursor.execute(query_user_sql)
                                                db.commit()
                                                usr = []
                                                for u in cursor.fetchall():
                                                    usr.append(u[0])
                                                    print(u[0])
                                                username = input("please input delete user name:")
                                                if username == 'q':
                                                    print("exit delete user ")
                                                elif username in usr:
                                                    en_delete_user(username)
                                                else:
                                                    print("user %s is not exist"% username)
                                            elif c == '3':
                                                query_user_sql = "select user_name from user_info where user_name not in ('%s');" % user
                                                cursor.execute(query_user_sql)
                                                db.commit()
                                                usr = []
                                                print("System existing users :")
                                                for u in cursor.fetchall():
                                                    usr.append(u[0])
                                                    print(u[0])
                                                usr_name = input("please input change username:")
                                                if usr_name == 'q':
                                                    print("exit change password ")
                                                elif usr_name in usr:
                                                    en_change_password(usr_name)
                                                else:
                                                    print("user %s is not exist"% usr_name)
                                            elif c == '4':
                                                print("exit user information center")
                                                break
                                            else:
                                                print("\033[31;1m input error,please input again\033[0m")
                                    elif v == '9':
                                        print("\033[46;1m user %s exit\033[0m" % user)
                                        break
                                    else:
                                        print("\033[41;1m input error\033[0m")
                            else:
                                print("\033[41;1mThe password is error\033[0m")
                                user_status_list[0] = int(user_status_list[0]) + 1
                                update_user_status_sql = "update user_status set user_fail_count='%s',user_last_fail_time=now() " \
                                                         "where user_name='%s';" % (user_status_list[0], user)
                                cursor.execute(update_user_status_sql)
                                db.commit()
                                break
                        else:
                            print("\033[41;1m user %s is locked\033[0m" % user)
                            lock_user_sql = "update user_status set user_status='locked'" \
                                            " where user_name='%s';" % user
                            cursor.execute(lock_user_sql)
                            db.commit()
                            break
                else:
                    print("\033[41;1m user %s is locked\033[0m" % user)
                    unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                      " where user_name='%s';" % user
                    now_date = datetime.datetime.now()
                    t_str = user_status_list[1]
                    last_date = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
                    count = now_date - last_date
                    print(count.seconds)
                    print("\033[41;1m User lock time has lasted %s seconds\033[0m" % count.seconds)
                    if count.seconds > 300:
                        cursor.execute(unlock_user_sql)
                        db.commit()
                        print("\033[36;1mUser %s lock time more than 300 seconds, unlock automatically\033[0m" % user)
                    else:
                        pass
                    break
            else:
                print("\033[31;1m user %s is not exist\033[0m" % user)
                break
    else:
        query_sql = "select * from user_info where user_name='%s';" % user
        count_sql = "select count(*) from user_info where user_name='%s';" % user
        query_user_status_sql = "select * from user_status where user_name='%s';" % user
        user_status_list = []
        cursor.execute(query_user_status_sql)
        for ss in cursor.fetchall():
            user_status_list.append(ss[1])
            user_status_list.append(ss[2])
            user_status_list.append(ss[3])
        cursor.execute(count_sql)
        db.commit()
        for data in cursor.fetchall():
            if data[0] != 0:
                if user_status_list[2] == 'unlocked':
                    cursor.execute(query_sql)
                    db.commit()
                    for record in cursor.fetchall():
                        if int(user_status_list[0]) < 3:
                            if auth == record[2]:
                                print("\033[36;1m login success\033[0m")
                                unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                                  " where user_name='%s';" % user
                                cursor.execute(unlock_user_sql)
                                db.commit()
                                while True:
                                    print("\033[36;1mWelcome to credit center\033[0m")
                                    print("\033[37;1m1 credit shopping mall\033[0m")
                                    print("\033[37;1m2 transfer accounts\033[0m")
                                    print("\033[37;1m3 repayment\033[0m")
                                    print("\033[37;1m4 spending bill   \033[0m")
                                    print("\033[37;1m5 User information management   \033[0m")
                                    print("\033[37;1m9 exit credit center\033[0m")
                                    v = input("please input your choice:")
                                    if v == '1':
                                        print("\033[46;1m Welcome to shop mall \033[0m")
                                        en_shop_mall(user)
                                    elif v == '2':
                                        print("\033[46;1mWelcome to transfer accounts center\033[0m")
                                        en_transfer(user)
                                    elif v == '3':
                                        print("\033[46;1mWelcome to repayment center\033[0m")
                                        query_credit_info_sql = "select * from credit_info where credit_user_name='%s';" % user
                                        cursor.execute(query_credit_info_sql)
                                        for r in cursor.fetchall():
                                            print("private float userDebt :%s" %r[5])
                                        try:
                                            num = int(input("please input repayment count:"))
                                        except ValueError:
                                            print("\033[41;1mInput error,Please enter Numbers\033[0m")
                                        else:
                                            en_repayment(user, num)
                                    elif v == '4':
                                        en_query_bill(user)
                                    elif v == '5':
                                        while True:
                                            print(" \033[46;1mUser information center\033[0m")
                                            print("\033[37;1m1\tquery user info   \033[0m")
                                            print("\033[37;1m2\tdelete user info  \033[0m")
                                            print("\033[37;1m3\tchange user password  \033[0m")
                                            print("\033[37;1m4\texit user information center  \033[0m")
                                            c = input("please input your choice:")
                                            if c == '1':
                                                en_user_query_info(user)
                                            elif c == '2':
                                                print("current login user is : %s" % user)
                                                d = input("delete current user?(y/n)")
                                                if d == 'y' or d == 'Y' or d == 'yes' or d == 'YES':
                                                    en_user_delete_user(user)
                                                    print("\033[41;1muser %s is not exist\n exit system\033[0m"% user)
                                                    exit()
                                                elif d == 'n' or d == 'N' or d == 'no' or d == 'NO':
                                                    print("exit delete user")
                                                else:
                                                    print("input error")
                                            elif c == '3':
                                                en_change_password(user)

                                            elif c == '4':
                                                print("exit user information center")
                                                break
                                            else:
                                                print("\033[31;1m input error,please input again\033[0m")

                                    elif v == '9':
                                        print("\033[46;1m user %s exit\033[0m" % user)
                                        break
                                    else:
                                        print("\033[41;1m input error\033[0m")
                            else:
                                print("\033[41;1mThe password is error\033[0m")
                                user_status_list[0] = int(user_status_list[0]) + 1
                                update_user_status_sql = "update user_status set user_fail_count='%s',user_last_fail_time=now() " \
                                                         "where user_name='%s';" % (user_status_list[0], user)
                                cursor.execute(update_user_status_sql)
                                db.commit()
                                break
                        else:
                            print("\033[41;1m user %s is locked\033[0m" % user)
                            lock_user_sql = "update user_status set user_status='locked'" \
                                            " where user_name='%s';" % (user)
                            cursor.execute(lock_user_sql)
                            db.commit()
                            break
                else:
                    print("\033[41;1m user %s is locked\033[0m" % user)
                    unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                      " where user_name='%s';" % (user)
                    now_date = datetime.datetime.now()
                    t_str = user_status_list[1]
                    last_date = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
                    count = now_date - last_date
                    print(count.seconds)
                    print("\033[41;1m User lock time has lasted %s seconds\033[0m" % count.seconds)
                    if count.seconds > 300:
                        cursor.execute(unlock_user_sql)
                        db.commit()
                        print("\033[36;1mUser %s lock time more than 300 seconds, unlock automatically\033[0m" % user)
                    else:
                        pass
                    break
            else:
                print("\033[31;1m user %s is not exist\033[0m" % user)
                break


def en_user_query_info(user):
    user_info__sql = "select * from user_info where user_name='%s';"% user
    user_status_sql = "select * from user_status where user_name='%s';"% user
    credit_info_sql = "select * from credit_info where credit_user_name='%s';"% user
    cursor.execute(user_info__sql)
    db.commit()
    print("\033[34;1m user_name\tpassword \tcard_id")
    for data in cursor.fetchall():
        print(data[1], '\t', data[2], '\t', data[3])
    print(" user_name\tuser_fail_count\tuser_last_fail_time\tuser_status")
    cursor.execute(user_status_sql)
    db.commit()
    for data1 in cursor.fetchall():
        print(data1[0], '\t', data1[1], '\t', data1[2], '\t', data1[3])
    print(" user_name\tcredit_card_number\tcredit_sum\tcredit_balance\tcredit_payment")
    cursor.execute(credit_info_sql)
    db.commit()
    for data2 in cursor.fetchall():
        print(data2[1], '\t', data2[2], '\t', data2[3], '\t', data2[4],'\t',data2[5])
    print("\033[0m")
def en_query_info(user):
    user_info__sql = "select * from user_info where user_name not in ('%s') ;" % user
    user_status_sql = "select * from user_status where user_name not in ('%s') ;" % user
    credit_info_sql = "select * from credit_info where credit_user_name not in ('%s') ;" % user
    cursor.execute(user_info__sql)
    db.commit()
    print("\033[34;1m user_name\tpassword \tcard_id")
    for data in cursor.fetchall():
        print(data[1], '\t', data[2], '\t', data[3])
    print(" user_name\tuser_fail_count\tuser_last_fail_time\tuser_status")
    cursor.execute(user_status_sql)
    db.commit()
    for data1 in cursor.fetchall():
        print(data1[0], '\t', data1[1], '\t', data1[2], '\t', data1[3])
    print(" user_name\tcredit_card_number\tcredit_sum\tcredit_balance\tcredit_payment")
    cursor.execute(credit_info_sql)
    db.commit()
    for data2 in cursor.fetchall():
        print(data2[1], '\t', data2[2], '\t', data2[3], '\t', data2[4],'\t',data2[5])
    print("\033[0m")

def en_user_delete_user(usr_name):
    count_sql = "select count(*) from user_info where user_name='%s';" % usr_name
    del_user_info_sql = "delete from user_info where user_name='%s';" % usr_name
    del_user_status_sql = "delete from user_status where user_name='%s';" % usr_name
    del_credit_info_sql = "delete from credit_info where credit_user_name='%s';" % usr_name
    cursor.execute(count_sql)
    db.commit()
    for data in cursor.fetchall():
        if data[0] != 0:
            cursor.execute(del_user_info_sql)
            print("update table user_info success")
            cursor.execute(del_user_status_sql)
            print("update table user_status success")
            cursor.execute(del_credit_info_sql)
            print("update table credit_info success")
            db.commit()
            print("\033[36;1m user %s delete success\033[0m"% usr_name)
        else:
            print("\033[31;1m user %s is not exist\033[0m" % usr_name)

def en_delete_user(usr_name):
    count_sql = "select count(*) from user_info where user_name not in ('%s');" % usr_name
    del_user_info_sql = "delete from user_info where user_name='%s';" % usr_name
    del_user_status_sql = "delete from user_status where user_name='%s';" % usr_name
    del_credit_info_sql = "delete from credit_info where credit_user_name='%s';" % usr_name
    cursor.execute(count_sql)
    db.commit()
    for data in cursor.fetchall():
        if data[0] != 0:
            cursor.execute(del_user_info_sql)
            print("update table user_info success")
            cursor.execute(del_user_status_sql)
            print("update table user_status success")
            cursor.execute(del_credit_info_sql)
            print("update table credit_info success")
            db.commit()
            print("\033[36;1m user %s delete success\033[0m"% usr_name)
        else:
            print("\033[31;1m user %s is not exist\033[0m" % usr_name)

def en_change_password(user):
    try:
        password = int(input("please input new password:"))
    except ValueError:
        print("please input int number")
    else:
        update_password_sql = "update user_info set user_passwd='%s' where user_name='%s';" % (password, user)
        cursor.execute(update_password_sql)
        db.commit()
        print("update user %s password success"% user)

def en_shop_mall(user):
    credit_list = []
    name_list = []
    price_list = []
    count_list = []
    buy_list = []
    buy_num_list = []
    cost_sum = 0
    print("\033[36;1m++++++++++++++++++product item++++++++++++++++++++\033[0m")
    query_sql = "select * from product_info ;"
    query_credit_info_sql = "select * from credit_info where credit_user_name='%s';" % user
    cursor.execute(query_sql)
    db.commit()
    print("\033[34;1m id\tproduct_class\tproduct_name\tproduct_unit_price\tproduct_count\033[0m")
    for data in cursor.fetchall():
        print(data[0], '\t', data[1], '\t', data[2], '\t', data[3], '\t', data[4])
        name_list.append(data[2])
        price_list.append(data[3])
        count_list.append(data[4])
    cursor.execute(query_credit_info_sql)
    for card in cursor.fetchall():
        credit_list.append(card[3])
        credit_list.append(card[4])
        credit_list.append(card[5])
        credit_list.append(card[6])
    while True:
        print("+++++++++++++++choice+++++++++++++++++")
        print("------1  shopping---------------------")
        print("------2  The end of the shopping------")
        print("++++++++++++++++++++++++++++++++++++++")
        cho = input("please input your choice:")
        if cho == '1':
            product_name = input("please input product_name you want buy:")
            if product_name in name_list:
                num = int(input("please enter %s purchase quantity:" % product_name))
                if num <= int(count_list[name_list.index(product_name)]):
                    c = int(count_list[name_list.index(product_name)])
                    p = int(price_list[name_list.index(product_name)])
                    cost_sum = cost_sum + p * num
                    c = c - num
                    if cost_sum <= int(credit_list[0]):
                        # credit_list[0]为额度 credit_list[1]为余额 credit_list[2]为花费总额 credit_list[3]下月需要还款数
                        credit_list[1] = int(credit_list[1]) - cost_sum
                        credit_list[2] = int(credit_list[2]) + cost_sum
                        credit_list[3] = int(credit_list[3]) + cost_sum
                        buy_list.append(product_name)
                        buy_num_list.append(num)
                        shop_desc = "product:%s,product quantity:%s"%(product_name,num)
                        # update_product_info_sql = "update product_info set product_count='%s' where product_name='%s';" % (c, product_name)
                        # update_credit_info_sql = "update credit_info set credit_payment='%s' where credit_user_name='%s';"% (cost_sum,product_name)
                        # cursor.execute(update_product_info_sql)
                        # cursor.execute(update_credit_info_sql)
                        # db.commit()
                    else:
                        print("金额不足，当前花费:%s,信用卡额度为:%s " % (cost_sum, credit_list[3]))
                else:
                    print("Input exceeding maximum value")
            else:
                print("%s is not exist" % product_name)
        elif cho == '2':
            print("The end of the shopping")
            print("shopping list:")
            for aa in buy_list:
                nu = buy_num_list[buy_list.index(aa)]
                pr = price_list[name_list.index(aa)]
                total = int(nu)*int(pr)
                print("商品名:%s|数量:%s|商品单价:%s|商品总价:%s" % (aa,nu,pr,total))
                echo = "商品名:%s|数量:%s|商品单价:%s|商品总价:%s" % (aa,nu,pr,total)
                insert_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description,credit_bill_type," \
                                         "credit_bill_trade_date,credit_bill_trade_detail,credit_bill_trade_note) values ('%s','%s','shopping'," \
                                         "now(),'%s','-%s');" % (user,shop_desc,echo,total)
                update_credit_info_sql = "update credit_info set credit_balance='%s',credit_payment='%s',credit_amount='%s'" \
                                         "where credit_user_name='%s';" %(credit_list[1],credit_list[2],credit_list[3],user)
                update_product_info_sql = "update product_info set product_count='%s' where product_name='%s';" % (c,product_name)
                cursor.execute(insert_credit_bill_sql)
                cursor.execute(update_credit_info_sql)
                cursor.execute(update_product_info_sql)
                db.commit()
            break
        else:
            print("input not exist")

def en_transfer(user):
    print("current user list:")
    #查询当前系统中的用户名
    query_user_info_sql = "select * from user_info where user_name not in ('admin','%s');"% user
    transfer_usr_list = []
    cursor.execute(query_user_info_sql)
    for u in cursor.fetchall():
        transfer_usr_list.append(u[1])
        print(u[1])
    # 使用列表存储转账发起用户信用卡余额 信用卡花费 信用卡待还金额
    transfer_credit_list = []
    query_transfer_credit_info_sql = "select * from credit_info where credit_user_name='%s';" % user
    cursor.execute(query_transfer_credit_info_sql)
    for f in cursor.fetchall():
        transfer_credit_list.append(f[4])
        transfer_credit_list.append(f[5])
        transfer_credit_list.append(f[6])
    print("\033[46;1m User %s current balance:%s\033[0m" % (user,transfer_credit_list[0]))
    transfer_to = input("please input transfer_to:").strip()
    transfer_amount = input("please input transfer_amount:").strip()
    transfer_description = input("please input transfer_description:").strip()
    # 使用列表存储转账接收用户信用卡余额 信用卡花费 信用卡待还金额
    transfer_to_credit_list = []
    query_transfer_to_credit_info_sql = "select * from credit_info where credit_user_name='%s';"% transfer_to
    cursor.execute(query_transfer_to_credit_info_sql)
    # 使用列表存储转账发起用户信用卡余额 信用卡花费 信用卡待还金额 信用卡额度
    for t in cursor.fetchall():
        transfer_to_credit_list.append(t[4])
        transfer_to_credit_list.append(t[5])
        transfer_to_credit_list.append(t[6])
        transfer_to_credit_list.append(t[3]) #信用卡额度
    transfer_service_charge = int(transfer_amount) * 0.05
    transfer_credit_balance = int(transfer_credit_list[0]) - int(transfer_amount) - int(transfer_service_charge)
    transfer_credit_payment = int(transfer_credit_list[1]) + int(transfer_amount) + int(transfer_service_charge)
    transfer_credit_amount = int(transfer_credit_list[2]) + int(transfer_amount) + int(transfer_service_charge)
    transfer_to_credit_balance = int(transfer_to_credit_list[0]) + int(transfer_amount)
    #对比转账金额与剩余金额，确定转账状态【transfer_status】success/fail
    if transfer_to in transfer_usr_list:
        if int(transfer_amount) > int(transfer_credit_list[0]) :
            transfer_status = "failed"
            insert_transfer_sql = "insert into transfer (transfer_people,transfer_to,transfer_amount," \
                                  "transfer_date,transfer_status,transfer_description) values ('%s','%s','%s',now(),'%s','%s');" \
                                  "" % (user, transfer_to, transfer_amount, transfer_status, transfer_description)
            transfer_credit_bill_trade_detail = "|user:%s |transfer_to user:%s |amount:%s |service_charge:%s" % (
            user, transfer_to, transfer_amount, transfer_service_charge)
            insert_transfer_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description," \
                                              "credit_bill_type,credit_bill_trade_date,credit_bill_trade_detail) values " \
                                              "('%s','%s','transfer',now(),'%s');" % (
                                              user, transfer_status, transfer_credit_bill_trade_detail)
            insert_transfer_to_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description," \
                                                 "credit_bill_type,credit_bill_trade_date,credit_bill_trade_detail) values " \
                                                 "('%s','%s','transfer',now(),'%s');" % (
                                                 transfer_to, transfer_status, transfer_credit_bill_trade_detail)
            cursor.execute(insert_transfer_sql)
            cursor.execute(insert_transfer_credit_bill_sql)
            cursor.execute(insert_transfer_to_credit_bill_sql)
            cursor.execute(query_transfer_to_credit_info_sql)
            db.commit()
            print("Transfer to %s failed"% transfer_to)

        else:
            transfer_status = "success"
            print(transfer_status)
            transfer_credit_bill_trade_detail = "user:%s transfer_to user:%s amount:%s" % (
                user, transfer_to, transfer_amount)
            insert_transfer_sql = "insert into transfer (transfer_people,transfer_to,transfer_amount," \
                                  "transfer_date,transfer_status,transfer_description) values ('%s','%s','%s',now(),'%s','%s');" \
                                  "" % (user, transfer_to, transfer_amount, transfer_status, transfer_description)
            insert_transfer_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description," \
                                              "credit_bill_type,credit_bill_trade_date,credit_bill_trade_detail,credit_bill_trade_note) values " \
                                              "('%s','%s','transfer',now(),'%s','-%s');" % (
                                                  user, transfer_status, transfer_credit_bill_trade_detail,
                                                  transfer_amount)
            insert_transfer_to_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description," \
                                                 "credit_bill_type,credit_bill_trade_date,credit_bill_trade_detail,credit_bill_trade_note) values " \
                                                 "('%s','%s','transfer',now(),'%s','+%s');" % (
                                                     transfer_to, transfer_status,
                                                     transfer_credit_bill_trade_detail,
                                                     transfer_amount)
            update_transfer_credit_info_sql = "update credit_info set credit_balance='%s',credit_payment='%s',credit_amount='%s'where credit_user_name='%s';" % (
                transfer_credit_balance, transfer_credit_payment, transfer_credit_amount, user)
            update_transfer_to_credit_info = "update credit_info set credit_balance='%s' where credit_user_name='%s';" % (
                transfer_to_credit_balance, transfer_to)
            cursor.execute(insert_transfer_sql)
            cursor.execute(insert_transfer_credit_bill_sql)
            cursor.execute(insert_transfer_to_credit_bill_sql)
            cursor.execute(query_transfer_to_credit_info_sql)
            cursor.execute(update_transfer_credit_info_sql)
            cursor.execute(update_transfer_to_credit_info)
            db.commit()
            print("Transfer to %s success" % transfer_to)
    else:
        print("\033[41;1m User %s does not exist in the actionable list\033[0m"% transfer_to)
def en_repayment(user,num):
    repayment_info_list = []
    query_credit_info_sql = "select * from credit_info where credit_user_name='%s';"% user
    cursor.execute(query_credit_info_sql)
    for r in cursor.fetchall():
        #r[3]为用户额度 r[4]为余额 r[5]为当前消费金额  r[6]为下月待还金额
        repayment_info_list.append(r[3])
        repayment_info_list.append(r[4])
        repayment_info_list.append(r[5])
        repayment_info_list.append(r[6])
    if int(repayment_info_list[2]) > 0:
        if num <= int(repayment_info_list[2]):
            credit_balance = int(repayment_info_list[1]) + num
            credit_payment = int(repayment_info_list[2]) - num
            credit_amount = int(repayment_info_list[2]) - num
            credit_bill_description = "repayment %s" % num
            credit_bill_trade_detail = "credit_balance:%s,repayment:%s,credit_amount:%s" % (
            credit_balance, num, credit_amount)
            update_credit_info_sql = "update credit_info set credit_balance='%s',credit_payment='%s'," \
                                     "credit_amount='%s' where credit_user_name='%s';" % (
                                     credit_balance, credit_payment, credit_amount, user)
            insert_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description," \
                                     "credit_bill_type,credit_bill_trade_date,credit_bill_trade_detail) values('%s','%s'," \
                                     "'repayment',now(),'%s');" % (
                                     user, credit_bill_description, credit_bill_trade_detail)
            cursor.execute(update_credit_info_sql)
            cursor.execute(insert_credit_bill_sql)
            db.commit()
            print("\033[36;1m repayment success\033[0m")
            print("\033[36;1m current info :credit_balance %s|credit_payment %s|credit_amount %s\033[0m" % (
            credit_balance, credit_payment, credit_amount))
        else:
            print("\033[31;1m repayment failed \033[0m")
            print("\033[31;1mThe amount of repayment is greater than the amount owed. The current amount owed is %s yuan \033[0m" %repayment_info_list[2])
    else:
        print("\033[31;1m repayment failed \033[0m")
        print("\033[31;1mYou have to pay more than 0\033[0m")

def en_main():
    while True:
        print("\033[34;1m welcome to credit center\033[0m")
        print("\033[34;1mid\tid description\033[0m")
        print("\033[37;1m1\tsign up           \033[0m")
        print("\033[37;1m2\tlogin             \033[0m")
        print("\033[37;1m9\texit credit center\033[0m")
        try:
            value = int(input("\033[34;1m please input your choice id:\033[0m").strip())
        except ValueError:
            print("\033[31;1m please input int type\033[0m")
        else:
            if value == 1:
                username = input("\033[34;1m please input username:\033[0m").strip()
                while True:
                    print("\033[34;1m Please input user %s password:\033[0m" % username)
                    try:
                        password0 = int(input().strip())
                    except ValueError:
                        print("\033[31;1mThe value should be numeral \033[0m")
                    else:
                        print("\033[34;1m Please input user %s password again:\033[0m" % username)
                        try:
                            password1 = int(input())
                        except ValueError:
                            print("\033[31;1mThe value should be numeral \033[0m")
                        else:
                            if password0 == password1:
                                password = password1
                                cardid = random.randint(9999999, 99999999)
                                en_sign_up(username, password, cardid)
                                break
                            else:
                                print("\033[31;1mThe two passwords you entered did not match\033[0m")
            elif value == 2:
                username = input("\033[34;1m please input username:\033[0m").strip()
                password = getpass.getpass().strip()
                en_login(username, password)
            elif value == 9:
                print("\033[36;1m exit credit center\033[0m")
                break
            else:
                print("\033[31;1m input not exist\033[0m")

def en_query_bill(user):
    bill_sql = "select * from credit_bill where credit_bill_user_name='%s';" % user
    cursor.execute(bill_sql)
    user_bill_list = []
    for line in cursor.fetchall():
        print(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
