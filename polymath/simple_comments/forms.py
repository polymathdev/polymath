from django import forms
from django.contrib.comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.conf import settings
import datetime
import ipdb

class SimpleCommentForm(CommentForm):
                                       
    # basically copying the method from django.contrib.comments.forms but excluding the 3 unnecessary fields so it doesn't break when they aren't in this form's data
    def get_comment_create_data(self):
        return dict(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk = force_unicode(self.target_object._get_pk_val()),
            comment = self.cleaned_data['comment'],
            submit_date = datetime.datetime.now(),
            site_id = settings.SITE_ID,
            is_public = True,
            is_removed = False,
        )

# in simple_comments, there is no need for the below fields since comments are only for registered users
SimpleCommentForm.base_fields.pop('url')
SimpleCommentForm.base_fields.pop('email')
SimpleCommentForm.base_fields.pop('name')
