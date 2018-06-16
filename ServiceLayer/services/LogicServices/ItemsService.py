import datetime
import random
import threading
from datetime import datetime
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import ItemsLogic, UsersLogic, ShopLogic, LotteryLogic
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.Item import Item
from SharedClasses.ItemReview import ItemReview


@csrf_exempt
def add_item_to_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        item_name = request.POST.get('item_name')
        item_quantity = int(request.POST.get('item_quantity'))
        item_category = request.POST.get('item_category')
        item_keywords = request.POST.get('item_keywords')
        item_price = float(request.POST.get('item_price'))
        item_url = request.POST.get('item_url')
        item_kind = request.POST.get('item_kind')
        if shop_name is None or ShopLogic.search_shop(shop_name) is False:
            return HttpResponse('invalid shop')

        if item_name is None or item_name == '':
            return HttpResponse('invalid item name')

        if item_quantity < 0:
            return HttpResponse('invalid quantity')

        if item_category is None or item_category == '':
            return HttpResponse('invalid category')

        if item_keywords is None:
            return HttpResponse('invalid keywords')

        if item_price <= 0:
            return HttpResponse('invalid price')

        if item_url == '':
            item_url = None

        sale_date = None
        sale_hour = None
        sale_minutes = None
        if item_kind == 'prize':
            sale_date = request.POST.get('sale_date')
            sale_hour = request.POST.get('sale_hour')
            sale_minutes = request.POST.get('sale_minutes')

        login = request.COOKIES.get('login_hash')
        if login is None:
            login = request.POST.get('login_hash')
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('user not logged in')
        if not UsersLogic.is_owner_of_shop(username, shop_name):
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.permission_add_item is not 1:  # no permission
                    return HttpResponse('no permission to add item')
            else:
                return HttpResponse('not owner or manager in this shop')  # not manager not owner

        status = False
        if item_kind == 'regular':
            regular_item = Item(None, shop_name, item_name, item_category, item_keywords,
                                item_price, item_quantity, item_kind, item_url, 0, 0, 0)
            status = ItemsLogic.add_item_to_shop(regular_item, username)
        elif item_kind == 'prize':
            prize = Item(None, shop_name, item_name, item_category, item_keywords,
                         item_price, 1, item_kind, item_url, 0, 0, 0)
            ticket = Item(None, shop_name, 'Ticket for ' + item_name, item_category, item_keywords,
                          item_price, item_quantity, 'ticket', item_url, 0, 0, 0)
            status = LotteryLogic.add_lottery_and_items_and_return_id(prize, ticket, ticket.price,
                                                                      sale_date + ' ' + sale_hour + ':' + sale_minutes,
                                                                      username)
        if status is False:
            return HttpResponse('could not add item')
        if item_kind == 'prize':
            LotteryLogic.start_lottery(status, sale_date, sale_hour, sale_minutes)
        return HttpResponse('success')


@csrf_exempt
def remove_item_from_shop(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('fail')

        item_id = request.POST.get('item_id')

        item = ItemsLogic.get_item(item_id)
        if item is False:
            return HttpResponse('fail')
        if not UsersLogic.is_owner_of_shop(username, item.shop_name):
            if UsersLogic.is_manager_of_shop(username, item.shop_name):
                manager = UsersLogic.get_manager(username, item.shop_name)
                if manager.permission_remove_item is not 1:  # no permission
                    return HttpResponse('no permission to remove item')
            else:
                return HttpResponse('fail')  # not manager not owner

        status = ItemsLogic.remove_item_from_shop(item_id, username)
        if status is False:
            return HttpResponse('fail')
        return HttpResponse('success')


@csrf_exempt
def add_review_on_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        description = request.POST.get('description')
        rank = request.POST.get('rank')

        login = request.COOKIES.get('login_hash')
        if login is not None:
            writer_name = Consumer.loggedInUsers.get(login)
            review = ItemReview(writer_name, item_id, description, rank)

            if ItemsLogic.add_review_on_item(review):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def edit_shop_item(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('fail')
        item_id = request.POST.get('item_id')

        item = ItemsLogic.get_item(item_id)
        if item is False:
            return HttpResponse('fail')
        if not UsersLogic.is_owner_of_shop(username, item.shop_name):
            if UsersLogic.is_manager_of_shop(username, item.shop_name):
                manager = UsersLogic.get_manager(username, item.shop_name)
                if manager.permission_edit_item is not 1:  # no permission
                    return HttpResponse('no permission to edit item')
            else:
                return HttpResponse('fail')  # not manager not owner

        fields = ['quantity', 'category', 'keywords', 'price', 'url']
        new_values = [request.POST.get('item_quantity'),
                      request.POST.get('item_category'),
                      request.POST.get('item_keywords'),
                      request.POST.get('item_price'),
                      request.POST.get('item_url')]
        for i in range(0, len(fields)):
            status = ItemsLogic.edit_shop_item(username, item_id, fields[i], new_values[i])
            if status is False:
                return HttpResponse('fail')
        return HttpResponse('success')


def get_all_purchased_items(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        return ItemsLogic.get_all_purchased_items(username)


def get_id_by_name(request):
    if request.method == 'GET':
        item_name = request.GET.get('item_name')

        id = ItemsLogic.get_id_by_name(item_name)
        print(id)
        return HttpResponse(str(id))
