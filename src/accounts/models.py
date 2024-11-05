from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser





class MyAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, gender, email, password=None):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have a username.')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name, 
            gender=gender,
        )

        user.set_password(password)   
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password, gender='M'):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            gender=gender
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
  


class Account(AbstractBaseUser):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name= models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER,  blank=True, null=True)  


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Ensure these are included 


    objects = MyAccountManager()
    
    
    def __str__(self):
         return self.username
     
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def has_perm(self, perm, obj=None):
         return self.is_admin
    
    def has_module_perms(self, app_label):
            return True
            
            



class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    bio  = models.TextField(max_length=1000, blank=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='users', default='avatar.png', blank=True)  
    
    def __str__(self) -> str:
        return f'Profile Of {self.user.get_full_name}'            