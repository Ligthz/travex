from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


# <!-- User related -->
class MyAccountManager(BaseUserManager):
    def create_user(self, username, password, name):
        if not username:
            raise ValueError["Users must have a username"]
        if not password:
            raise ValueError["Users must have a password"]
        
        user = self.model(
            username = username,
            name = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, name):
        user = self.create_user(
            username = username,
            password = password,
            name = name
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class Message(models.Model):
    msg = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    
    def __str__(self):
        return msg


class Account(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=16, null=True, blank=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)

    bank = models.CharField(max_length=50)
    bank_account = models.CharField(max_length=30)

    profit = models.CharField(max_length=15, null=True, default="0")
    duration = models.CharField(max_length=10, null=True, default="0")
    deposit = models.CharField(max_length=15, null=True, default="0")
    amount = models.CharField(max_length=15, null=True, default="0")


    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name',]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def para(self):
        return ["Name","Phone","Profit","Duration","Deposit","Amount"," "]

    def list(self):
        return [self.name,self.phone,self.profit,self.duration,self.deposit,self.amount,self.id]


class UserAction(models.Model):
    action = models.CharField(max_length=200)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(user)+":"+action

class UserTransactions(models.Model):
    transaction = models.CharField(max_length=200)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(date_created).split(".")[0]+" : "+transaction

class Blog(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=1000)
    image = models.ImageField(null=True, blank=True)

class Portfolio_data(models.Model):
    average_profit = models.CharField(max_length=15)
    average_return_of_investment = models.CharField(max_length=15)
    total_investment_profit = models.CharField(max_length=15)
    total_investment_contra = models.CharField(max_length=15)
    total_investment_lost = models.CharField(max_length=15)


class About_data(models.Model):
    founded = models.CharField(max_length=15)
    header = models.CharField(max_length=250)
    topic1 = models.CharField(max_length=500)
    body1 = models.CharField(max_length=500)
    topic2 = models.CharField(max_length=500)
    body2 = models.CharField(max_length=500)
    