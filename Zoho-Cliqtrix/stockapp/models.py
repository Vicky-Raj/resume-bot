from django.db import models
from django.conf import settings

class Bookmark(models.Model):
    email=models.EmailField()
    url=models.TextField()
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Profile(models.Model):
    network = models.TextField()
    username = models.TextField()
    url = models.TextField()

class String(models.Model):
    highlight = models.TextField()

class Basics(models.Model):
    name = models.TextField()
    label = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    website = models.TextField()
    summary = models.TextField()
    address = models.TextField()
    country = models.TextField()
    region = models.TextField()
    profiles = models.ManyToManyField(Profile)

class Work(models.Model):
    company = models.TextField()
    position = models.TextField()
    website = models.TextField()
    startDate = models.TextField()
    endDate = models.TextField()
    summary = models.TextField()
    highlights = models.ManyToManyField(String)



class Education(models.Model):
    institute = models.TextField()
    area = models.TextField()
    studyType = models.TextField()
    startDate = models.TextField()
    endDate = models.TextField()
    gpa = models.TextField()
    courses = models.ManyToManyField(String)

class Awards(models.Model):
    title = models.TextField()
    date = models.TextField()
    awarder = models.TextField()
    summary = models.TextField()

class Publications(models.Model):
    name = models.TextField()
    publisher = models.TextField()
    releaseDate = models.TextField()
    website = models.TextField()
    summary = models.TextField()


class References(models.Model):
    name = models.TextField()
    reference = models.TextField()

class Client(models.Model):
    email = models.EmailField()

class Resume(models.Model):
    client = models.ForeignKey(Client,models.CASCADE)
    name = models.TextField()
    basics = models.ForeignKey(Basics,on_delete=models.CASCADE)
    works = models.ManyToManyField(Work)
    education = models.ManyToManyField(Education)
    awards = models.ManyToManyField(Awards)
    publications = models.ManyToManyField(Publications)
    skills = models.ManyToManyField(String,related_name="skills")
    languages = models.ManyToManyField(String,related_name="languages")
    interests = models.ManyToManyField(String,related_name="interests")
    references = models.ManyToManyField(References)
    file = models.TextField(null=True,blank=True)
    def __str__(self):
        return f"{self.name}"