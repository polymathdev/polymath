from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Count
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from annoying.functions import get_object_or_None 
from facepy import GraphAPI
import ipdb

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    blurb = models.TextField(blank=True, default='Polymath Newbie')
    profile_pic = models.ImageField(upload_to='user_profile_pics', blank=True)
    fb_profile_pic = models.URLField(blank=True)
    fb_profile_thumb = models.URLField(blank=True)

    def get_facebook_url(self):
        return u'http://www.facebook.com/profile.php?id=' + self.user.social_auth.get(provider='facebook').uid

    def get_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        else:
            return self.fb_profile_thumb

    def courses_with_progress(self):
        """
        get a list of dictionaries that contains data about all of the courses that this user has completed at least 1 lesson in
        each dictionary in the list contains the course object, the number of total lessons, and the number of lessons this user has completed
        """
        # get the courses that the user has completed lessons on, each annotated with the number of completed lessons by this user
        courses_with_completions = Course.objects.filter(lesson__lessoncompletion__user_profile=self.user).annotate(num_completed=Count('lesson__lessoncompletion'))

        # << the reason I added num_lessons in here is because I can get all of them with 1 query, as opposed to calling course.lesson_set.count in the template which would query for each course >> #
        # << maybe i can use select_related() to get all of the lesson data in 1 query somewhere? >>

        # get a list of the above courses, each annotated with the number of total lessons in each respective course
        courses_with_num_lessons = Course.objects.annotate(num_lessons=Count('lesson')).filter(pk__in=courses_with_completions)

        # build a dictionary that maps course id to total number of lessons in that course
        id_to_lessons = { c.id : c.num_lessons for c in courses_with_num_lessons }

        # build the list of dictionaries to return, as described in docstring
        courses_with_progress_data = [ { 'course' : c, 'num_lessons' : id_to_lessons[c.id], 'num_completed' : c.num_completed } for c in courses_with_completions ]

        return courses_with_progress_data

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

    # send quick+dirty welcome email
    message = 'Hey ' + user.first_name + ',\n\nWelcome to Polymath!\n\n'
    message += 'We\'re working on building a central resource for the web\'s best educational content and the ultimate community-based online learning experience.\n\n'
    message += 'Learn more here: http://beta.whatispolymath.com/howitworks/\n\n'
    message += 'Looking forward to seeing you out there!\n\n'
    message += 'Thanks,\nThe Polymath Team'

    send_mail('Welcome to Polymath!', message, 'Polymath <hello@whatispolymath.com>', [user.email])

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
    slug = models.SlugField(max_length=200, editable=False)
    
    photo = models.ImageField(upload_to='course_profile_pics', blank=True)

    followers = models.ManyToManyField(User, related_name='courses_following', blank=True)

    tags = TaggableManager()
    
    FEATURED_HOMEPAGE_POSITIONS = [('A', 'Left'), ('B', 'Middle'), ('C', 'Right')]

    homepage_featured = models.CharField(max_length=1, blank=True, choices=FEATURED_HOMEPAGE_POSITIONS)

    # get a unique list of the users who have completed at least one lesson in this course
    def users_with_progress(self):
        return User.objects.filter(lessoncompletion__lesson__in=self.lesson_set.all()).distinct()

    class Meta:
        ordering = ['-creation_date']

    # update the slug on save
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
        

class Lesson(models.Model): 
    course = models.ManyToManyField(Course, editable=False, blank=True)
    completers = models.ManyToManyField(User, through='LessonCompletion', editable=False) 
    category = models.ForeignKey(CourseCategory) # should change CourseCategory to just Category at some point, given that it looks like we'll be applying them to both Lessons and Courses.
    creator = models.ForeignKey(User, related_name='lessons_created') 

    slug = models.SlugField(max_length=200, editable=False) 
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    order = models.IntegerField(blank=True, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)

    LESSON_TYPES = [('t', 'Text'), ('v', 'Video'), ('i', 'Interactive')]

    type = models.CharField(max_length=1, blank=True, choices=LESSON_TYPES)

    tags = TaggableManager(blank=True) 

    # don't allow a duplicate URL for standalone lessons (i.e. lessons without courses)
    def clean(self):
        from django.core.exceptions import ValidationError
        
        duplicate = get_object_or_None(Lesson, link=self.link, course=None)

        if duplicate:
            raise ValidationError('StandaloneDuplicate::'+str(duplicate.pk))

    # update the slug on save
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Lesson, self).save(*args, **kwargs)

	# get list of users who've voted on a lesson
    def users_voted(self):
		return User.objects.filter(lessonvote__lesson=self)

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
    lesson = models.ForeignKey(Lesson)
    user_profile = models.ForeignKey(User)
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
