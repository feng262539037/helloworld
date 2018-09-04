#coding:utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
import csv, os
import json
from django.contrib import auth
from models import *
# Create your views here.

def home(request):
    #增加，2种方法
    #方式一
    #Author(name = '李清照').save()
    #方式二
    #Author.objects.create(name = '李白')

    #插入作者详情
    #author = Author.objects.get(name='李白')
    #AuthorDetails.objects.create(age=18, sex=0, email='xxx@163.com',
    #                             phone='13800000000', author=author)

    #查询（3种方法）
    #方法一：get
    #author = Author.objects.get(name='李商隐')
    #print type(author)  #<class 'demo.models.Author'>

    #方法二
    #查询李白：fliter
    #author = Author.objects.filter(name='李白')
    #print type(author)  #<class 'django.db.models.query.QuerySet'>
    #for a in author:
    #    print a  #打印出数据库中所有的李白，下面的也可以
    #    print a.name  #打印出数据库中所有的李白，上面的也可以

    #查询所有姓李的：filter
    #author = Author.objects.filter(name__startswith='李')
    #for a in author:
    #    print a
    #   print a.name

    #查询所有：all
    #author = Author.objects.all()
    #for a in author:
    #    print a.name

    #删除：先查找，再删除
    #author = Author.objects.filter(name = '李白').delete()

    #改：先查找，再修改
    #author = Author.objects.filter(name='李白')
    #author.update(name = '李黑')
    #return HttpResponse('1')

    #获取cookies
    # username = request.COOKIES.get('username')
    # password = request.COOKIES.get('password')

    #获取session
    username = request.session.get('username')
    password = request.session.get('password')

    if username and password:
        info = u'欢迎登录：%s' % username
        return HttpResponse(content=info)
        #return render(request, 'home.html', {'username': username})
    else:
        #
        #return render_to_response('login.html')
        return HttpResponseRedirect('/demo/login')

def login(request):
    return render(request, 'login.html')

def api_login(request):
    http_response = HttpResponse()
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        issave = request.POST.get('isSave')
        if username and password:
            #username的长度大于5，才有效
            if len(username) > 5:
                #判断用户名和密码是否是django的后台管理用户
                #如果有，返回一个对象，如果没有，返回空对象
                #user = auth.authenticate(username = username, password = password)
                #print user  #zhangsan
                #print type(user)  #<class 'django.contrib.auth.models.User'>

                #读取文件
                # user = search_user(username, password)

                #方式一：用filter查询：返回一个列表
                # user = User.objects.filter(name = username,pwd = password)
                #判断列表的长度要大于0
                # if len(user) > 0:

                #方式二：filter里提供一个方法：返回布尔值
                #if User.objects.filter(name = username,pwd = password).exists():

                #方式三：用get查询
                #但是get查询不到会抛异常，所以用try...except...
                try:
                    user = User.objects.get(name=username, pwd=password)
                except:
                    user = None
                if user:
                    #如果设置了保存登陆信息（保存cookies信息）
                    if issave:
                        # 利用cookies
                        # http_response.set_cookie('username', username, max_age=10)
                        # http_response.set_signed_cookie('password', password, salt='123', max_age=10)

                        #利用session
                        request.session['username'] = username
                        request.session['password'] = password
                        #设置session的过期时间
                        request.session.set_expiry(10)
                        info = u'欢迎登录：%s' % username
                    else:
                        info = u'欢迎登录：%s' % username
                else:
                    info = u'用户名/密码错误'
            else:
                info = u'您输入的用户名小于5位，请重新输入'
        else:
            #利用HttpResponse的属性
            http_response.content = u'用户名和密码是必填参数，请输入'
            http_response.status_code = 400
            return http_response
            #利用HttpResponse的构造函数
            #return HttpResponse(content=u'用户名和密码是必填参数，请输入',status=400)
    else:
        info = u'请求类型错误,不是POST请求'
    http_response.content = info
    return http_response

def sign(request):
    return render(request, 'sign.html')

def api_sign(request):
    result = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = User.objects.filter(name=username)
            if not user.exists():
                try:
                    User.objects.create(name=username, pwd=password)
                    return HttpResponseRedirect('/demo/login/')
                except:
                    info = u'未知错误'
            else:
                info = u'用户名已存在'
        else:
            info = u'用户名/密码是必填项，请重新输入'
    else:
        info = u'请求类型错误,不是POST请求'

    result = {"info": info}
    return HttpResponse(content=json.dumps(result, ensure_ascii=False), content_type='application/json')

def search_user(username,password):
    flag = False
    file_name = './data.csv'
    #如果读取文件的路径写错，下面这段代码会发生异常
    #所以可以用try
    #如果文件错了，也会报用户名密码错误，并且在控制台，有错误信息
    try:
        with open(file_name) as f:
            data = csv.reader(f)
            #print list(data) #[['zhangsan', '12345'], ['tianlaoshi', '123'], ['wangwu', '125']]
            for d in list(data):
                if d[0] == username and d[1] == password:
                        flag = True
    except Exception as e:
        print e.message
    return flag

def bugs(request):
    #GET请求
    #if request.method == 'GET':
        #month = request.GET.get('month')
    #POST请求：form表单格式或urlencoded格式
    #if request.method == 'POST':
        #month = request.POST.get('month')
    #POST请求：raw/json格式
    if request.method == 'POST':
        #month = request.body
        #print month #{"month": 9}
        #print type(month) #str
        body = request.body
        dic = json.loads(body)
        month = dic.get('month')
        #print month #9
        #print type(month) #int
        if month:
            try:
                #字符串转int类型
                #如果输入的是09，自动转成9
                month = int(month)
                if month in range(1, 10):
                    month = '2016_0' + str(month)
                    sum = search_by_month(month)
                    dic = {'month': month, 'total': sum}
                    # status = 必须是3位数，否则报错！
                    return HttpResponse(status=200, content=json.dumps(dic, ensure_ascii=False), content_type='application/json')
                elif month in range(10, 13):
                    month = '2016_' + str(month)
                    sum = search_by_month(month)
                    dic = {'month': month, 'total': sum}
                    #方式一：返回JsonResponse(dic)
                    return JsonResponse(dic)
                    #方式二：返回JsonResponse(data=dic)
                    #return JsonResponse(data=dic)
                else:
                    info = u'您输入的月份，不在1~12范围内，请重新输入'
                    code = 1
            except:
                info = u'您输入的月份不是数字'
                code = 2
        else:
            info = u'月份是必填参数，请您输入'
            code = 3
    else:
        info = u'请求类型错误，不是GET请求'
        code = 4
    data = {"info": info, "code": code}
    return HttpResponse(content=json.dumps(data, ensure_ascii=False), content_type='application/json')

def search_by_month(month):
    sum = 0
    data = {
        "business_autoFans_J": [{"2016_08": 14}, {"2016_09": 15}, {"2016_10": 9}],
        "autoAX": [{"2016_08": 7}, {"2016_09": 32}, {"2016_10": 0}],
        "autoAX_admin": [{"2016_08": 5}, {"2016_09": 13}, {"2016_10": 2}],
    }
    for v in data.values():
        for d in v:
            if d.has_key(month):
                sum = sum + d.get(month)
    return sum

#POST请求，格式是json字符串
def weather(request):
    result = {}
    if request.method == 'POST':
        body = request.body
        #先校验json的格式正确
        #如果json格式正确，就可以把json转成字典，所以用json.loads(body)
        try:
            dic = json.loads(body)
        except:
            error_code = 10003
        #然后校验必填参数
        else:
            theCityCode = dic.get('theCityCode')
            if theCityCode:
                if theCityCode == 1:
                    error_code = 0
                    result["cid"] = "1"
                    result["name"] = u"北京市"
                    result["weather"] = u"今日天气实况：气温：19℃;风向 / 风力: 东北风"
                else:
                    error_code = 10002
            else:
                error_code = 10001
    else:
        error_code = 10004
    result['error_code'] = error_code
    return JsonResponse(result)

def error(request):
    return render(request, 'error.html', {'username': '456'})

# def index(request):
#     if request.method == 'GET':
#         username = request.GET.get('username')
#         password = request.GET.get('password')
#         if username and password:
#             info = u'欢迎登录:%s' % username
#         else:
#             info = u'用户名/密码为空'
#             return HttpResponse(status=400, content=json.dumps({"info": info}, ensure_ascii=False), content_type='application/json')
#     else:
#         info = u'请求类型错误'
#     data = {"info": info}
#     return HttpResponse(content=json.dumps(data, ensure_ascii=False),content_type='application/json')
