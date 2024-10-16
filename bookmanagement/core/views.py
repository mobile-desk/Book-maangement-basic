from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate

from django.contrib.auth import views as auth_views
from .forms import UserRegisterForm, BookForm, UserLoginForm
from .models import Book, Transaction
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm


# Create your views here.



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')

            
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})






def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=user_id, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in.')
                return redirect('book_list')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})




class LogoutView(auth_views.LogoutView):
    next_page = 'book_list'




def book_list(request):
    books = Book.objects.all()
    return render(request, 'core/book_list.html', {'books': books})




def rent_book(request, book_id):
    book = Book.objects.get(id=book_id)
    due_date = timezone.now() + timedelta(days=3)
    Transaction.objects.create(user=request.user, book=book, due_date=due_date)
    book.is_available = False
    book.save()
    return redirect('book_list')





def return_book(request, transaction_id):
    rental = Transaction.objects.get(id=transaction_id)
    rental.returning_date = timezone.now()
    # Calculate penalty
    rental.calculate_penalty()
    rental.save()

    rental.book.is_available = True
    rental.book.save()
    
    return redirect('my_rentals')


def my_rentals(request):
    rentals = Transaction.objects.filter(user=request.user)
    return render(request, 'core/my_rentals.html', {'rentals': rentals})






