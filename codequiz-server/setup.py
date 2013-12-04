from distutils.core import setup

setup(
    name='codequiz-server',
    version='0.1',
    packages=['aux', 'codequiz', 'quiz'],
    package_dir={'': 'codequiz-server'},
    url='',
    license='',
    author='leberwurstsaft',
    author_email='',
    description='', requires=['django, django-taggit, django-taggit-autosuggest', 'IPython']
)
