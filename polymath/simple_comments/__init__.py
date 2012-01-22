from simple_comments.forms import SimpleCommentForm

# tells django to use the simple_comments form instead of the stock comments form
def get_form():
    return SimpleCommentForm
