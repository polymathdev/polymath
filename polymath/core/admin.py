from core.models import Course, Lesson, UserProfile, CourseCategory, LessonCompletion
from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# user/userprofile stuff
admin.site.unregister(User)
      
class UserProfileInline(admin.StackedInline):
    model = UserProfile
                   
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
                            
admin.site.register(User, UserProfileAdmin)
                 




# my stuff
class LessonUnderCourse(admin.StackedInline):
	model = Lesson
	extra = 1

class CourseAdmin(admin.ModelAdmin):
	inlines = [LessonUnderCourse]

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory)
admin.site.register(LessonCompletion)

