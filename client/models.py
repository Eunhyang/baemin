from django.db import models
from django.contrib.auth.models import User
from partner.models import Menu
# Create your models here.
class  Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    username = models.CharField(
            max_length=50,
            verbose_name="고객 이름",
        )

    def __str__(self):
        return self.username

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(
        max_length = 100,
        verbose_name = "주소",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(
        Menu,
        through = 'Ordertime',
        through_fields = ('order', 'menu'),
    )

    def __str__(self):
        return "고객 :{} 주소:{}".format(self.client.username, self.address)

class Ordertime(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField()

    def __str__(self):
        return "메뉴 :{} 수량:{}".format(self.menu.name, self.count)
