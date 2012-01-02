from django.db.models.loading import get_models


print "hello world!!"

for m in get_models():
    print "loading %s from %s" % (m.__module__, m.__name__)
    exec "from %s import %s" % (m.__module__, m.__name__)
