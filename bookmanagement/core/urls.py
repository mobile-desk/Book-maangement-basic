from django.urls import path
from .views import register, user_login, LogoutView, book_list, rent_book, return_book, my_rentals


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    
    path('', book_list, name='book_list'),
    path('rent/<int:book_id>/', rent_book, name='rent_book'),
    path('return/<int:transaction_id>/', return_book, name='return_book'),
    path('my-rentals', my_rentals, name='my_rentals'),
    
]
