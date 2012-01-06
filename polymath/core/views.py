from django.shortcuts import render_to_response, get_object_or_404, render
from core.models import Course, Lesson, CourseCategory, LessonCompletion
from taggit.models import Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.forms import CourseForm, LessonForm, OrderedLessonFormSet
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import ModelForm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils import simplejson as json
from django.core.exceptions import ObjectDoesNotExist
import ipdb 

def test(request):
    
    c = Course.objects.get(pk=3)
    
    return render(request, 'test.dtl', {
        'all_lessons' : Lesson.objects.all(),
        'course_lessons' : c.lesson_set.all()
        })

def home_page(request):
    return render(request, 'home_page.dtl')

def view_profile(request, uname):
    profile_owner = get_object_or_404(User, username=uname)    
    user_profile = profile_owner.get_profile()

    user_blurb = user_profile.blurb
    courses_created_by_user = user_profile.courses_created.all()

    # EVALUATE AND OPTIMIZE THE BELOW IF POSSIBLE, THE CODE IS RATHER MESSY IN MY OPINION

    courses_following = user_profile.courses_following.select_related('category').all()

    lessons_following = Lesson.objects.filter(course__in=courses_following)
    lessons_following_completed = Lesson.objects.filter(course__in=courses_following, completers=request.user.get_profile())  

    lessons = { les['id'] : les for les in lessons_following.values() }
    completed_lessons = { les['id'] : les for les in lessons_following_completed.values() }

    courses_following_with_progress = { c['id'] : c for c in courses_following.values() }

    for c in courses_following:
        courses_following_with_progress[c.id]['category_id'] = c.category.id
        courses_following_with_progress[c.id]['category'] = c.category.name

    course_progress = { c.id : { 'total' : 0, 'completed' : 0 } for c in courses_following } 

    for les_id, les in lessons.iteritems():
        course_progress[les['course_id']]['total'] = course_progress[les['course_id']]['total'] + 1

        if completed_lessons.has_key(les_id):
            course_progress[les['course_id']]['completed'] = course_progress[les['course_id']]['completed'] + 1 
    
    for c_id, c in courses_following_with_progress.iteritems():
       c['total'] = course_progress.get(c_id, 0)['total']
       c['completed'] = course_progress.get(c_id, 0)['completed']
    

    courses_following = courses_following_with_progress.values()

    return render_to_response('view_profile.dtl', {
    'profile_owner': profile_owner,
	'user_blurb': user_blurb,
    'courses_created_by_user': courses_created_by_user,
    'courses_following': courses_following,
    'is_my_profile': (profile_owner == request.user)
    },
    context_instance=RequestContext(request))

    
@login_required
def view_myprofile(request):
    return view_profile(request, request.user.username)


def view_course(request, course_slug):
    requested_course = get_object_or_404(Course, slug=course_slug)
    creator = requested_course.creator.user
    lesson_list = requested_course.lesson_set.all()

    completed_lesson_list = None
    
    if request.user.is_authenticated():
        completed_lesson_list = Lesson.objects.filter(course=requested_course, completers=request.user.get_profile()) 

    return render_to_response('view_course.dtl',  {
        'requested_course': requested_course,
        'course_tags': requested_course.tags.all(),
	    'lessons': lesson_list,
        'completed_lessons': completed_lesson_list,
        'creator': creator,
        'is_my_course': (creator == request.user),
        'to_client': json.dumps({'complete_lesson_url': reverse('complete_lesson')})
    },
    context_instance=RequestContext(request))


@login_required
def add_course(request):
    EditLessonFormSet = inlineformset_factory(Course, Lesson, can_delete=False, form=LessonForm, formset=OrderedLessonFormSet, extra=1) 
 
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        lesson_fs = EditLessonFormSet(request.POST) 
        
        if course_form.is_valid() and lesson_fs.is_valid():
            new_course = course_form.save(commit=False)
            new_course.creator = request.user.get_profile()
            new_course.save()
            # save tags
            course_form.save_m2m()

            lesson_fs.instance = new_course
            lesson_fs.save()

            messages.success(request, 'Your course has been created! Share it with your friends on Twitter and Facebook.')
            return HttpResponseRedirect('/myprofile/')

    else:
        course_form = CourseForm()            
        lesson_fs = EditLessonFormSet()

	messages.success(request, 'Share your expertise by creating a course on a topic - a collection of resources for someone to progress through to learn about the subject. Get creative! You\'re the expert.')
    return render_to_response('add_course2.dtl', {
        'course_form': course_form,
        'lesson_fs': lesson_fs,
        'is_add_page': True
    },
    context_instance=RequestContext(request))

@login_required
def edit_course(request, course_slug):
    course_to_edit = get_object_or_404(Course, slug=course_slug)

    # don't let people edit courses that other people created
    if request.user != course_to_edit.creator.user:
        messages.error(request, 'You can only edit courses that you have created')
        return HttpResponseRedirect('/courses/'+course_slug)

    EditLessonFormSet = inlineformset_factory(Course, Lesson, can_delete=False, form=LessonForm, formset=OrderedLessonFormSet, extra=1)
    
    if request.method == 'POST':
        
        edit_course_form = CourseForm(request.POST, instance=course_to_edit)
        edit_lesson_fs = EditLessonFormSet(request.POST, instance=course_to_edit)
        
        if edit_course_form.is_valid() and edit_lesson_fs.is_valid():
            edit_course_form.save() 
            edited_lessons = edit_lesson_fs.save()
            
            messages.success(request, 'Your changes have been saved!')
            return HttpResponseRedirect('/courses/'+course_slug)
        
    else:
        edit_course_form = CourseForm(instance=course_to_edit)
        edit_lesson_fs = EditLessonFormSet(instance=course_to_edit)
        
    return render_to_response('add_course2.dtl', {
        'course_form': edit_course_form,
        'lesson_fs': edit_lesson_fs,
        'to_client': json.dumps({'delete_lesson_url': reverse('delete_lesson')})
    },
    context_instance=RequestContext(request))


@login_required
def delete_lesson(request):
    if not request.method == 'POST':
        raise Http404

    lesson_id = request.POST['lesson_id']
    delete_successful = False
    
    try:
        lesson_to_delete = Lesson.objects.get(id=lesson_id)

        if request.user != lesson_to_delete.course.creator.user:
            result_message = 'You cannot delete lessons you did not create! (this is most likely a bug)'
        else:
            lesson_to_delete.delete()
            delete_successful = True
            result_message = 'Lesson deleted'

    except ObjectDoesNotExist:
        result_message = 'That lesson does not exist (this is most likely a bug)'  # don't want 404 here because then the front-end will just silently fail since this is responding to an ajax request

    return HttpResponse(json.dumps({'delete_successful' : delete_successful, 'result_message' : result_message}), mimetype="application/json")


@login_required
def complete_lesson(request):
    if not request.method == 'POST':
        raise Http404

    lesson_id = request.POST['lesson_id']
    complete_successful = False

    try:
        lesson_to_complete = Lesson.objects.get(id=lesson_id)
        LessonCompletion.objects.create(lesson=lesson_to_complete, user_profile=request.user.get_profile()) 

        # update the course followers table so that any user who has marked a lesson as 'done' is now following that course
        lesson_to_complete.course.followers.add(request.user.get_profile())

        complete_successful = True
        result_message = "Got it, you\'ve done that!"

    except ObjectDoesNotExist:
        result_message = 'That lesson does not exist (this is most likely a bug)'  # don't want 404 here because then the front-end will just silently fail since this is responding to an ajax request

    return HttpResponse(json.dumps({'complete_successful' : complete_successful, 'result_message' : result_message}), mimetype="application/json")



def browse_courses(request, cat_slug=None, tag_slug=None):
    tags_by_cat = None
    course_list = None
    filters = None                            

    # default browse page with no filtering
    if not cat_slug and not tag_slug:
        cats = CourseCategory.objects.all()
        tags_by_cat = { cat : Course.tags.filter(course__category=cat) for cat in cats }
        course_list = Course.objects.all().select_related()

    if cat_slug:
        cat = CourseCategory.objects.get(slug=cat_slug) 

        # browse a single category
        if not tag_slug:
            tags_by_cat = { cat : Course.tags.filter(course__category=cat) }
            course_list = Course.objects.filter(category=cat)

        # filter by both category and tag
        else:
            course_list = Course.objects.filter(category=cat, tags__slug=tag_slug)     
            filters = { 'category' : cat , 'tag' : Tag.objects.get(slug=tag_slug) }

    return render(request, 'browse_courses.dtl', {
        'tags_by_cat' : tags_by_cat,
        'course_list' : course_list,
        'filters' : filters
        })


# security vulnerability?
# used for 
@login_required
def quick_ajax_post(request, view_to_call):
    if not request.method == 'POST':
        raise Http404

    func = getattr(self, view_to_call)

    return func(request)
