from django.conf.urls import url
from .views import (
    index,
    login, signup,
    order
)


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^(?P<partner_id>\d+)/$', order, name='order'),
    ]
