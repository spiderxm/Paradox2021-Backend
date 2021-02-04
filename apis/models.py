from django.db import models

from django.core.validators import MinLengthValidator


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

    def __str__(self):
        return self.email


class Hints(models.Model):
    """
    Model For Question Hints
    """
    level = models.IntegerField(primary_key=True)
    hint1 = models.CharField(max_length=255, blank=False, null=False)
    hint2 = models.CharField(max_length=255, blank=False, null=False)
    hint3 = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.level)


class Questions(models.Model):
    """
    Model for Questions
    """
    level = models.IntegerField(primary_key=True, auto_created=True)
    location = models.CharField(max_length=255, blank=False, null=False)
    answer = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.level)


class Referral(models.Model):
    """
    Model For Referral
    """
    user = models.ForeignKey(ParadoxUser, on_delete=models.CASCADE, unique=True, primary_key=True)
    ref_code = models.CharField(max_length=255, unique=True)
    ref_success = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email


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
    refferral_availed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Rules(models.Model):
    """
    Model to Store Rules of Paradox
    """
    rule = models.CharField(max_length=255)


class ExeMembers(models.Model):
    """
    Model For Exe Members
    """
    choices = (
        ('Full Stack', 'Full Stack'),
        ('Front End', 'Front End'),
        ('Back End', 'Back End')
    )

    position_choices = (
        ('Developer', 'Developer'),
        ('Mentor', 'Mentor'),
        ('Final year', 'Final year'),
        ('Coordinator', 'Coordinator'),
        ('Executive', 'Executive'),
        ('Volunteer', 'Volunteer')
    )
    name = models.CharField(max_length=255, validators=[
        MinLengthValidator(limit_value=3, message="Name Length Should be greater than 3 charcters.")])
    position = models.CharField(max_length=255, choices=position_choices)
    category = models.CharField(max_length=255, choices=choices, null=True, blank=True)
    image = models.URLField(max_length=255, null=False, blank=False)
    githubUrl = models.URLField(max_length=255, null=True, blank=True, unique=True)
    linkedInUrl = models.URLField(max_length=255, null=True, blank=True, unique=True)


class UserHintLevel(models.Model):
    """
    Model for User Hints
    """
    user = models.ForeignKey(ParadoxUser, on_delete=models.CASCADE, unique=True, primary_key=True)
    level = models.IntegerField(default=1)
    hintNumber = models.IntegerField(default=0)
