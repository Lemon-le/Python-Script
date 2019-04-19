import os,json

#Function：将一个目录下的所有文件内容汇总到一个文件
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0


#指定文件所在的目录
path='D:/app'
#指定文件内容汇总到一个文件的文件
file_path='D:/b.txt'

#将一个目录下的所有文件内容输出到一个文件
def print_all_to_one_file():
    for file_name in os.listdir(path):
        merge_file = open(file_path,'ab+')
        content = open(path+"/"+file_name,'r',encoding='UTF-8').read()
        #文件内容编码转换
        content = content.encode()
        merge_file.write(content)
        merge_file.close()

def main():
    print_all_to_one_file()

if __name__ == '__main__':
    main()