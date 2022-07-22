from django.db import models

# Create your models here.

class User(models.Model):
    #Telegram Data
    telegram_user_id = models.BigIntegerField(null=True, unique=True)
    telegram_user_name = models.CharField(max_length=255, null=True)
    telegram_first_name = models.CharField(max_length=255, null=True)
    telegram_last_name = models.CharField(max_length=255, null=True)
    telegram_language = models.CharField(max_length=255, null=False)
    telegram_is_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    #User Input Data
    name = models.CharField(max_length=100, default="None")
    phone_number = models.CharField(max_length=100, default="None")
    
    #Time of Creating and Updating
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #User Sheet Column
    # sheet_column =  models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


class Group(models.Model):
    #Relations
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    #Telegram Data
    telegram_group_id = models.BigIntegerField(null=True, unique=True)
    telegram_group_title = models.CharField(max_length=255, null=True)
    telegram_url = models.CharField(max_length=255, null=True, unique=True)
    telegram_counts = models.IntegerField(default=0, null=True)
    telegram_chat_type = models.CharField(max_length=255, null=True)

    #Telegram Group Inputs
    start = models.IntegerField(null=True)
    end = models.IntegerField(null=True)
    period = models.CharField(max_length=25, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.telegram_group_title


class Sheet(models.Model):
    telegram_user_id = models.BigIntegerField(null=True, unique=True)
    name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    group_one = models.CharField(max_length=255, default="مغادر")
    group_two = models.CharField(max_length=255, default="مغادر")
    group_three = models.CharField(max_length=255, default="مغادر")


    