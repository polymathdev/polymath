from django import forms
from django.forms import ModelForm
from core.models import Course, Lesson, UserProfile
from django.forms.models import BaseModelFormSet
from taggit.forms import TagField
import ipdb


class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ['creator', 'followers']
        widgets = { 
			'name': forms.TextInput(attrs={'placeholder':'Course Name, e.g. "Intro to Python"'}),
			'category': forms.Select(attrs={'initial':'Category'}),
			'description': forms.Textarea(attrs={'placeholder':'Enter a short description of your course here'}),
		}        

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['blurb', 'profile_pic']


class StandaloneLessonForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ['order']
        widgets = { 
			'name': forms.TextInput(attrs={'placeholder':'Lesson Name'}),
            'link': forms.TextInput(attrs={'placeholder':'Lesson URL'}),
			'description': forms.Textarea(attrs={'placeholder':'Describe the link - what\'s this all about?'}),
		}        

    # tags have blank=True in the Lesson model since there are no lesson tags added to lessons when people create a full course right now.  w
    # on individual lesson submissions, tags should be required so we need to redclare this and set the parameter accordingly
    tags = TagField(required=True)


# this should probably be called CourseLessonForm, since it's a form that deals specifically with lessons in courses and not with standalone lessons
class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ['category']
        widgets = {
               'name': forms.TextInput(attrs={'placeholder':'Lesson Name, e.g. "Dive Into Python"'}), 
               'description': forms.Textarea(attrs={'placeholder':'Enter a short description of your lesson here, e.g. "This is a great resource for Python beginners!"'}),
               'link': forms.TextInput(attrs={'placeholder':'Lesson URL, e.g. http://www.diveintopython.org'}),
        }

    # override the init method so that we can make the link fields for existing lessons read-only
    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        
        # is setting required=False even necessary here?
        self.fields['order'].required = False

        # remove 'order' from changed data so that re-ordering a lesson form that is blank to the user doesn't trigger form validation (thus forcing the user to fill out the form)
        try:
            self.changed_data.remove('order')
        except ValueError, e:
            pass

        # if this LessonForm's instance has an id attribute then that means it's an existing object in the database, so set required=False since we aren't letting ppl update the link on lessons (as of this writing, they must be removed)
        # if we didn't set required=False here, the lack of data in the link field on lesson edits will cause the form to be invalid
        if instance and instance.id:
            self.fields['link'].required = False

    def clean_link(self):
        instance = getattr(self, 'instance', None)
        
        # this prevents overwriting existing links on lessons using a LessonForm (as of this writing, we are requiring users to delete existing lessons and make new ones if they want to use a different link in their course)
        if instance and instance.id:
            return instance.link
        # if there is not an instance.id, that means we're trying to validate a form to create a new lesson, so return the cleaned data from the form
        else:
            return self.cleaned_data.get('link', None)

   
    saved_order = 999  # this has the effect of moving unbound lesson forms in the add/edit course pages to the end of the order if the formset is sent back with validation errors.  might change this later.

    # create a custom class attribute for lesson forms so that they can save their order across form validations
    # if the user changes the order on the client-side and submits an invalid form, the new order data won't be saved in the database yet so when the form is sent back with errors, the lessons would show up in their
    # original order if we didn't do this.  the saved_order attribute is used in the OrderedLessonFormSet's overriden __iter__ method below
    def clean_order(self):
        self.saved_order = self.cleaned_data['order']
        return self.saved_order


# i overrode the __iter__ method of the inline formset to display in order of the saved_order attribute i created (see above for explanation on that)
class OrderedLessonFormSet(BaseModelFormSet):
    def __iter__(self):
        # if this formset is bound, it means the user actually changed the form and is trying to submit something, so display in the saved_order because the order fields in the DB may not be updated
        if self.is_bound:
            return iter(sorted(self.forms, key=lambda form: form.saved_order))
        # if the form is not bound, it's blank or it has initial data from the database, so use the default iterator which looks at the ordering attribute in the Meta class of the Lesson model
        else:
            return super(OrderedLessonFormSet, self).__iter__()
