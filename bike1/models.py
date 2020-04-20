from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class User_manager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_input']):
            errors['email_error'] = "Invalid email address"
        objects = User_manager()
        if len(postData['first_name_input']) < 2:
            errors['first_name_error'] = "Name must be at least 2 characters"
        if len(postData['last_name_input']) < 2:
            errors['last_night_error'] = "must be at least 2 characters"
        if len(postData['password_input']) < 8:
            print("password")
            errors['password_error'] = "must be at least 8 characters"
        if postData['confirm_password_input'] != postData["password_input"]:
            print("password confirm")
            errors['confirm_password_error'] = "Passwords must match"
        return errors
    def login_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_input']):
            errors['email_error'] = "Invalid email address"
        user = self.get(email=postData['email_input'])
        if user:
            if bcrypt.checkpw(postData['password_input'].encode(), user.password.encode()):
                print("password matches")
        return errors
        if len(postData['email_input']) < 1 or len(postData['password_input']) < 1:
            errors['all_fields_error'] = "All fields required."

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    rider_level=models.CharField(max_length=100, default="Newbie")
    bike_type=models.CharField(max_length=100, default="Road")
    created_at=models.DateTimeField(auto_now_add=True)
    objects=User_manager()

class Trail(models.Model):
    title=models.CharField(max_length=255)
    length=models.FloatField()
    level=models.CharField(max_length=255)
    users=models.ManyToManyField(User, related_name="trails")
    desc=models.TextField()

class Pictures(models.Model):
    img=models.ImageField(upload_to='media/', blank=True)
    title=models.CharField(max_length=255)
    desc=models.TextField()
    user=models.ForeignKey(User, related_name="users_bike", on_delete=models.CASCADE)
    likes=models.ManyToManyField(User, related_name="imgs_liked")

class Messages(models.Model):
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="user_message", on_delete=models.CASCADE)
    # message_comment = list of comments

class Comments(models.Model):
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    bike=models.ForeignKey(Pictures, related_name="comments", on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
