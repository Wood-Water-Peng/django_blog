import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
import django

django.setup()

from rango.models import Category


def remove_cat(cat):
    c = Category.objects.get(name=cat)
    if c:
        print ("remove---" + str(c))
        c.delete()


def remove():
    remove_cat('Test')
    remove_cat('Other Frameworks')


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango remove script..."
    remove()
