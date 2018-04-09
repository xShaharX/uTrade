
from ServiceLayer.services import users,search,items
from django.urls import path

users_urlpatterns = [
    path('users/add_user/', users.add_user),
    path('users/remove_user/', users.remove_user),
    path('users/edit_user/', users.edit_user),

]

search_urlpatterns = [
    path('search/item/', search.search_item)
]

items_urlpatterns = [
    path('items/add_item_to_shop',items.add_item),
    path('items/remove_item_from_shop', items.remove_item),
]

urlpatterns = users_urlpatterns + search_urlpatterns + items_urlpatterns# add more here using '+'
