from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from facepy import GraphAPI
import ipdb

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    blurb = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='user_profile_pics', blank=True)
    fb_profile_pic = models.URLField(blank=True)
    fb_profile_thumb = models.URLField(blank=True)

    def get_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        else:
            return self.fb_profile_pic

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


# I should probably use the pipeline flow of django-social-auth instead of this signal - will redo that later maybe
from social_auth.signals import socialauth_registered

def new_users_handler(sender, user, response, details, **kwargs):
    user.is_new = True
    ipdb.set_trace()
    # this should be refactored into some other module once we start using facebook more
    fb_data = user.social_auth.get(provider='facebook').extra_data
    access_token = fb_data['access_token']

    fb_uid = fb_data['id']
    fb = GraphAPI(access_token)
    fb_pics = fb.get('fql',q='select pic_big, pic_square from user where uid='+fb_uid) 

    profile = user.get_profile() 
    profile.fb_profile_pic = fb_pics['data'][0]['pic_big']
    profile.fb_profile_thumb = fb_pics['data'][0]['pic_square']

    profile.save()

    return False


socialauth_registered.connect(new_users_handler, sender=None)


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CourseCategory, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    creator = models.ForeignKey(User, related_name='courses_created')
    category = models.ForeignKey(CourseCategory)
    name = models.CharField(max_length=200)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(editable=False)
    
    photo = models.ImageField(upload_to='course_profile_pics', blank=True)

    followers = models.ManyToManyField(User, related_name='courses_following', blank=True)

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

    completers = models.ManyToManyField(User, through='LessonCompletion', editable=False) 

    # count up votes as +1 and down votes as -1 to calculate an aggregate score for this lesson
    def vote_score(self):
        score = 0
        votes = self.lessonvote_set.all()

        for v in votes:
            if v.up:
                score += 1
            else:
                score -= 1

        return score


    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name


class LessonCompletion(models.Model):
    lesson = models.ForeignKey(Lesson, editable=False)
    user_profile = models.ForeignKey(User, editable=False)
    date_completed = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user_profile.first_name + " " + self.user_profile.last_name + " --> " + self.lesson.name


class LessonVote(models.Model):
    lesson = models.ForeignKey(Lesson)
    user_profile = models.ForeignKey(User)
    up = models.BooleanField()
    date_voted = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self):
        return self.user_profile.first_name + " " + self.user_profile.last_name + " --> " + self.lesson.name 
