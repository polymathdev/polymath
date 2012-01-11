from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    blurb = models.TextField()

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
        

class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CourseCategory, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    creator = models.ForeignKey(UserProfile, related_name='courses_created')
    category = models.ForeignKey(CourseCategory)
    name = models.CharField(max_length=200)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(editable=False, unique=True)
    
    photo = models.ImageField(upload_to='course_profile_pics', blank=True)

    followers = models.ManyToManyField(UserProfile, related_name='courses_following')

    tags = TaggableManager()
    
    class Meta:
        ordering = ['-creation_date']

    # WE DON'T WANT COURSE NAMES TO CHANGE, RIGHT?  MAY NEED TO UDPATE THIS ACCORDINGLY
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.name
        

class Lesson(models.Model): 
    course = models.ForeignKey(Course, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    order = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    completers = models.ManyToManyField(UserProfile, through='LessonCompletion', editable=False) 

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name


class LessonCompletion(models.Model):
    lesson = models.ForeignKey(Lesson, editable=False)
    user_profile = models.ForeignKey(UserProfile, editable=False)
    date_completed = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user_profile.user.first_name + " " + self.user_profile.user.last_name + " --> " + self.lesson.name


class LessonVote(models.Model):
    lesson = models.ForeignKey(Lesson, editable=False)
    user_profile = models.ForeignKey(UserProfile, editable=False)
    up = models.BooleanField()
    date_voted = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self):
        return self.user_profile.user.first_name + " " + self.user_profile.user.last_name + " --> " + self.lesson.name 
