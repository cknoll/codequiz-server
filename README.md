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

    pip install django-generic-ratings
    pip install django-jquery
    pip install django-taggit-autosuggest

(optional: `pip install ipython`)

To deploy the static files you have to set the right path for `STATIC_ROOT` in `codequiz/settings.py`, then run `python manage.py collectstatic`.

### jQuery and Plugins
[jQuery Star Rating Plugin](http://www.fyneworks.com/jquery/star-rating/#tab-Download)  
You need jQuery + jQueryUI as well  
All of this is already in the repository, or linked from an external source. No need to add anything.
