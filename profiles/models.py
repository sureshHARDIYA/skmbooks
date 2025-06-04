from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Custom User model - this is the primary authentication model for the app
# It replaces Django's built-in User model as specified in settings.AUTH_USER_MODEL
class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "email"
    username = None
    email = models.EmailField(unique=True)
    
    REQUIRED_FIELDS = []
    USER_TYPE_BACKOFFICE = 'backoffice'
    USER_TYPE_STUDENT = 'student'
    USER_TYPE_SUPERADMIN = 'superuser'
    
    USER_GENDER_MALE = 'm'
    USER_GENDER_FEMALE = 'f'
    USER_GENDER_UNKNOWN = 'u'
    GENDER_CHOICES = [
        (USER_GENDER_MALE, "Male"),
        (USER_GENDER_FEMALE, "Female"),
        (USER_GENDER_UNKNOWN, "Unknown"),
    ]


    CHOICES = [
        [USER_TYPE_BACKOFFICE, USER_TYPE_BACKOFFICE],
        [USER_TYPE_STUDENT, USER_TYPE_STUDENT],
        [USER_TYPE_SUPERADMIN, USER_TYPE_SUPERADMIN],
    ]
    


    first_name = models.CharField("first name", max_length=150, blank=False)
    last_name = models.CharField("last name", max_length=150, blank=False)
    nickname = models.CharField(max_length=100, default="", blank=True)
    user_type = models.CharField(max_length=20, choices=CHOICES, default=USER_TYPE_BACKOFFICE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=USER_GENDER_UNKNOWN)
    address = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=50, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")
    zip_code = models.CharField(max_length=10, blank=True, default="")
    picture = models.ImageField(null=True, blank=True)
    cover_picture = models.ImageField(null=True, blank=True)
    about_me = models.TextField(blank=True, default="")
    title = models.CharField(max_length=100, blank=True, default="")
    quizzes_completed = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    
    objects = CustomUserManager()