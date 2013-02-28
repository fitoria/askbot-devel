from django import forms
from django.utils import safestring

class ImageInput(forms.FileInput):

    def __init__(self, *args, **kwargs):
        """ImageInput.__init__ function takes
        an optional parameter url_resolver
        which must be a callable accepting one argument - the url
        or url key
        url_resolver must return a valid image url

        if not given or None, the resolver will be a dummy
        fuction returning an unchanged value
        """
        self.url_resolver = kwargs.pop('url_resolver', lambda val: val)
        super(ImageInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs = None):
        output = '<img '
        if attrs and 'image_class' in attrs:
            output += 'class="%s" ' % attrs['image_class']
        output += 'src="%s"/><br/>' % self.url_resolver(value)
        output += super(ImageInput, self).render(name, value, attrs)
        return safestring.mark_safe(output)

class FileInput(forms.FileInput):

    def render(self, name, value, attrs = None):
        if value:
            output = 'Currently: <strong>%s</strong> <br/>' % value
        else:
            output = 'Currently: <strong>None Selected</strong> <br/>'
        output += super(FileInput, self).render(name, value, attrs)
        return safestring.mark_safe(output)
