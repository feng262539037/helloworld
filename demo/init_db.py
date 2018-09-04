#coding:utf-8
import os,csv
import json
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helloworld.settings")
django.setup()
import xlrd
from xlrd import xldate_as_datetime
from demo.models import *

book = xlrd.open_workbook(u'./图书信息表.xls')

table1 = book.sheet_by_name(u'作者信息')
for i in range(1, table1.nrows):
    #取整行的值，是个列表
    value = table1.row_values(i)
    #print value #如：[u'\u5218\u5927\u6d77', u'\u7537', 30.0, u'liudahai@163.com', 13812345001.0]等等
    #通过列表的索引取值
    name = value[0]
    sex = value[1]
    age = value[2]
    email = value[3]
    # phone在excel表中存的是数字，读回来也是数字（float型）
    phone = value[4]

    # 从excel表中获取的性别（男/女）
    # 在数据库中插入的性别是0或1，所以需要做转换，方便插入数据库
    if sex == u'男':
        sex = 0
    else:
        sex = 1

    # 在Author表中插入姓名，由于这个对象后面还用，所以用author接一下
    author = Author.objects.create(name = name)
    # print type(author)
    # print author

    # 在AuthorDetails中插入姓名和详情
    # 把phone从float转成int
    # 由于数据库中phone的格式是str，所以在数据库插入之前，再转str
    AuthorDetails.objects.create(sex = sex, email = email, age = age,
                                 phone = str(int(phone)), author = author)

table2 = book.sheet_by_name(u'出版社信息')
for i in range(1, table2.nrows):
    value = table2.row_values(i)
    publisher = value[0]
    address = value[1]
    city = value[2]
    website = value[3]

    Publisher.objects.create(name = publisher, address = address,
                            city = city, website = website)

table3 = book.sheet_by_name(u'图书信息')
for i in range(1, table3.nrows):
    value = table3.row_values(i)
    title = value[0]
    publication_name = value[2]
    price = value[4]

    #获取作者的值,是一个列表！！！
    author_name = value[1].split(',')

    #获取出版日期的值,转成date格式
    publication_date = xldate_as_datetime(value[3], 0)
    # print values[3]  #打印的是，比如 37834等
    # print publication_date  #打印的是，比如2017-09-16

    #为什么查询时，不能用filter？？？
    #filter查询回来的是列表！！！而不是对象
    #往book中插入出版社，是对象！！！，所以必须用get！！！

    #代码中有get，找不到会抛异常，所以用try...catch...
    try:
        #从出版社列表中找到这本书的出版社
        publisher = Publisher.objects.get(name = publication_name)
        #在书中添加，名称，出版日期，价格
        #在书中添加出版社，多对一
        book = Book.objects.create(title = title, publication_date = publication_date,
                                   price = price, publisher = publisher)
        # print type(book)
        #print book

        #循环作者列表
        for a_name in author_name:
            #从作者列表中找到这本书的作者
            author = Author.objects.get(name = a_name)
            #在书中添加作者，多对多关系（只能用add！！！！！）
            #对象.属性名.add(关联对象)！！！
            book.author.add(author)
    except Exception as e :
        print e



#循环添加4次，以下是最笨的方法

# book = xlrd.open_workbook(u'./图书信息表.xls')
#
# table = book.sheet_by_name(u'作者信息')
# for i in range(1, table.nrows):
#     value = table.row_values(i)
#     name = value[0]
#     Author.objects.create(name=name)
#
# for i in range(1, table.nrows):
#     value = table.row_values(i)
#     name = value[0]
#     sex = value[1]
#     age = value[2]
#     email = value[3]
#     phone = value[4]
#
#     if sex == u'男':
#         sex = 0
#     else:
#         sex = 1
#
#     author = Author.objects.get(name = name)
#     AuthorDetails.objects.create(age = age, email = email,
#                                  sex = sex, phone=int(phone), author = author)
#
# table2 = book.sheet_by_name(u'出版社信息')
# for i in range(1,table2.nrows):
#     value = table2.row_values(i)
#     name = value[0]
#     address = value[1]
#     city = value[2]
#     website = value[3]
#
#     Publisher.objects.create(name = name, address = address,
#                              city = city, website = website)
#
# table3 = book.sheet_by_name(u'图书信息')
# for i in range(1,table3.nrows):
#     value = table3.row_values(i)
#     title = value[0]
#     publication_name = value[2]
#     price = value[4]
#
#     author_name = value[1].split(',')
#
#     publication_date = xldate_as_datetime(value[3], 0)
#
#     publisher = Publisher.objects.get(name = publication_name)
#     book = Book.objects.create(title = title,price = price,publication_date = publication_date,
#                         publisher = publisher)
#
#     try:
#         for a_name in author_name:
#             author = Author.objects.get(name = a_name)
#             book.author.add(author)
#     except Exception as e:
#         print e


# dic = {'name':'张三'}

#print dic  #{'name': '\xe5\xbc\xa0\xe4\xb8\x89'}

#默认使用ASCII编码
#print json.dumps(dic)  #{"name": "\u5f20\u4e09"}

#我把字典转成json时，可以指定编码格式
#print json.dumps(dic, ensure_ascii=False)  #{"name": "张三"}


#file_name = './data.csv'
#with open(file_name) as f:
#    data = csv.reader(f)
#    print list(data)  #[['zhangsan', '12345'], ['tianlaoshi', '123'], ['lisi', '1234']]


# data = {
#         "business_autoFans_J":[{"2016_08":14},  {"2016_09":15}, {"2016_10":9}],
#         "autoAX":[{"2016_08":7},  {"2016_09":32}, {"2016_10":0}],
#         "autoAX_admin":[{"2016_08":5},  {"2016_09":13}, {"2016_10":2}],
#         }
# sum = 0
# for v in data.values():
#     for i in v:
#         if i.has_key('2016_09'):
#             sum = sum + i.get('2016_09')
# print sum