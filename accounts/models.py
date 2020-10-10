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
    username = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    Messages = models.ManyToManyField(Message, blank=True)

    is_superuser = models.BooleanField(default=False)
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

    def list(self):
        return [self.username,self.name,self.phone,self.profile_pic,self.date_created,self.last_login,self.Messages]


class UserAction(models.Model):
    action = models.CharField(max_length=200)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(user)+":"+action

class MachineData(models.Model):
    IP = models.CharField(max_length=20)
    Line = models.CharField(max_length=30)
    Page = models.CharField(max_length=30)
    Name = models.CharField(max_length=80)
    Parameter = models.CharField(max_length=30)
    Code = models.CharField(max_length=30, unique=True)
    Address = models.CharField(max_length=30)
    Unit = models.CharField(max_length=10)
    low_limit = models.CharField(max_length=10)
    upper_limit = models.CharField(max_length=10)
    Value = models.DecimalField(decimal_places = 2, max_digits=8, default=0.00)
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastEdit = models.DateTimeField(null=True)
    Dev = models.CharField(max_length=30, null=True)
    
    def __str__(self):
        return self.Code

    def parameter(self):
        return ["Line","Page","Code","Machine Name","Unit","Last Seen"]

    def list(self):
        return [self.Line,self.Page,self.Code,self.Name,self.Unit,self.LastEdit]
           
class LogData(models.Model):
    DateCreated = models.DateTimeField(null=True)
    Value = models.FloatField(default=0)
    Machine = models.ForeignKey(MachineData,null=True, on_delete= models.CASCADE)
    def __str__(self):
        return str(self.Machine.Code)+":"+str(self.Value)

    def parameter(self):
        return ["Date","Line","Name","Value","Unit"]
        
    def list(self):
        return [self.DateCreated.strftime('%d/%m/%y %H:%M:%S'),self.Machine.Line,self.Machine.Name,self.Value,self.Machine.Unit]


class IOTDev(models.Model):
    DateCreated = models.DateTimeField(auto_now_add=True)
    Site = models.CharField(max_length=30, unique=True)
    Passport = models.CharField(max_length=30)
    CSRFTok = models.CharField(null=True, max_length=12)
    LastSeen = models.DateTimeField(null=True)
    def __str__(self):
        return str(self.Site)