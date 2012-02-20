from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from core.models import Course, Lesson, CourseCategory, LessonCompletion, LessonVote
from taggit.models import Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.forms import CourseForm, LessonForm, OrderedLessonFormSet, ProfileForm, StandaloneLessonForm
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
    # fb_data = request.user.social_auth.get(provider='facebook').extra_data
    # access_token = fb_data['access_token']
    # fb_uid = fb_data['id']
    # fb = GraphAPI(access_token)
    # pic = fb.get('fql',q='select pic_big from user where uid='+fb_uid)

    return render(request, 'howitworks.dtl', {} )

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

def home_page(request):
    default_course = Course.objects.all()[0]

    # there has to be a more elegant way to accomplish the below
    if Course.objects.filter(homepage_featured='A').count() > 0:
        left = Course.objects.filter(homepage_featured='A')[0]
    else:
        left = default_course

    if Course.objects.filter(homepage_featured='B').count() > 0:
        middle = Course.objects.filter(homepage_featured='B')[0]
    else:
        middle = default_course

    if Course.objects.filter(homepage_featured='C').count() > 0:
        right = Course.objects.filter(homepage_featured='C')[0]
    else:
        right = default_course

    return render(request, 'home_page.dtl', {
        'featured_courses' : {
            'left' : left,
            'middle' : middle,
            'right' : right
            }        
        })

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
    upvoted_lessons = LessonVote.objects.filter(user_profile=profile_owner).select_related('course')
    
    # courses_following = profile_owner.courses_following.select_related('category').all()

    # lessons_following = Lesson.objects.filter(course__in=courses_following)
    # lessons_following_completed = Lesson.objects.filter(course__in=courses_following, completers=profile_owner)  

    # lessons = { les['id'] : les for les in lessons_following.values() }
    # completed_lessons = { les['id'] : les for les in lessons_following_completed.values() }

    # courses_following_with_progress = { c['id'] : c for c in courses_following.values() }

    # for c in courses_following:
    #     courses_following_with_progress[c.id]['category_id'] = c.category.id
    #     courses_following_with_progress[c.id]['category'] = c.category.name

    # course_progress = { c.id : { 'total' : 0, 'completed' : 0 } for c in courses_following } 

    # for les_id, les in lessons.iteritems():
    #     course_progress[les['course_id']]['total'] = course_progress[les['course_id']]['total'] + 1

    #     if completed_lessons.has_key(les_id):
    #         course_progress[les['course_id']]['completed'] = course_progress[les['course_id']]['completed'] + 1 
    # 
    # for c_id, c in courses_following_with_progress.iteritems():
    #    c['total'] = course_progress.get(c_id, 0)['total']
    #    c['completed'] = course_progress.get(c_id, 0)['completed']

    # courses_following = courses_following_with_progress.values()

    return render_to_response('view_profile.dtl', {
    'profile_owner': profile_owner,
	'user_blurb': user_blurb,
    'courses_created_by_user': courses_created_by_user,
    # 'courses_following': courses_following,
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
    show_course_message = None

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
    
    # i.e. not logged in - determine if course message should be displayed
    else:
        # should have more organized session handling for this kind of stuff down the road but this is fine for now
        if not request.session.get('has_seen_course_msg', False):
            show_course_message = True
            request.session['has_seen_course_msg'] = True

    return render_to_response('view_course.dtl',  {
        'show_course_message' : show_course_message,
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

# can we accomplish this exact same thing with one of Django's generic views?
@login_required
def add_lesson(request):
    # errors that we'll handle manually so we can manipulate the error message as opposed to having the ModelForm handle it automatically
    extra_errors = {} 

    if request.method == 'POST':
        lesson_form = StandaloneLessonForm(request.POST)

        if lesson_form.is_valid():
            new_lesson = lesson_form.save(commit=False)
            new_lesson.creator = request.user
            new_lesson.save()

            # save tags
            lesson_form.save_m2m()

            messages.success(request, 'Your lesson has been submitted! Share it with your friends on Twitter and Facebook.')
            return redirect('browse_all')
    
        # handling if lesson_form is not valid.  normally this is handled automatically by django passing errors to template, but in this case we have a special error we want to manually handle here
        else:
            # this whole thing kind of feels like a bit of a hack - maybe there's a better way to do this
            if lesson_form.errors.has_key('__all__'):
                all_error_msg = str(lesson_form.errors.get('__all__')[0]) 
            
                if all_error_msg.startswith('StandaloneDuplicate'):
                    extra_errors['duplicate_lesson_pk'] = int(all_error_msg.split('::')[1])
            
    # if this is not a POST request
    else:
        lesson_form = StandaloneLessonForm()

    return render(request, 'submitlesson.dtl', {
        'lesson_form': lesson_form,
        'extra_errors': extra_errors
        })

@login_required
def add_course(request):
    LessonFormSet = modelformset_factory(Lesson, form=LessonForm)                                   

    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        lesson_fs = LessonFormSet(request.POST)     
        
        if course_form.is_valid() and lesson_fs.is_valid():
            new_course = course_form.save(commit=False)
            new_course.creator = request.user
            new_course.save()

            # save tags
            course_form.save_m2m()

            lesson_fs.save(commit=False)

            # add the M2M relationship from each lesson to the new course after the lessons are created with lesson_fs.save() above
            # does this hit the database a separate time for each lesson?  is there a way to avoid that?
            # also add category to match course's category - this may be temporary but for now we'll associate every lesson object with a category
            for lesson_form in lesson_fs.forms:
                lesson_form.instance.category = new_course.category
                lesson_form.instance.save()
                lesson_form.instance.course = [new_course] 

            messages.success(request, 'Your course has been created! Share it with your friends on Twitter and Facebook.')
            return redirect('view_my_profile')

    else:
        course_form = CourseForm()            
        lesson_fs = LessonFormSet(queryset=Lesson.objects.none())
        
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
    
    EditLessonFormSet = modelformset_factory(Lesson, form=LessonForm, formset=OrderedLessonFormSet)                                    
    
    if request.method == 'POST':
        
        edit_course_form = CourseForm(request.POST, request.FILES, instance=course_to_edit)
        edit_lesson_fs = EditLessonFormSet(request.POST, queryset=course_to_edit.lesson_set.all()) 

        if edit_course_form.is_valid() and edit_lesson_fs.is_valid():
            edit_course_form.save() 

            edit_lesson_fs.save(commit=False)
            
            # create relations between new lessons and this course (is this querying the database for overwriting the FK relation on existing courses?  check this later, if so that is inefficient)
            # need to examine how many queries are run as a result of all this...
            for lesson_form in edit_lesson_fs.forms:
                # there is probably a better way to do this, but i'm just trying to ignore blank forms.  for some reason is_valid() is returning true on them so i can't check that...
                if lesson_form.saved_order <> 999:
                    lesson_form.instance.category = course_to_edit.category
                    lesson_form.instance.save()
                    lesson_form.instance.course = [course_to_edit]

            messages.success(request, 'Your changes have been saved!')
            return redirect('view_course', course_id=course_id, course_slug=course_to_edit.slug) 
        
    else:
        edit_course_form = CourseForm(instance=course_to_edit)
        edit_lesson_fs = EditLessonFormSet(queryset=course_to_edit.lesson_set.all())
    
    return render_to_response('add_course2.dtl', {
		'requested_course': course_to_edit,
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


def browse(request, cat_slug=None, tag_slug=None):
    course_list = None
    standalone_lessons = None
    filters = {}                            
    
    cats = CourseCategory.objects.all()
    # tags_by_cat shouldn't work as expected right now given that we have standalone lessons with tags...
    tags_by_cat = { cat : Course.tags.filter(course__category=cat) for cat in cats } 

    # create course/standalone-lesson querysets which we'll filter later based on cat or tag criteria if necessary.
    # since querysets are lazy we should only be hitting the database a single tine once they are looped through in the template
    course_list = Course.objects.all()
    standalone_lessons = Lesson.objects.filter(course=None)

    if cat_slug:
        cat = get_object_or_404(CourseCategory, slug=cat_slug)  
        course_list = course_list.filter(category=cat)
        standalone_lessons = standalone_lessons.filter(category=cat)
        filters['cat'] = cat

    if tag_slug:
        course_list = course_list.filter(tags__slug=tag_slug)
        standalone_lessons = standalone_lessons.filter(tags__slug=tag_slug)
        filters['tag'] = Tag.objects.get(slug=tag_slug)

    return render(request, 'browse_courses.dtl', {
        'tags_by_cat' : tags_by_cat,
        'course_list' : course_list,
        'standalone_lessons' : standalone_lessons,
        'filters' : filters
        })


def view_lesson(request, lesson_id, lesson_slug=None):
    requested_lesson = get_object_or_404(Lesson, pk=lesson_id, course=None) 

    # redirect to appropriate URL with complete slug if necessary (this is a cosmetic thing)
    if lesson_slug != requested_lesson.slug:
        return redirect('view_lesson', permanent=True, lesson_id=lesson_id, lesson_slug=requested_lesson.slug)

    return render(request, 'view_lesson.dtl', {
        'lesson' : requested_lesson,
        'next' : reverse('view_lesson', kwargs={'lesson_id':lesson_id,'lesson_slug':lesson_slug}),
        'to_client': json.dumps({'complete_lesson_url': reverse('complete_lesson'), 'vote_lesson_url' : reverse('vote_lesson')}) 
        })
