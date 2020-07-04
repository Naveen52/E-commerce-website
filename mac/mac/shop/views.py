from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from.models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

def index(request):
    # products = Product.objects.all()
    # print(products)

    allprods=[]
    cate = Product.objects.values('category')
    cats = {item['category'] for item in cate}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n= len(prod)
        nSlides = n // 4 + ceil(n / 4 - n // 4)
        allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods':allprods}
    return render(request, 'shop/index.html', params)

def searchmatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allprods = []
    cate = Product.objects.values('category')
    cats = {item['category'] for item in cate}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil(n / 4 - n // 4)
        if len(prod) != 0:
            allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods': allprods, 'msg': ''}
    if len(allprods) == 0 or len(query)<2:
        params = {'msg': "Please enter a valid search query"}
    return render(request, 'shop/search.html', params)


def aboutus(request):
    return render(request, 'shop/about.html')


def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        query = request.POST.get('query', '')
        contact = Contact(name=name, email=email, phone=phone, query=query)
        contact.save()
    return render(request, 'shop/contact.html')




def tracker(request):
    if request.method  == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                    return HttpResponse(response)
            else:
                pass
        except Exception as e:
            pass

    return render(request, 'shop/tracker.html')
    

def productview(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/productview.html', {'product': product[0]})

def checkout(request):
    if request.method == 'POST':
        items_Json = request.POST.get('items_Json', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code= request.POST.get('zip_code', '')
        order = Order(items_Json=items_Json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code)
        order.save()
        update= OrderUpdate(order_id= order.order_id ,update_desc = "Your order has been placed" )
        update.save()
        id = order.order_id
        thank = True
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id} )
    return render(request, 'shop/checkout.html')