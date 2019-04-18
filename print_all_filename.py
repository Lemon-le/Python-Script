import os,json

#Function：将一个目录下的所有文件名打印
#Author  ：李先生
#Date    ：20190418
#Version ：V1.0



#指定需要遍历的目录
path='D:/app'

#将遍历到的文件名存放于此列表中
file_name_list=[]

def __print__file():
    for file_name in os.listdir(path):
        if os.path.isdir(file_name):
            __print__file(file_name)
        else:
            file_name_list.append(file_name)

    #遍历列表，打印文件名
    for file in file_name_list:
        print(file)

def main():
    __print__file()

if __name__ == '__main__':
    main()