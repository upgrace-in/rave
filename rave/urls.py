"""rave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from rave import settings
from rave_app import views
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name="index"),
    re_path(r'nft/(?P<id>[\w-]+)/$', views.view_nft, name='view_nft'),
    path('create_nft/', views.create_nft, name='create_nft'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('login/', TemplateView.as_view(template_name="login.html"), name='login'),
    path('register/', TemplateView.as_view(template_name="register.html"), name='register'),
    path('user/', views.user_func, name='user'),
    path('logout/', views.logout_view, name='logout'),

    path('admin_panel/', views.admin_panel, name='admin_panel'),
    re_path(r'nft_status/(?P<id>[\w-]+)/$', views.nft_status, name='nft_status'),

    #APIs:
    re_path(r'update_txhash/(?P<id>[\w-]+)/$', views.update_txhash, name='update_txhash'),
    re_path(r'verify_price/(?P<id>[\w-]+)/$', views.verify_price, name='verify_price'),
    

    re_path(r'purchased/(?P<id>[\w-]+)/$', views.purchased, name='purchased'),
    path('applied_for_purchasing/', views.applied_for_purchasing, name='applied_for_purchasing'),

    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
