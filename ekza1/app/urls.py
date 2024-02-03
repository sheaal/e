from django.urls import path, include
from .views import index, register, profile, ProductDetailView, product, search
from .views import BBLoginView
from .views import BBLogoutView
from .views import RegisterDoneView, RegisterUserView

app_name = 'app'


urlpatterns = [
   path('', index, name='index'),
   path('login/', BBLoginView.as_view(), name='login'),
   path('logout/', BBLogoutView.as_view(), name='logout'),
   path('register/done/', RegisterDoneView.as_view(), name='register_done'),
   path('accounts/profile/', profile, name='profile'),
   path('product/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
   path('product/', product, name='product'),
   path('register/', register, name='register'),
   path('search/', search, name='search'),
   # path('order/<int:product_id>/', ordering, name='ordering'),
]




