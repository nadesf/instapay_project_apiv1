from django.db import models

# Create your models here.

class Users(models.Model):

    user_id = models.CharField(max_length=12, null=False, blank=False, primary_key=True, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=100, unique=True, default=None)
    password = models.CharField(max_length=100, blank=False, null=False)
    active = models.BooleanField(default=False)
    send_code = models.CharField(max_length=30)
    receive_code = models.CharField(max_length=30)
    status_user =  models.CharField(max_length=50, default="client")
    date_created = models.DateTimeField(auto_now_add=True)
    ip_addresses = models.CharField(max_length=50)
    access_ressource_code = models.CharField(max_length=30, default="NoCode")
    name_pointofsale = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)


class Transactions(models.Model):

    transaction_id = models.CharField(max_length=30, unique=True, primary_key=True)
    sender = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name="user_sender", null=True)
    recipient = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name="user_receiver", null=True)
    amount = models.FloatField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, null=False, default="En Attente")
    validation_code = models.CharField(max_length=6, unique=True, blank=True, null=True)

class Providers(models.Model):

    provider_id = models.CharField(max_length=9, unique=True, primary_key=True)
    provider_name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

class Accounts(models.Model):

    account_id = models.CharField(max_length=12, primary_key=True, unique=True)
    amount = models.FloatField(default=1000000)
    owner = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name="account_owner", null=True)
    status_account = models.BooleanField(default=True)
    provider = models.ForeignKey(Providers, on_delete=models.SET_NULL, null=True, default="Instapay", related_name="account_provider")