
from ServiceLayer.services import users,search,items,shops,customer
from django.urls import path

users_urlpatterns = [
    path('users/register/', users.register),
    path('users/remove_user/', users.remove_user),
    path('users/edit_profile/', users.edit_profile),

]

search_urlpatterns = [
    path('search/item/', search.search_item),
    path('search/shop/', search.search_shop),
    path('search/itemsInShop/', search.search_item_in_shop),
]

items_urlpatterns = [
    path('items/add_item/', items.add_item),
    path('items/add_item_to_shop/',items.add_item),
    path('items/remove_item_from_shop/', items.remove_item),
    path('items/add_review_on_item/', items.add_review_on_item),
]

shops_urlpatterns = [
    path('shops/create_shop/', shops.create_shop),
    path('shops/add_review_on_shop/', shops.add_review_on_shop),
]

customer_urlpatterns = [
    path('customer/get_purchase_history/', customer.get_purchase_history),
]

urlpatterns = users_urlpatterns + search_urlpatterns + items_urlpatterns + shops_urlpatterns# add more here using '+'
