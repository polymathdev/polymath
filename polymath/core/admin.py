from core.models import Course, Lesson, UserProfile, CourseCategory, LessonCompletion, LessonVote
from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# user/userprofile stuff
admin.site.unregister(User)
      
class UserProfileInline(admin.StackedInline):
    model = UserProfile
                   
class LessonVoteUnderUser(admin.StackedInline):
    model = LessonVote

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
                            
class LessonUnderCourse(admin.StackedInline):
	model = Lesson
	extra = 1

class CourseAdmin(admin.ModelAdmin):
	inlines = [LessonUnderCourse]

admin.site.register(User, UserProfileAdmin) 
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(LessonCompletion)
admin.site.register(LessonVote)
admin.site.register(Lesson)
