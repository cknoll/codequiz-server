from django.forms import Textarea

class BuilderTextArea(Textarea):

    def __init__(self, attrs=None):
        default_attrs = {'class': 'builder'}
        if attrs is None:
            attrs = default_attrs 
        attrs.update(default_attrs)
        super(BuilderTextArea, self).__init__(attrs)

    class Media:
        css = {
            'all': (
                'builder/style.css',
                'http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css',
                'http://netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css'
            )
        }
        js = (
            'builder/dynamic.js',
            'http://code.jquery.com/jquery-1.9.1.js',
            'http://code.jquery.com/ui/1.10.3/jquery-ui.js'
        )
