from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Partner(models.Model):
    KOREAN = 'kr'
    CHINESE = 'ch'
    JAPANESE = 'jp'
    CATEGORY_CHOICES = (
        (KOREAN, '한식'),
        (CHINESE, '중식'),
        (JAPANESE, '일식'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    name = models.CharField(
        max_length=50,
        verbose_name="업체 이름",
    )
    contact = models.CharField(
        max_length=50,
        verbose_name="연락처",
    )
    address = models.CharField(
        max_length=200,
        verbose_name="주소",
    )
    description = models.TextField(
        verbose_name="상세 소개",
    )
    category = models.CharField(
    max_length = 2,
    choices = CATEGORY_CHOICES,
    default = KOREAN,
    )
    def __str__(self):
        return self.name


class Menu(models.Model):
    partner =  models.ForeignKey(
        Partner,
        on_delete = models.CASCADE,
    )
    image = models.ImageField(
        verbose_name="메뉴 이미지",
    )
    name = models.CharField(
        max_length = 50,
        verbose_name="메뉴명",
        )
    price = models.PositiveIntegerField(
        verbose_name="가격",
        )
    def __str__(self):
        return self.name
