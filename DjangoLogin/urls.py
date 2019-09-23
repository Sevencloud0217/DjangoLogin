"""DjangoLogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from LoginUser import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register),
    path('login/',views.login),
    path('index/',views.index),
    path('forgot/',views.forgot),
    path('base/',views.base),
    path('add_goods/',views.add_goods),
    path('goods_list/',views.goods_list),
    re_path('goods_list/(?P<status>[01])/(?P<page>\d+)',views.goods_list),
    re_path('goods_status/(?P<status>\w+)/(?P<id>\d+)',views.goods_status),
]

router = routers.DefaultRouter()
router.register("goods",views.GoodsViewSet)

urlpatterns += [
    re_path('goods_list_api/(?P<status>[01])/(?P<page>\d)',views.goods_list_api),
    path('api/',views.api),
    path('vuedemo/',views.vuedemo),
    # path('goodxiews/',views.GoodView.as_view),
    path('goodviews/',csrf_exempt(views.GoodView.as_view())),
    re_path('API/',include(router.urls)),
    path('personal_info/',views.personal_info),

]
