from django.db import models
from django.contrib.auth. models import User
from django.utils import timezone



# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.title
    
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returning_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    penalty_days = models.PositiveIntegerField(default=0)
    penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    
    # comare returned date to the expected retun date
    def is_late(self):
        if self.returning_date:
            return self.returning_date > self.due_date + timezone.timedelta(hours=3)
        return False
    
    
    # late fees
    def calculate_penalty(self):
        if self.returning_date:
            if self.is_late():
                late_days = (self.returning_date.date() - self.due_date.date()).days
                if late_days > 0:
                    self.penalty_days = late_days
                    self.penalty = late_days * 10
                    
                else:
                    self.penalty_days = 0
                    self.penalty = 0.0
    
    