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

def zh_sign_up(user, password, cardid):
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
        print("\033[36;1m 更新表 user_info 成功\033[0m")
        cursor.execute(create_user_status_sql)
        print("\033[36;1m 更新表 user_status 成功\033[0m")
        cursor.execute(create_credit_info_sql)
        print("\033[36;1m 更新表 credit_info 成功\033[0m")
        db.commit()
        print("\033[36;1m 创建用户 %s 成功\033[0m" % user)
    else:
        print("用户 %s 已经存在"% user)


def zh_login(user, auth):
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
                                print("\033[46;1m 登陆成功\033[0m")
                                print("\033[46;1m 欢迎管理员登陆\033[0m")
                                unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                                  " where user_name='%s';" % (user)
                                cursor.execute(unlock_user_sql)
                                db.commit()
                                while True:
                                    print("\033[36;1m  用户信息中心\033[0m")
                                    print("\033[37;1m1 用户信息管理   \033[0m")
                                    print("\033[37;1m9 退出信用卡中心\033[0m")
                                    v = input("请输入您的选择:")
                                    if v == '1':
                                        while True:
                                            print(" \033[46;1m用户信息中心\033[0m")
                                            print("\033[37;1m1\t查询用户信息   \033[0m")
                                            print("\033[37;1m2\t注销用户  \033[0m")
                                            print("\033[37;1m3\t修改用户密码 \033[0m")
                                            print("\033[37;1m4\t退出用户信息中心  \033[0m")
                                            c = input("请输入您的选择:")
                                            if c == '1':
                                                zh_query_info(user)
                                            elif c == '2':
                                                print("当前系统存在的用户:")
                                                query_user_sql = "select user_name from user_info where user_name not in ('%s');"% user
                                                cursor.execute(query_user_sql)
                                                db.commit()
                                                usr = []
                                                for u in cursor.fetchall():
                                                    usr.append(u[0])
                                                    print(u[0])
                                                username = input("请输入需要删除的用户名:")
                                                if username == 'q':
                                                    print("退出删除用户 ")
                                                elif username in usr:
                                                    zh_delete_user(username)
                                                else:
                                                    print("用户 %s 不存在"% username)
                                            elif c == '3':
                                                query_user_sql = "select user_name from user_info where user_name not in ('%s');" % user
                                                cursor.execute(query_user_sql)
                                                db.commit()
                                                usr = []
                                                print("当前系统用户 :")
                                                for u in cursor.fetchall():
                                                    usr.append(u[0])
                                                    print(u[0])
                                                usr_name = input("请输入需要修改的用户名:")
                                                if usr_name == 'q':
                                                    print("退出密码修改 ")
                                                elif usr_name in usr:
                                                    zh_change_password(usr_name)
                                                else:
                                                    print("用户 %s 不存在"% usr_name)
                                            elif c == '4':
                                                print("退出用户信息中心")
                                                break
                                            else:
                                                print("\033[31;1m 输入错误,请重新输入\033[0m")
                                    elif v == '9':
                                        print("\033[46;1m 用户 %s 退出\033[0m" % user)
                                        break
                                    else:
                                        print("\033[41;1m 输入错误\033[0m")
                            else:
                                print("\033[41;1m密码错误\033[0m")
                                user_status_list[0] = int(user_status_list[0]) + 1
                                update_user_status_sql = "update user_status set user_fail_count='%s',user_last_fail_time=now() " \
                                                         "where user_name='%s';" % (user_status_list[0], user)
                                cursor.execute(update_user_status_sql)
                                db.commit()
                                break
                        else:
                            print("\033[41;1m 用户 %s 被锁定\033[0m" % user)
                            lock_user_sql = "update user_status set user_status='locked'" \
                                            " where user_name='%s';" % user
                            cursor.execute(lock_user_sql)
                            db.commit()
                            break
                else:
                    print("\033[41;1m 用户 %s 被锁定\033[0m" % user)
                    unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                      " where user_name='%s';" % user
                    now_date = datetime.datetime.now()
                    t_str = user_status_list[1]
                    last_date = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
                    count = now_date - last_date
                    print("\033[41;1m 用户被锁定时间已经持续 %s 秒\033[0m" % count.seconds)
                    if count.seconds > 300:
                        cursor.execute(unlock_user_sql)
                        db.commit()
                        print("\033[36;1m用户 %s 锁定时间超过 300 秒, 自动解锁\033[0m" % user)
                    else:
                        pass
                    break
            else:
                print("\033[31;1m 用户 %s 不存在\033[0m" % user)
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
                                print("\033[36;1m 登陆成功\033[0m")
                                unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                                  " where user_name='%s';" % user
                                cursor.execute(unlock_user_sql)
                                db.commit()
                                while True:
                                    print("\033[36;1m欢迎来到信用卡中心\033[0m")
                                    print("\033[37;1m1 信用卡商城\033[0m")
                                    print("\033[37;1m2 转账\033[0m")
                                    print("\033[37;1m3 信用卡还款\033[0m")
                                    print("\033[37;1m4 信用卡账单   \033[0m")
                                    print("\033[37;1m5 用户个人信息管理中心   \033[0m")
                                    print("\033[37;1m9 退出信用卡中心\033[0m")
                                    v = input("请输入您的选择:")
                                    if v == '1':
                                        print("\033[46;1m 欢迎来到商城 \033[0m")
                                        zh_shop_mall(user)
                                    elif v == '2':
                                        print("\033[46;1m欢迎来到转账中心\033[0m")
                                        zh_transfer(user)
                                    elif v == '3':
                                        print("\033[46;1m欢迎来到还款中心\033[0m")
                                        query_credit_info_sql = "select * from credit_info where credit_user_name='%s';" % user
                                        cursor.execute(query_credit_info_sql)
                                        for r in cursor.fetchall():
                                            print("当前欠款金额为:%s" %r[5])
                                        try:
                                            num = int(input("请输入还款金额:"))
                                        except ValueError:
                                            print("\033[41;1m输入错误,请输入数字\033[0m")
                                        else:
                                            zh_repayment(user, num)
                                    elif v == '4':
                                        zh_query_bill(user)
                                    elif v == '5':
                                        while True:
                                            print(" \033[46;1m用户信息中心\033[0m")
                                            print("\033[37;1m1\t用户信息查询   \033[0m")
                                            print("\033[37;1m2\t用户信息删除  \033[0m")
                                            print("\033[37;1m3\t用户密码修改  \033[0m")
                                            print("\033[37;1m4\t退出用户信息中心  \033[0m")
                                            c = input("请输入您的选择:")
                                            if c == '1':
                                                zh_user_query_info(user)
                                            elif c == '2':
                                                print("当前登录用户是: %s" % user)
                                                d = input("删除当前登录用户?(y/n)")
                                                if d == 'y' or d == 'Y' or d == 'yes' or d == 'YES':
                                                    zh_user_delete_user(user)
                                                    print("\033[41;1m用户 %s 不存在\n 退出系统\033[0m"% user)
                                                    exit()
                                                elif d == 'n' or d == 'N' or d == 'no' or d == 'NO':
                                                    print("停止删除用户")
                                                else:
                                                    print("输入错误")
                                            elif c == '3':
                                                zh_change_password(user)

                                            elif c == '4':
                                                print("退出用户信息中心")
                                                break
                                            else:
                                                print("\033[31;1m 输入错误,请重新输入\033[0m")

                                    elif v == '9':
                                        print("\033[46;1m 用户 %s 退出\033[0m" % user)
                                        break
                                    else:
                                        print("\033[41;1m 输入错误\033[0m")
                            else:
                                print("\033[41;1m密码错误\033[0m")
                                user_status_list[0] = int(user_status_list[0]) + 1
                                update_user_status_sql = "update user_status set user_fail_count='%s',user_last_fail_time=now() " \
                                                         "where user_name='%s';" % (user_status_list[0], user)
                                cursor.execute(update_user_status_sql)
                                db.commit()
                                break
                        else:
                            print("\033[41;1m 用户 %s 被锁定\033[0m" % user)
                            lock_user_sql = "update user_status set user_status='locked'" \
                                            " where user_name='%s';" % (user)
                            cursor.execute(lock_user_sql)
                            db.commit()
                            break
                else:
                    print("\033[41;1m 用户 %s 被锁定\033[0m" % user)
                    unlock_user_sql = "update user_status set user_status='unlocked',user_fail_count='0',user_last_fail_time='None'" \
                                      " where user_name='%s';" % (user)
                    now_date = datetime.datetime.now()
                    t_str = user_status_list[1]
                    last_date = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
                    count = now_date - last_date
                    print(count.seconds)
                    print("\033[41;1m 用户锁定时间已经持续 %s 秒\033[0m" % count.seconds)
                    if count.seconds > 300:
                        cursor.execute(unlock_user_sql)
                        db.commit()
                        print("\033[36;1m用户 %s 锁定时间超过 300 秒, 自动解锁\033[0m" % user)
                    else:
                        pass
                    break
            else:
                print("\033[31;1m 用户 %s 不存在\033[0m" % user)
                break


def zh_user_query_info(user):
    user_info__sql = "select * from user_info where user_name='%s';"% user
    user_status_sql = "select * from user_status where user_name='%s';"% user
    credit_info_sql = "select * from credit_info where credit_user_name='%s';"% user
    cursor.execute(user_info__sql)
    db.commit()
    print("\033[34;1m 用户名\t登录密码 \t信用卡卡号")
    for data in cursor.fetchall():
        print(data[1], '\t', data[2], '\t', data[3])
    print(" 用户名\t用户登录失败次数\t用户上一次登录失败时间\t用户状态")
    cursor.execute(user_status_sql)
    db.commit()
    for data1 in cursor.fetchall():
        print(data1[0], '\t', data1[1], '\t', data1[2], '\t', data1[3])
    print(" 用户名\t信用卡卡号\t信用卡额度\t信用卡消费金额\t信用卡欠款金额")
    cursor.execute(credit_info_sql)
    db.commit()
    for data2 in cursor.fetchall():
        print(data2[1], '\t', data2[2], '\t', data2[3], '\t', data2[4],'\t',data2[5])
    print("\033[0m")
def zh_query_info(user):
    user_info__sql = "select * from user_info where user_name not in ('%s') ;" % user
    user_status_sql = "select * from user_status where user_name not in ('%s') ;" % user
    credit_info_sql = "select * from credit_info where credit_user_name not in ('%s') ;" % user
    cursor.execute(user_info__sql)
    db.commit()
    print("\033[34;1m 用户名\t登录密码 \t信用卡卡号")
    for data in cursor.fetchall():
        print(data[1], '\t', data[2], '\t', data[3])
    print(" 用户名\t用户登录失败次数\t用户上一次登录失败时间\t用户状态")
    cursor.execute(user_status_sql)
    db.commit()
    for data1 in cursor.fetchall():
        print(data1[0], '\t', data1[1], '\t', data1[2], '\t', data1[3])
    print(" 用户名\t信用卡卡号\t信用卡额度\t信用卡消费金额\t信用卡欠款金额")
    cursor.execute(credit_info_sql)
    db.commit()
    for data2 in cursor.fetchall():
        print(data2[1], '\t', data2[2], '\t', data2[3], '\t', data2[4],'\t',data2[5])
    print("\033[0m")

def zh_user_delete_user(usr_name):
    count_sql = "select count(*) from user_info where user_name='%s';" % usr_name
    del_user_info_sql = "delete from user_info where user_name='%s';" % usr_name
    del_user_status_sql = "delete from user_status where user_name='%s';" % usr_name
    del_credit_info_sql = "delete from credit_info where credit_user_name='%s';" % usr_name
    cursor.execute(count_sql)
    db.commit()
    for data in cursor.fetchall():
        if data[0] != 0:
            cursor.execute(del_user_info_sql)
            print("更新表 user_info 成功")
            cursor.execute(del_user_status_sql)
            print("更新表 user_status 成功")
            cursor.execute(del_credit_info_sql)
            print("更新表 credit_info 成功")
            db.commit()
            print("\033[36;1m 用户 %s 删除成功\033[0m"% usr_name)
        else:
            print("\033[31;1m 用户 %s 不存在\033[0m" % usr_name)

def zh_delete_user(usr_name):
    count_sql = "select count(*) from user_info where user_name not in ('%s');" % usr_name
    del_user_info_sql = "delete from user_info where user_name='%s';" % usr_name
    del_user_status_sql = "delete from user_status where user_name='%s';" % usr_name
    del_credit_info_sql = "delete from credit_info where credit_user_name='%s';" % usr_name
    cursor.execute(count_sql)
    db.commit()
    for data in cursor.fetchall():
        if data[0] != 0:
            cursor.execute(del_user_info_sql)
            print("更新表 user_info 成功")
            cursor.execute(del_user_status_sql)
            print("更新表 user_status 成功")
            cursor.execute(del_credit_info_sql)
            print("更新表 credit_info 成功")
            db.commit()
            print("\033[36;1m 用户 %s 删除成功\033[0m" % usr_name)
        else:
            print("\033[31;1m 用户 %s 不存在\033[0m" % usr_name)

def zh_change_password(user):
    try:
        password = int(input("请输入新密码:"))
    except ValueError:
        print("输入错误，请输入数字")
    else:
        update_password_sql = "update user_info set user_passwd='%s' where user_name='%s';" % (password, user)
        cursor.execute(update_password_sql)
        db.commit()
        print("更新用户 %s 密码成功"% user)

def zh_shop_mall(user):
    credit_list = []
    name_list = []
    price_list = []
    count_list = []
    buy_list = []
    buy_num_list = []
    cost_sum = 0
    print("\033[36;1m++++++++++++++++++产品列表++++++++++++++++++++\033[0m")
    query_sql = "select * from product_info ;"
    query_credit_info_sql = "select * from credit_info where credit_user_name='%s';" % user
    cursor.execute(query_sql)
    db.commit()
    print("\033[34;1m 产品ID\t产品子类\t产品名\t产品单价\t产品数量\033[0m")
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
        print("+++++++++++++++选项+++++++++++++++++")
        print("------1  购物---------------------")
        print("------2  停止购物并结账------")
        print("++++++++++++++++++++++++++++++++++++++")
        cho = input("请输入您的选择:")
        if cho == '1':
            product_name = input("请输入您需要购买的产品名:")
            if product_name in name_list:
                num = int(input("请输入产品 %s 的购买数量:" % product_name))
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
                        shop_desc = "产品:%s,产品数量:%s"%(product_name,num)
                        # update_product_info_sql = "update product_info set product_count='%s' where product_name='%s';" % (c, product_name)
                        # update_credit_info_sql = "update credit_info set credit_payment='%s' where credit_user_name='%s';"% (cost_sum,product_name)
                        # cursor.execute(update_product_info_sql)
                        # cursor.execute(update_credit_info_sql)
                        # db.commit()
                    else:
                        print("金额不足，当前花费:%s,信用卡额度为:%s " % (cost_sum, credit_list[3]))
                else:
                    print("输入超过最大商品数量")
            else:
                print("商品%s不存在" % product_name)
        elif cho == '2':
            print("结束购物")
            print("购物列表为:")
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
            print("输入的选项不存在")

def zh_transfer(user):
    print("当前用户列表:")
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
    print("\033[46;1m 用户 %s 当前余额为:%s\033[0m" % (user,transfer_credit_list[0]))
    transfer_to = input("请输入需要转向的用户:").strip()
    transfer_amount = input("请输入转账金额:").strip()
    transfer_description = input("请输入转账描述:").strip()
    # 使用列表存储转账接收用户信用卡余额 信用卡花费 信用卡待还金额
    transfer_to_credit_list = []
    query_transfer_to_credit_info_sql = "select * from credit_info where credit_user_name='%s';"% transfer_to
    cursor.execute(query_transfer_to_credit_info_sql)
    # 使用列表存储转账发起用户信用卡余额 信用卡花费 信用卡待还金额
    for t in cursor.fetchall():
        transfer_to_credit_list.append(t[4])
        transfer_to_credit_list.append(t[5])
        transfer_to_credit_list.append(t[6])
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
            transfer_credit_bill_trade_detail = "|转账发起用户:%s |转账接收用户 user:%s |转账金额:%s |服务费:%s" % (
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
            print("向用户 %s 转账失败"% transfer_to)

        else:
            transfer_status = "success"
            transfer_credit_bill_trade_detail = "转账发起用户:%s 转账接收用户:%s 转账金额:%s" % (
            user, transfer_to, transfer_amount)
            insert_transfer_sql = "insert into transfer (transfer_people,transfer_to,transfer_amount," \
                                  "transfer_date,transfer_status,transfer_description) values ('%s','%s','%s',now(),'%s','%s');" \
                                  "" % (user, transfer_to, transfer_amount, transfer_status, transfer_description)
            insert_transfer_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description," \
                                              "credit_bill_type,credit_bill_trade_date,credit_bill_trade_detail,credit_bill_trade_note) values " \
                                              "('%s','%s','transfer',now(),'%s','-%s');" % (
                                              user, transfer_status, transfer_credit_bill_trade_detail, transfer_amount)
            insert_transfer_to_credit_bill_sql = "insert into credit_bill (credit_bill_user_name,credit_bill_description," \
                                                 "credit_bill_type,credit_bill_trade_date,credit_bill_trade_detail,credit_bill_trade_note) values " \
                                                 "('%s','%s','transfer',now(),'%s','+%s');" % (
                                                 transfer_to, transfer_status, transfer_credit_bill_trade_detail,
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
            print("向用户%s转账成功"%transfer_to)
    else:
        print("\033[41;1m 用户 %s 不在可转账列表中\033[0m"% transfer_to)
def zh_repayment(user,num):
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
            credit_bill_trade_detail = "信用卡余额:%s,本次还款金额:%s,待偿还金额:%s" % (
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
            print("\033[36;1m 还款成功\033[0m")
            print("\033[36;1m 当前用户信息 :信用卡余额 %s|当前消费金额 %s|待还金额 %s\033[0m" % (
            credit_balance, credit_payment, credit_amount))
        else:
            print("\033[31;1m 还款失败 \033[0m")
            print("\033[31;1m还款金额超过信用卡欠款. 当前欠款为 %s 元 \033[0m" % repayment_info_list[2])
    else:
        print("\033[31;1m 还款失败 \033[0m")
        print("\033[31;1m还款金额需要大于0\033[0m")

def zh_main():
    while True:
        print("\033[34;1m 欢迎来到信用卡中心\033[0m")
        print("\033[34;1mID\tID描述\033[0m")
        print("\033[37;1m1\t用户注册          \033[0m")
        print("\033[37;1m2\t用户登录             \033[0m")
        print("\033[37;1m9\t退出\033[0m")
        try:
            value = int(input("\033[34;1m 请输入您选择的ID:\033[0m").strip())
        except ValueError:
            print("\033[31;1m 请输入int类型\033[0m")
        else:
            if value == 1:
                username = input("\033[34;1m 请输入用户名:\033[0m").strip()
                while True:
                    print("\033[34;1m 请输入用户 %s 的密码:\033[0m" % username)
                    try:
                        password0 = int(input().strip())
                    except ValueError:
                        print("\033[31;1m值必须为数字 \033[0m")
                    else:
                        print("\033[34;1m 请再次输入用户 %s 的密码:\033[0m" % username)
                        try:
                            password1 = int(input())
                        except ValueError:
                            print("\033[31;1m值必须为数字 \033[0m")
                        else:
                            if password0 == password1:
                                password = password1
                                cardid = random.randint(9999999, 99999999)
                                zh_sign_up(username, password, cardid)
                                break
                            else:
                                print("\033[31;1m两次输入的密码不一致\033[0m")
            elif value == 2:
                username = input("\033[34;1m 请输入用户名:\033[0m").strip()
                password = getpass.getpass("请输入用户密码:").strip()
                zh_login(username, password)
            elif value == 9:
                print("\033[36;1m 退出信用卡中心\033[0m")
                break
            else:
                print("\033[31;1m 输入的值不存在\033[0m")

def zh_query_bill(user):
    bill_sql = "select * from credit_bill where credit_bill_user_name='%s';" % user
    cursor.execute(bill_sql)
    user_bill_list = []
    for line in cursor.fetchall():
        print(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
