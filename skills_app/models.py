from django.db import models
import re
import bcrypt 
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "All fields must be present" 
        elif postData['password'] != postData['confirm']:
            errors['password'] = "Passwords do not match."
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = ("email address!")
        return errors
    def basic_login(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = ("Invalid Data!")
        if len(postData['password']) < 1:
            errors[ 'password'] = ("Invalid entry")
        return errors 

class User(models.Model):
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length= 14)
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=20)
    confirmpw = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

    # def __repr__(self):
    #     return f"<User object: {self.name} ({self.id})>"


class SkillManager(models.Manager):
    def skill_validator(self,postData):
        errors = {}
        if len(postData["location"]) < 5:
            errors["location"] = "  location must be at least 5 characters"
        if len(postData['skill']) <10:
            errors['skill'] = " location must be at least 10 characters"
        if len(postData['profession']) <3:
            errors['profession'] = " profession must be at least 3 characters"
        if len(postData['time']) < 5: 
            errors['time']= "please enter a time you would like to donate a skill"
        return errors  

class Skill(models.Model):
    posted_by = models.ForeignKey(User, related_name = "user_skills", on_delete=models.CASCADE, null=True, blank = True)
    location = models.CharField(max_length=14)
    skill= models.TextField()
    profession= models.CharField(max_length=20)
    time= models.CharField(max_length=10)
    
