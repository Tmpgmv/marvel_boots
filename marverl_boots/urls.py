"""
URL configuration for Marverl boots project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from django.contrib.auth.decorators import login_required

from django.urls import path, include
from django.conf import settings  # PREP
from django.conf.urls.static import static  # PREP

from home.views import HomeView
from orders.views import CartItemCreateView, CartDetailView
from products.views import ProductDetailView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    
    path("", login_required(HomeView.as_view()), name="home"),
    
    path("admin/", admin.site.urls),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("cart/", CartDetailView.as_view(), name="cart"),
    path("cart-item-create/", CartItemCreateView.as_view(), name="cart-item-create"),
]

urlpatterns += i18n_patterns(

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
