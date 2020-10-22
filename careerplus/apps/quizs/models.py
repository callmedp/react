from django.db import models
from order.models import OrderItem
# Create your models here.


class QuizResponse(models.Model):
    """QuizResponse Sent with Linked In"""
    oi = models.OneToOneField(OrderItem, default=None, null=True,on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    question1 = models.CharField(max_length=500, blank=True, verbose_name=('Question1'))
    anser1 = models.CharField(max_length=500, verbose_name='Answer1', blank=True)
    question2 = models.CharField(max_length=500, blank=True, verbose_name=('Question2'))
    anser2 = models.CharField(max_length=500, verbose_name='Answer2', blank=True)
    question3 = models.CharField(max_length=500, blank=True, verbose_name=('Question3'))
    anser3 = models.CharField(max_length=500, verbose_name='Answer3', blank=True)
    question4 = models.CharField(max_length=500, blank=True, verbose_name=('Question4'))
    anser4 = models.CharField(max_length=500, verbose_name='Answer4', blank=True)
    question5 = models.CharField(max_length=500, blank=True, verbose_name=('Question5'))
    anser5 = models.CharField(max_length=500, verbose_name='Answer5', blank=True)

    def __str__(self):
        return '{}'.format(str(self.oi))