from django.test import TestCase  # super important to load TestCase like this! fixtures won't load otherwise
from django.test.client import Client
from bs4 import BeautifulSoup
from django.conf import settings

# for debugging only:
from ipydex import IPS

# run these tests e.g. with `pytest -s --disable-warnings`
# (currently there are some deprecation warnings with lower priority)

settings.TESTMODE = True
settings.TESTMODE = False


class FollowRedirectMixin:

    def follow_redirects(self, url):
        response = self.client.get(url)
        while response.status_code >= 300 and response.status_code < 400:
            url = response['Location']
            response = self.client.get(url)
        return response


class TestCore1(TestCase, FollowRedirectMixin):
    fixtures = ['real_quiz_data.json']

    @classmethod
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get("/quiz/")
        self.assertEqual(response.status_code, 200)

    def test_leagacy_result_tc_id_and_tc_task_id(self):
        response = self.client.get('/quiz/test/result/1/0/')
        self.assertEqual(response.status_code, 404)

    def test_by_tc_id(self):
        response = self.client.get('/quiz/test/1/')
        self.assertEqual(response.status_code, 200)

    def test_leagacy_result_by_task_id(self):
        # test no old url scheme lurking arround
        response = self.client.get('/quiz/result/1/')
        self.assertEqual(response.status_code, 404)

    def test_explicit_by_task_id(self):
        response = self.client.get('/quiz/explicit/12/')
        self.assertEqual(response.status_code, 200)

    def test_gap_fill_text(self):
        rpns = self.client.get('/quiz/explicit/82/')
        self.assertEqual(rpns.status_code, 200)

        form = get_first_form(rpns)
        form_values = {"button_result": [""]}

        # post wrong answer
        post_data = generate_post_data_for_form(form, spec_values=form_values)
        rpns = self.client.post(form.action_url, post_data)

        # post correct answer
        post_data["answer_0:0"] = "ist"
        post_data = generate_post_data_for_form(form, spec_values=form_values)
        rpns = self.client.post(form.action_url, post_data)
        # IPS()

    def test_run_tc(self):

        # get overview page
        rpns = self.follow_redirects('/quiz/test/2')
        self.assertEqual(rpns.status_code, 200)

        form = get_first_form(rpns)

        form_values = {"button_next": [""]}
        post_data = generate_post_data_for_form(form, spec_values=form_values)

        # click on "Start Task Collection"
        rpns = self.client.post(form.action_url, post_data)
        self.assertEqual(rpns.status_code, 200)

        form = get_first_form(rpns)
        form_values = {"button_result": ["Result"]}
        post_data = generate_post_data_for_form(form, spec_values=form_values)
        rpns = self.client.post(form.action_url, post_data)

        # finalize
        form = get_first_form(rpns)
        form_values = {"button_next": ["Next"]}
        post_data = generate_post_data_for_form(form, spec_values=form_values)
        rpns4 = self.client.post(form.action_url, post_data)

        result_tracker = self.client.session["result_tracker"]
        result_data = self.client.session["result_data"]

        import json
        from cryptography.fernet import Fernet
        enc_key = settings.ENCRYPTION_KEY
        crypter = Fernet(enc_key)

        json_bytes = json.dumps(result_tracker).encode("utf8")

        # this worked, until I changed some details how the the ressult data is composed.
        # json_bytes2 = crypter.decrypt(result_data.split("----")[1])
        # self.assertEqual(json_bytes, json_bytes2)

        json_bytes2 = crypter.decrypt(result_data)

        decrypted_data = json.loads(json_bytes2)
        assert isinstance(decrypted_data, dict)
        for k in ["tc", "total", "total_segments"]:
            self.assertEqual(decrypted_data[k], result_tracker[k])



# ----


# helper functions copied from moodpoll
def get_first_form(response):
    """
    Auxiliary function that returns a bs-object of the first form which is specifies by action-url.

    :param response:
    :return:
    """
    bs = BeautifulSoup(response.content, 'html.parser')
    forms = bs.find_all("form")

    form = forms[0]
    form.action_url = form.attrs.get("action")

    return form

def get_form_fields_to_submit(form):
    """
    Return two lists: fields and hidden_fields.

    :param form:
    :return:
    """

    inputs = form.find_all("input")
    textareas = form.find_all("textarea")

    post_fields = inputs + textareas

    types_to_omit = ["submit", "cancel"]

    fields = []
    hidden_fields = []
    for field in post_fields:
        ftype = field.attrs.get("type")
        if ftype in types_to_omit:
            continue

        if ftype == "hidden":
            hidden_fields.append(field)
        else:
            fields.append(field)

    return fields, hidden_fields


def generate_post_data_for_form(form, default_value="xyz", spec_values=None):
    """
    Return a dict containing all dummy-data for the form

    :param form:
    :param default_value:   str; use this value for all not specified fields
    :param spec_values:     dict; use these values to override default value

    :return:                dict of post_data
    """

    if spec_values is None:
        spec_values = {}

    fields, hidden_fields = get_form_fields_to_submit(form)

    post_data = {}
    for f in hidden_fields:
        post_data[f.attrs['name']] = f.attrs['value']

    for f in fields:
        name = f.attrs.get('name')

        if name is None:
            # ignore fields without a name (relevant for dropdown checkbox)
            continue

        if name.startswith("captcha"):
            # special case for captcha fields (assume CAPTCHA_TEST_MODE=True)
            post_data[name] = "passed"
        else:
            post_data[name] = default_value

    post_data.update(spec_values)

    return post_data
