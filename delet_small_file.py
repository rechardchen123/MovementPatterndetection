# !/usr/bin/env python3
# -*- coding: utf-8 -*
import os

directory = ''
os.chdir(directory)
cwd = os.getcwd()
print('current working directory:' +cwd )

def deleteBySize(minSize):
    '''
    :param minSize:
    :return:
    '''
    files = os.listdir(os.getcwd())
    for file in files:
        if os.path.getsize(file) < minSize * 1024:
            os.remove(file)
            print(file + "was deleted.")
    return

def deleteNullFile():
    '''
    :return:
    '''
    files = os.listdir(os.getcwd())
    for file in files:
        if os.path.getsize(file) == 1:
            os.remove(file)
            print(file + " was deleted.")
    return

hint = '''funtion : 
        1    delete null file
        2    delete by size
        q    quit\n
please input number: '''

while True:
    option = input(hint)
    if option == '1':
        deleteNullFile()
    elif option == '2':
        minSize = int(input("minSize(k):"))  # 键盘输入的是字符串，需要强制转换成int类型
        deleteBySize(minSize)
    elif option == 'q':
        print("quit !")
        break
    else:
        print("disabled input. please try again...")