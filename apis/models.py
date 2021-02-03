from django.db import models

from django.core.validators import MinLengthValidator


# Create your models here.

class ParadoxUser(models.Model):
    """
    Model for Paradox Users
    """
    google_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False,
                            validators=[
                                MinLengthValidator(limit_value=3, message="Minimum Length should be 3 Characters")])
    email = models.EmailField(max_length=255, blank=False, null=False, unique=True)
    ref_code = models.CharField(max_length=255, blank=False, null=False)


class Hints(models.Model):
    """
    Model For Question Hints
    """
    level = models.IntegerField(primary_key=True)
    hint1 = models.CharField(max_length=255, blank=False, null=False)
    hint2 = models.CharField(max_length=255, blank=False, null=False)
    hint3 = models.CharField(max_length=255, blank=False, null=False)


class Questions(models.Model):
    """
    Model for Questions
    """
    level = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=255, blank=False, null=False)
    answer = models.CharField(max_length=255, blank=False, null=False)


class Referral(models.Model):
    """
    Model For Referral
    """
    user = models.ForeignKey(ParadoxUser, on_delete=models.CASCADE, unique=True, primary_key=True)
    ref_code = models.CharField(max_length=255, unique=True)
    ref_success = models.IntegerField(default=0)


class Profile(models.Model):
    """
    Model For User Profile
    """
    user = models.ForeignKey(ParadoxUser, on_delete=models.CASCADE, unique=True, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.URLField(max_length=255, null=False, blank=False)
    reg_time = models.DateTimeField(auto_now=True)
    level = models.IntegerField(default=1)
    attempts = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    coins = models.IntegerField(default=100)
    super_coins = models.IntegerField(default=100)
