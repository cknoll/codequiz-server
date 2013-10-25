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
                'jquery/smoothness/jquery-ui.css',
                'font-awesome/css/font-awesome.min.css'
            )
        }
        js = (
            'jquery/jquery-1.10.2.min.js',
            'jquery/jquery-ui-1.10.3.custom.min.js',
            'ace/ace.js',
            'ace/require.js',
            'builder/aced.js',
            'builder/dynamic.js'
        )
