# -*- coding:utf-8 -*-
from en_main import *
from zh_main import *
print("+++++++++++++")
print("+++1 en++++++")
print("+++2 zh++++++")
print("+++++++++++++")
choice = input("please input choice:")
if choice == '1':
    en_main()
elif choice == '2':
    zh_main()
else:
    print("input not exist:")
