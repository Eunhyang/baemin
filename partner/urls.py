from django.conf.urls import url
from .views import (
    index,
    edit_info,
    menu, menu_add, menu_detail, menu_edit, menu_delete,
    signup, login, logout,
    order
)
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^edit/$', edit_info, name='edit_info'),
    url(r'^menu/$', menu, name='menu'),
    url(r'^menu/add/$', menu_add, name='menu_add'),
    url(r'^menu/(?P<menu_id>\d+)/$', menu_detail, name='menu_detail'),
    url(r'^menu/(?P<menu_id>\d+)/edit/$', menu_edit, name='menu_edit'),
    url(r'^menu/(?P<menu_id>\d+)/delete/$', menu_delete, name='menu_delete'),
    url(r'^order/$', order, name='order'),
]
