from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=10)
    name = models.CharField(max_length=255, unique=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(25)])


class Order(models.Model):
    order_number = models.CharField(max_length=15, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            last_order_number = int(last_order.order_number[3:]) if last_order else 0
            self.order_number = f"ORD{str(last_order_number + 1).zfill(5)}"
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# username = models.CharField(_('username'), max_length=30, unique=True,
#     help_text=_('Required. 30 characters or fewer. Letters, numbers and '
#                 '@/./+/-/_ characters'),
#     validators=[
#         validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
#     ])