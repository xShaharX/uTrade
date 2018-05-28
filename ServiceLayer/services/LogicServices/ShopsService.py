from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import ItemsLogic
from DomainLayer import ShopLogic
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.Shop import Shop
from SharedClasses.ShopReview import ShopReview


@csrf_exempt
def create_shop(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        shop_name = request.POST.get('name')
        shop_status = request.POST.get('status')

        login = request.COOKIES.get('login_hash')
        if login is None:
            return HttpResponse('FAILED: You are not logged in')
        username = Consumer.loggedInUsers.get(login)
        if username is None:
            return HttpResponse('FAILED: You are not logged in')

        shop = Shop(shop_name, shop_status)
        return HttpResponse(ShopLogic.create_shop(shop, username))


@csrf_exempt
def remove_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        item_id = request.POST.get('item_id')
        username = request.POST.get('username')
        ItemsLogic.remove_item_from_shop(item_id, username)


@csrf_exempt
def add_review_on_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        description = request.POST.get('description')
        rank = int(request.POST.get('rank'))

        login = request.COOKIES.get('login_hash')
        if login is not None:
            writer_id = Consumer.loggedInUsers.get(login)
            shop_review = ShopReview(writer_id, description, rank, shop_name)

            if ShopLogic.add_review_on_shop(shop_review):
                return HttpResponse('success')
        return HttpResponse('fail')


def search_shop_purchase_history(request):
    if request.method == 'GET':
        return HttpResponse('no GUI yet')


@csrf_exempt
def close_shop_permanently(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if ShopLogic.close_shop_permanently(username, shop_name):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def shop_page(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
