# codequiz-server

Django app for source-code related quizzes


## Local test deployment

- clone the repo
- `pip install -r requirements.txt`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py loaddata codequiz-server/apps/quiz/fixtures/real_quiz_data.json`
- `python manage.py runserver`
- open <http://localhost:8000/>
- go to <http://localhost:8000/admin/> to create, delete or edit tasks




## Remote deployment


The following instructions are taylored towards [uberspace](https://uberspace.de)

- copy `<BASEDIR>/deployment/config-exampl.ini` to `<BASEDIR>/config.ini`
- change that file (insert your connection data etc.)
- review `deployment/deploy.py` to understand what happens
- run `pip install -r deployment/deployment_requirements.txt`
- run `python deployment/deploy.py` from `<BASEDIR>/`

