from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from bookstore.models import Book


def index(request):
    if request.GET.keys():  # 显示所有key
        order_by = request.GET.get('order_by', 'mark_price')
        z = request.GET.get('z', '1')
        if z == '1':
            # 升序
            new_order_by = order_by
        else:
            # 降序
            new_order_by = '-' + order_by
        all_book = Book.objects.filter(isActive=True).order_by(new_order_by)
    else:
        all_book = Book.objects.filter(isActive=True)
    return render(request, 'index.html', locals())

def add(request):
    if request.method == 'GET':
        return render(request,'add.html')
    if request.method == 'POST':
        title = request.POST.get('title')
        pub = request.POST.get('pub')
        price = request.POST.get('price')
        m_price = request.POST.get('m_price')
        try:
            Book.objects.create(title=title,pub = pub,price=price,mark_price = m_price)
        except Exception as e:
            print(e)
            error = '请检查提交数据'
        return render(request,'add.html',locals())
    return HttpResponse('sorry! You can not come in ')

def details(request,book_id):
    book_id = int(book_id)
    if request.method == 'GET':
        try:
            book = Book.objects.get(id=book_id)
        except Exception as e:
            print('------------detail error-----------------')
            print(e)
            return HttpResponse('sorry,book is not existed')
        return render(request, 'details.html', locals())
    if request.method == 'POST':
        books = Book.objects.filter(id=book_id)
        if not books:
            return HttpResponse('---sorry this book is not exist!!')
        book = books[0]
        # 2 改
        price = request.POST.get('price')
        m_price = request.POST.get('mark_price')

        if not price:
            return HttpResponse('---sorry this book.price is not exist!!')
        if not m_price:
            return HttpResponse('---sorry this book.m_price is not exist!!')
        to_update = False
        price = float(price)
        m_price = float(m_price)

        if book.price != price or book.mark_price != m_price:
            to_update = True

        # 3 更新
        if to_update:
            book.price = price
            book.mark_price = m_price
            # 保存
            book.save()
        return HttpResponseRedirect('/book/index')


# def delete(request,book_id):
#     # id = int(book_id)
#     books = Book.objects.filter(id=book_id,isActive=True)
#     if not books:
#         return HttpResponseRedirect('/book/index')
#     # 伪删除
#     book=books[0]
#     book.isActive = False
#     book.save()
#     return HttpResponseRedirect('/book/index')


def test_count(request):
    # 测试分组聚合
    #导入
    from django.db.models import Count
    # 要聚合的列以及对相应的数据   用values准备好
    pub_set = Book.objects.values('pub')
    # 根据上一步返回值在进行聚合

    result = pub_set.annotate(myCount = Count('pub'))
    print(result)

    # 返回值为QuerySet  [注意注意,分组聚合返回为QuerySet]
    for res in result:
        print('出版社:',res['pub'],'图书:',res['myCount'])
    return HttpResponse('----聚合成功,查看终端信息-----------')
