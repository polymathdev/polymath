from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from core.models import Course, Lesson, CourseCategory, LessonCompletion, LessonVote
from taggit.models import Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.forms import CourseForm, LessonForm, OrderedLessonFormSet, ProfileForm
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import ModelForm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils import simplejson as json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from annoying.functions import get_object_or_None
from facepy import GraphAPI
import ipdb, re

def test(request):
    ipdb.set_trace()
    fb_data = request.user.social_auth.get(provider='facebook').extra_data
    access_token = fb_data['access_token']
    fb_uid = fb_data['id']
    fb = GraphAPI(access_token)
    pic = fb.get('fql',q='select pic_big from user where uid='+fb_uid)
     
    ipdb.set_trace()

    return render(request, 'test.dtl', {
        'course_form' : cf
        })


def welcome(request):
    return_to_course = None
    referer = request.META.get('HTTP_REFERER', None)

    # grab the url of the refering page and check to see if it was a course page
    if referer:
        view_course_url_pattern = re.compile(r'^.*/courses/(?P<course_id>\d+)/.*')
        match = view_course_url_pattern.match(referer)

        # if it was a course page, on the welcome page let's give the user a link back to the course they were looking at
        if match:
            course_id = int(match.group('course_id')) 
            return_to_course = get_object_or_None(Course, pk=course_id)

    return render(request, 'howitworks.dtl', {
        'return_to_course' : return_to_course,
        'is_welcome' : True
        })

def new_user(request):
    ipdb.set_trace()

    return render(request, 'test.dtl')

def home_page(request):
    return render(request, 'home_page.dtl')

def view_profile(request, uname):
    profile_owner = get_object_or_404(User, username=uname)    
    user_profile = profile_owner.get_profile()

    profile_edit_form = None

    # if the current user is the profile owner, give them the profile edit form
    if request.user == profile_owner:
        profile_edit_form = ProfileForm(instance=user_profile)
        
        # if this is a POST from the profile's owner, assume (for now) that the profile edit form was submitted and update accordingly 
        if request.method == 'POST':
            profile_edit_form = ProfileForm(request.POST, request.FILES, instance=user_profile)

            if profile_edit_form.is_valid():
                profile_edit_form.save()
                messages.success(request, 'Your profile changes have been saved') 

                return redirect('view_profile', uname=uname)

    user_blurb = user_profile.blurb
    courses_created_by_user = profile_owner.courses_created.all()
     
    # EVALUATE AND OPTIMIZE THE BELOW IF POSSIBLE, THE CODE IS RATHER MESSY IN MY OPINION AND THERE ARE PROBABLY MUCH BETTER WAYS TO DO THIS

    upvoted_lessons = LessonVote.objects.filter(user_profile=profile_owner).select_related('course')
    courses_following = profile_owner.courses_following.select_related('category').all()

    lessons_following = Lesson.objects.filter(course__in=courses_following)
    lessons_following_completed = Lesson.objects.filter(course__in=courses_following, completers=profile_owner)  

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
    'upvoted_lessons': upvoted_lessons,
    'is_my_profile': (profile_owner == request.user),
    'profile_edit_form': profile_edit_form
    },
    context_instance=RequestContext(request))

    
@login_required
def view_myprofile(request):
    return view_profile(request, request.user.username)


def view_course(request, course_id, course_slug=None):
    requested_course = get_object_or_404(Course, pk=course_id)

    # redirect to appropriate URL with complete slug if necessary (this is a cosmetic thing)
    if course_slug != requested_course.slug:
        return redirect('view_course', permanent=True, course_id=course_id, course_slug=requested_course.slug)

    creator = requested_course.creator
    lesson_list = requested_course.lesson_set.all()

    completed_lesson_list = None
    
    # list of dictionaries where each contains relevant info about a lesson.  initialize with 'lesson' key to contain Lesson object
    lesson_list_info = [ {'lesson' : l } for l in lesson_list ]

    if request.user.is_authenticated():
        # lessons that the current user has completed for this course
        completed_lesson_list = Lesson.objects.filter(course=requested_course, completers=request.user) 

        # all votes that the current user has made on lessons in this course
        lesson_votes = LessonVote.objects.filter(lesson__in=lesson_list, user_profile=request.user)
        
        for l in lesson_list_info:

             # add a 'completed' key to this lesson info item if it has been completed
            if l['lesson'] in completed_lesson_list:
                l['completed'] = True

            # set 'my_vote' key to the appropriate value if necessary based on lesson_votes queryset
            try:
                vote = lesson_votes.get(lesson=l['lesson'])
                if vote:
                    if vote.up:
                        l['my_vote'] = 'up'
                    else:
                        l['my_vote'] = 'down'

            except ObjectDoesNotExist:
                pass

    return render_to_response('view_course.dtl',  {
        'requested_course': requested_course,
        'course_tags': requested_course.tags.all(),
	    'lessons': lesson_list_info,
        'completed_lessons': completed_lesson_list,
        'creator': creator,
        'is_my_course': (creator == request.user),
        'next' : reverse('view_course', kwargs={'course_id':course_id,'course_slug':course_slug}),
        'delete_comment_action' : reverse('simple_comments_delete'),
        'to_client': json.dumps({'complete_lesson_url': reverse('complete_lesson'), 'vote_lesson_url' : reverse('vote_lesson')})
    },
    context_instance=RequestContext(request))


@login_required
def add_course(request):
    EditLessonFormSet = inlineformset_factory(Course, Lesson, can_delete=False, form=LessonForm, formset=OrderedLessonFormSet, extra=1) 
                                         
    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        lesson_fs = EditLessonFormSet(request.POST)     
        
        if course_form.is_valid() and lesson_fs.is_valid():
            new_course = course_form.save(commit=False)
            new_course.creator = request.user
            new_course.save()
            # save tags
            course_form.save_m2m()

            lesson_fs.instance = new_course
            lesson_fs.save()

            messages.success(request, 'Your course has been created! Share it with your friends on Twitter and Facebook.')
            return redirect('view_my_profile')

    else:
        course_form = CourseForm()            
        lesson_fs = EditLessonFormSet()

	messages.success(request, 'A course is a set of resources for someone to progress through to learn about the subject. Get creative! You\'re the expert.')
    return render_to_response('add_course2.dtl', {
        'course_form': course_form,
        'lesson_fs': lesson_fs,
        'is_add_page': True
    },
    context_instance=RequestContext(request))

@login_required
def edit_course(request, course_id):
    course_to_edit = get_object_or_404(Course, pk=course_id)

    # don't let people edit courses that other people created
    if request.user != course_to_edit.creator:
        messages.error(request, 'You can only edit courses that you have created')
        return redirect('view_course', course_id=course_id, course_slug=course_to_edit.slug)

    EditLessonFormSet = inlineformset_factory(Course, Lesson, can_delete=False, form=LessonForm, formset=OrderedLessonFormSet, extra=1)
    
    if request.method == 'POST':
        
        edit_course_form = CourseForm(request.POST, request.FILES, instance=course_to_edit)
        edit_lesson_fs = EditLessonFormSet(request.POST, instance=course_to_edit)
        
        if edit_course_form.is_valid() and edit_lesson_fs.is_valid():
            edit_course_form.save() 
            edited_lessons = edit_lesson_fs.save()
            
            messages.success(request, 'Your changes have been saved!')
            return redirect('view_course', course_id=course_id, course_slug=course_to_edit.slug) 
        
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
@require_POST
def delete_lesson(request):

    lesson_id = request.POST['lesson_id']
    delete_successful = False
    
    try:
        lesson_to_delete = Lesson.objects.get(id=lesson_id)

        if request.user != lesson_to_delete.course.creator:
            result_message = 'You cannot delete lessons you did not create! (this is most likely a bug)'
        else:
            lesson_to_delete.delete()
            delete_successful = True
            result_message = 'Lesson deleted'

    except ObjectDoesNotExist:
        result_message = 'That lesson does not exist (this is most likely a bug)'  # don't want 404 here because then the front-end will just silently fail since this is responding to an ajax request

    return HttpResponse(json.dumps({'delete_successful' : delete_successful, 'result_message' : result_message}), mimetype="application/json")


@login_required
@require_POST
def complete_lesson(request):

    lesson_id = request.POST['lesson_id']
    complete_successful = False

    try:
        lesson_to_complete = Lesson.objects.get(id=lesson_id)
        LessonCompletion.objects.create(lesson=lesson_to_complete, user_profile=request.user) 

        # update the course followers table so that any user who has marked a lesson as 'done' is now following that course
        # lesson_to_complete.course.followers.add(request.user)

        complete_successful = True
        result_message = "Got it, you\'ve done that!"

    except ObjectDoesNotExist:
        result_message = 'That lesson does not exist (this is most likely a bug)'  # don't want 404 here because then the front-end will just silently fail since this is responding to an ajax request

    return HttpResponse(json.dumps({'complete_successful' : complete_successful, 'result_message' : result_message}), mimetype="application/json")


# I should really test for the existence of any required POST variables for any of these ajax views
@login_required
@require_POST
def vote_lesson(request):
    lesson_id = request.POST['lesson_id']
    is_up = bool(int(request.POST['is_up']))
    vote_successful = False
    vote_result = None

    try:
        lesson_to_vote = Lesson.objects.get(id=lesson_id)
        existing_vote = LessonVote.objects.filter(lesson=lesson_to_vote, user_profile=request.user)

        if existing_vote:
            existing_vote = existing_vote.get()
            # if this vote is the opposite of an existing vote, delete the existing vote (e.g. down-voting an existing up-vote should just delete the vote all together i.e. neutral)
            if not existing_vote.up == is_up:
                existing_vote.delete()
                vote_result = 'neutral'

        else:
            LessonVote.objects.create(lesson=lesson_to_vote, user_profile=request.user, up=is_up) 

        if not vote_result == 'neutral':
            if is_up:
                vote_result = 'up'
            else:
                vote_result = 'down'

        vote_successful = True

    except ObjectDoesNotExist:
        result_message = 'That lesson does not exist (this is most likely a bug)'  # don't want 404 here because then the front-end will just silently fail since this is responding to an ajax request

    return HttpResponse(json.dumps({'vote_successful' : vote_successful, 'vote_result' : vote_result }), mimetype="application/json")


def browse_courses(request, cat_slug=None, tag_slug=None):
    course_list = None
    filters = None                            
    
    cats = CourseCategory.objects.all()
    tags_by_cat = { cat : Course.tags.filter(course__category=cat) for cat in cats } 

    # default browse page with no filtering
    if not cat_slug and not tag_slug:
        course_list = Course.objects.all().select_related()

    if cat_slug:
        cat = CourseCategory.objects.get(slug=cat_slug) 

        # browse a single category
        if not tag_slug:
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
