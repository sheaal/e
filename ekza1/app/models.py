from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.dispatch import Signal

def get_name_file(instance, filename):
    return 'ekza1/file'.join([get_random_string(5) + '_' + filename])

class AdvUser(AbstractUser):

    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False)
    sur_name = models.CharField(max_length=200, blank=False, verbose_name='Фамилия')
    n_name = models.CharField(max_length=200, blank=False, verbose_name='Имя')
    pat_mic = models.CharField(max_length=200, blank=False, verbose_name='Отчество')
    ava = models.ImageField(upload_to=get_name_file, verbose_name='Аватар', blank=False, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])


    class Meta:
        ordering = ['username', 'sur_name', 'n_name', 'pat_mic', 'ava']

    USERNAME_FIELD = 'username'

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    def is_author(self, bb):
        if self.pk == bb.author.pk:
            return True
        return False

   # def clean(self):
   #     if not self.send_messages:
   #         raise ValidationError('Подтвердите согласие на обработку персональных данных')

    def __str__(self):
        return self.username

user_registrated = Signal()

class Product(models.Model):
    pr_name = models.CharField(max_length=200, verbose_name='Название услуги/товара')
    pr_date = models.DateTimeField('date published')
    description_pr = models.CharField(max_length=200, verbose_name='Описание')
    pr_img = models.ImageField(verbose_name='Изображение', upload_to=get_name_file, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    user = models.ForeignKey('AdvUser', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.pr_name

class Order(models.Model):
    user = models.ForeignKey('AdvUser', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.pr_name}"