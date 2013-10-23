codequiz-server
===============

Simple django app for source-code related quizzes


for testing:


python manage.py runserver


--> http://127.0.0.1:8000/

Dependencies:
---

###Django apps
If you don't have these modules already:  

[django-generic-ratings](https://bitbucket.org/frankban/django-generic-ratings)  
[django-jquery](https://bitbucket.org/massimilianoravelli/django-jquery)  
[django-taggit-autosuggest](https://bitbucket.org/fabian/django-taggit-autosuggest)  
[django-feedback](https://github.com/jaredly/django-feedback) (don't use pip for this one, it's included in the repo)  
[Django-MathJax](https://github.com/kaleidos/django-mathjax)  
[django-ace](https://github.com/bradleyayers/django-ace) (also: don't use pip, it's too old, therefore it's included)  

(optional: `pip install ipython`)

To deploy the static files on the production server, you have to set the right path for `STATIC_ROOT` in `codequiz/static_root.py`, then run `python manage.py collectstatic`.
In `settings.py` there is some code that will conditionally load the server specific setting, which should not be in the git repository.

### jQuery and Plugins
[jQuery Star Rating Plugin](http://www.fyneworks.com/jquery/star-rating/#tab-Download)  
You need jQuery + jQueryUI as well  
All of this is already in the repository, or linked from an external source. No need to add anything.
