import json
import base64
import time

from django.http import HttpResponse, Http404, HttpResponseForbidden, FileResponse
from django.template import loader
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
import hashlib
from cryptography.fernet import Fernet


from aux import json_lib
from quiz.models import Task, TaskCollection, QuizResult

# for debugging only:
from ipydex import IPS

"""
Some general notes:
tc means task collection
"""


# TODO: this is merely the same as the json_lib.DictContainer without deeprec.
class myContainer(object):
    """
    just a simple data structure for storing objects as attributes
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TC_Finished(ValueError):
    pass


class NotAllowedResponse(HttpResponseForbidden):
    def __init__(self, content=None):
        super(HttpResponseForbidden, self).__init__(content)
        if not content:
            self.content = "You're not allowed to be here."
        else:
            self.content = content


def evaluate_and_render_segment(segment, user_sol_list=None, tc=None):
    """

    :returns:   result ∈ (True, False, None), rendered segment (html string)
    """
    template = loader.get_template(segment.template)
    print_solution = False
    print_feedback = False

    if user_sol_list is not None:
        if tc is not None:
            print_feedback = tc.should_give_feedback()
            print_solution = tc.should_give_solution()
        else:
            # this is not inside a TC, but rather a single task --> show solutions and feedback!
            print_feedback = True
            print_solution = True

        segment.context.update({'print_feedback': print_feedback})
        segment.context.update({'print_solution': print_solution})

        result = segment.update_user_solution(user_sol_list)
        if isinstance(segment, json_lib.QuestionSegment):
            assert result in (True, False)
    else:
        result = None

    return result, template.render(segment.context)


def simple(request, **kwargs):
    """
    Renders a single page with the HTML contents from the kwarg 'template' (html file path)
    """
    text = loader.get_template(kwargs['template']).render(context=None, request=request)
    return render(request, 'tasks/cq0_simple.html', dict(pagecontent=text))


def index(request):
    return simple(request, template="index.html")


def aux_get_task_from_tc_ids(tc_id, tc_task_id=None, next_task=False):
    """
    tc_task_id = None -> first task in this collection
    """

    tc = get_object_or_404(TaskCollection, pk=tc_id)

    if next_task:
        tc_task_id = int(tc_task_id) + 1
    else:
        tc_task_id = int(tc_task_id)

    if tc_task_id >= tc.number_of_tasks():
        raise TC_Finished

    ordered_task_list = tc.ordered_tasks()
    task_id = ordered_task_list[tc_task_id].id
    current_task = aux_get_json_task(task_id)

    current_task.tc_id = tc_id
    current_task.tc_task_id = tc_task_id

    return current_task


def aux_get_json_task(task_id):
    """
    Fetch Task object and preprocess JSON task description into segments
    @task_id {int} ID of task
    """
    db_task = get_object_or_404(Task, pk=task_id)
    json_lib.preprocess_task_from_db(db_task)

    return db_task


def debug_url_landing(request):
    """
    Example function how to emulate formular-processing
    in case just a simple url is opened
    """

    p = dict(request.POST)  # POST itself is immutable
    p['meta_task_id'] = "-1"
    p['meta_no_form'] = True  # indicate that this data is "pseudo"
    request.POST = p

    return render_task(request)


def explicit_task_view(request, task_id):
    """
    this view handles the rendering of a task outside of a TC
    (e.g. in preview mode)
    """
    # TODO: this should be restricted to moderators (session management)

    p = dict(request.POST)  # POST itself is immutable
    p['meta_task_id'] = task_id
    p['meta_no_form'] = True  # indicate that this data is "pseudo"
    request.POST = p

    return render_task(request)


def get_taskcollection_from_post_dict(post_dict):
    """
    This function determines which task collection is referenced in the POST content
    and returns the corresponding object
    """
    tc = None
    if "meta_tc_id" in post_dict:
        tc_id = post_dict["meta_tc_id"]
        if tc_id:
            tc = get_object_or_404(TaskCollection, pk=tc_id)
    return tc


def get_task_to_process(post_dict):
    """
    This function determines which task should be displayed
    and returns the corresponding object
    """

    task_id = post_dict.get('meta_task_id', None)
    tc_id = post_dict.get('meta_tc_id', None)
    tc_task_id = post_dict.get('meta_tc_task_id', None)

    # TODO: simplify!
    if 'meta_no_form' in post_dict:
        task = aux_get_json_task(task_id=task_id)
        return task

    else:
        next_task_flag = False
        solution_flag = False

        if tc_id and not tc_id == 'None':
            # FIXME Somehow the tc_id sometimes is a unicode that says None.
            # FIXME Somewhere this is wrongly being set (in the dict, probably).
            if 'button_next' in post_dict:
                next_task_flag = True

            elif 'button_result' in post_dict:
                solution_flag = True
            else:
                raise Http404("Unknown form content.")

            if int(tc_id) <= 0:
                task = aux_get_json_task(task_id=task_id)
            else:
                task = aux_get_task_from_tc_ids(int(tc_id), tc_task_id, next_task=next_task_flag)
            task.solution_flag = solution_flag

        else:
            if 'button_result' in post_dict:
                task = aux_get_json_task(task_id=task_id)
                task.solution_flag = True

        return task


def template_debug(request):

    if 1:
        return tc_run_final_view(request, tc_id=2, debug=True)

    # fallback
    context_dict = dict()
    return render(request, 'tasks/debug/db_cq0_main_base.html', context_dict)

def render_task(request):
    """

    This function is the main entry point for rendering a task
    all relevant data (task_id, tc_task_id etc) is obtained via request.POST

    """

    post = request.POST
    if len(post) == 0:
        # this happens if the form_process url is opend directly
        return debug_url_landing(request)
    task = get_task_to_process(post)
    tc = get_taskcollection_from_post_dict(post)

    main_block = process_main_block_object(request, task)

    context_dict = dict(main_block=main_block, task=task, tc=tc)

    return render(request, 'tasks/cq0_main_simple.html', context_dict)


def process_main_block_object(request, task):
    """
    :param request:
    :param task: which task to insert
    :return: a container which will be passed to an "include"-template tag

    This function is primarily for testing
    """

    segment_list = task.segment_list

    user_solution = aux_task_user_solution(request, task.solution_flag)


    # build a list of expected solutions, to compare received solutions to
    # and fill the missing ones with empty strings
    # TODO: This block seems obsolete
    if user_solution is not None:
        expected_solutions = list(range(0, len(segment_list)))

        missing_solutions = []
        for sol in expected_solutions:
            if str(sol) not in user_solution:
                missing_solutions.append((str(sol), ""))
        user_solution.update(dict(missing_solutions))

    button_list = []

    try:
        tc_id = task.tc_id
    except AttributeError as err:
        tc_id = None

    if tc_id:
        tc = get_object_or_404(TaskCollection, pk=tc_id)

        if tc.should_give_feedback():
            button_list.append("result")

        if task.solution_flag or not tc.should_give_feedback():
            button_list.append("next")

    else:
        tc = None
        button_list.append("result")  # this only occurs in explicit mode

    button_strings = aux_task_button_strings(button_list)

    html_strings = []
    result_list = []
    for segment in filter_segment_list(segment_list, tc, task.solution_flag):
        result, html_str = evaluate_and_render_segment(segment, user_solution, tc)
        result_list.append(result)
        html_strings.append(html_str)

    res = myContainer(
        task=task, button_strings=button_strings, html_strings=html_strings, result_list=result_list
    )
    IPS(settings.TESTMODE)

    res.debug_flag = True
    res.tc_id = ""
    res.tc_task_id = ""

    return res


def filter_segment_list(segment_list, tc, solution_flag):
    if tc:
        should_show_comments = tc.should_give_feedback()
    else:
        should_show_comments = True

    if should_show_comments and solution_flag:
        return segment_list
    else:
        return [s for s in segment_list if not (hasattr(s, "c_comment") and s.c_comment)]


def get_button(button_type):
    #!! loaded every time!!
    button_template = loader.get_template('tasks/task_buttons1.html')
    button_ctxt_dict = {'button_type': button_type}

    return button_template.render(button_ctxt_dict)


def get_solutions_from_post(request):
    items = list(request.POST.items())
    items.sort()

    transformed_items = [(k.split("_")[1], v) for k, v in items if k.startswith("answer")]
    return dict(transformed_items)


def aux_task_button_strings(button_list):
    button_strings = [get_button(t) for t in button_list]
    return button_strings


def aux_task_user_solution(request, solution_flag):
    if not solution_flag:
        user_solution = None
    else:
        user_solution = get_solutions_from_post(request)

    return user_solution

# FIXME: remove
def tc_run_form_process(request, tc_id, tc_task_id):
    1/0
    post = request.POST
    if 'next' in post:
        next_id = "%i" % (int(tc_task_id) + 1)
        return tc_run_view(request, tc_id, next_id, solution_flag=False)  # FIXME Verify this method is used at all
                                                                          # FIXME Number of arguments isn't valid here

    elif 'result' in post:
        return tc_run_view(request, tc_id, tc_task_id, solution_flag=True) # FIXME same problem as above --^

    else:
        return redirect('quiz_ns:index', )


def tc_run_final_view(request, tc_id, debug=None):
    tc = get_object_or_404(TaskCollection, pk=tc_id)

    if debug:
        request.session.update(
            {
                'meta_tc_id': '2',
                'tc_id': 2,
                'tc_task_id': 0

            }
        )

    response = HttpResponse()

    # TODO: better error handling
    if "tc_task_id" not in request.session:
        response.write("<p>You haven't even started the quiz yet.</p>")
        return response

    # TODO: better error handling
    if "tc_id" in request.session:
        if int(tc_id) != request.session["tc_id"]:
            response.write("<p>You can't switch task collections on your own.</p>")
            return response

    # TODO: better error handling
    tc_task_id = request.session["tc_task_id"]
    if tc_task_id < tc.number_of_tasks() - 1:
        response.write("<p>You're not done with the quiz yet.</p>")
        return response

    log = ""
    if "log" in request.session:
        log = request.session["log"]
    log += "Show final page."

    result_tracker = request.session.get("result_tracker", {})
    _finalize_result_tracker(result_tracker, tc)
    request.session["result_tracker"] = result_tracker

    # request.session.clear()

    current_date = datetime.now()
    date_iso8601 = current_date.isoformat(" ")
    hash_string = compute_hash(log, date_iso8601)

    quiz_result = QuizResult()
    quiz_result.date = current_date
    quiz_result.hash = hash_string
    quiz_result.log = log
    quiz_result.result_data = json.dumps(result_tracker).encode("utf8")
    quiz_result.save()

    result_data = _generate_result_data(result_tracker)
    quiz_result.save()

    context_dict = dict(tc=tc)
    context_dict["hash"] = hash_string
    context_dict["result_data"] = result_data
    context_dict["percentage"] = round(result_tracker["total"] *100)
    context_dict["percentage_segments"] = round(result_tracker["total_segments"] *100)

    # this is for unit_testing
    request.session["result_data"] = result_data

    return render(request, 'tasks/tc_run_final.html', context_dict)


def _finalize_result_tracker(result_tracker, tc):


    overall_segment_res = 0
    overall_task_res = 0
    tasks = 0
    for key, value in result_tracker.items():
        try:
            k = int(key)
        except ValueError:
            # if a key is not an stringified integer
            continue

        # value contains the fraction of correct answer-segments
        # here we want to count only fully correct tasks
        if value >= 1:
            overall_task_res += 1

        overall_segment_res += value
        tasks += 1

    result_tracker["tc"] = (tc.id, tc.title)
    if tasks > 0:
        result_tracker["total"] = overall_task_res/tasks
        result_tracker["total_segments"] = overall_segment_res/tasks
    else:
        # there where no tasks with solutions
        result_tracker["total"] = 0
        result_tracker["total_segments"] = 0


def _generate_result_data(result_tracker, colwidth=60):
    """
    :param result_tracker:    dict
    :param colwidth:          columnwidth of the resulting string

    convert the result_tracker dict into an encrypted base64 str.
    """

    assert isinstance(result_tracker, dict)
    assert isinstance(colwidth, int) and 0 < colwidth

    enc_key = settings.ENCRYPTION_KEY

    json_bytes = json.dumps(result_tracker).encode("utf8")
    crypter = Fernet(enc_key)
    c_bytes = crypter.encrypt(json_bytes)

    meta_data = {
        "ts": time.strftime(r"%Y-%m-%d %H:%M:%S"),
        "txt": base64.b64decode(
            b"SWYgeW91IHJlYWQgdGhpcywgeW91IHNob3VsZCBjb25zaWRlciBjb250cmlidXRpbmcgdG8gdGh"
            b"lIHByb2plY3QgKGFuZCBub3QgdHJ5aW5nIHRvIG1hbmlwdWxhdGUgcmVzdWx0cyA7KSku"
        ).decode("utf8")
    }

    meta_data_bytes = base64.b64encode(json.dumps(meta_data).encode("utf8"))

    SEP = b"----"
    all_bytes = meta_data_bytes + SEP + c_bytes

    blocks = []
    i = 0
    while i*colwidth < len(all_bytes):

        blocks.append(all_bytes[i*colwidth:(i+1)*colwidth])
        i += 1

    res = b"\n".join(blocks).decode("utf8")
    return res


def compute_hash(string, date):
    byte_string = (string + date).encode("utf8")
    result = hashlib.sha256(byte_string).hexdigest()
    return result

# TODO: rename to task_result_view
def tc_run_view(request):
    """
    Here we land after clicking on 'Result'
    """
    post_dict = request.POST

    if len(post_dict) <= 0:
        if "tc_id" in request.session and "tc_task_id" in request.session:

            meta_tc_id = request.session['tc_id']
            meta_tc_task_id = request.session['tc_task_id']

            if meta_tc_id is None or meta_tc_task_id is None:
                return redirect('quiz_ns:index', )
            else:
                post_dict = {
                    'button_next': '',
                    'meta_tc_id': int(meta_tc_id),
                    'meta_tc_task_id': int(meta_tc_task_id) - 1
                }

        else:
            return redirect('quiz_ns:index', )

    try:
        task = get_task_to_process(post_dict)
    except TC_Finished:
        tc_id = request.POST['meta_tc_id']
        return tc_run_final_view(request, tc_id)

    tc_id = getattr(task, "tc_id", None)
    tc_task_id = getattr(task, "tc_task_id", None)

    request.session['tc_id'] = tc_id
    request.session['tc_task_id'] = tc_task_id

    log = ""
    if 'log' in request.session:
        log = request.session['log']

    log += "Show {solution} task {task} of collection {coll}.\n".format(
        solution="solution of" if task.solution_flag else "",
        task=str(tc_task_id),
        coll=str(tc_id)
    )
    request.session["log"] = log

    result_tracker = request.session.get("result_tracker", {})

    main_block = process_main_block_object(request, task)
    main_block.tc_run_flag = True  # trigger the correct url in the template
    main_block.tc_id = tc_id
    main_block.tc_task_id = tc_task_id

    _track_result(task, main_block.result_list, target_dict=result_tracker)
    request.session["result_tracker"] = result_tracker

    tc = None if not tc_id else get_object_or_404(TaskCollection, pk=tc_id)

    context_dict = dict(main_block=main_block, task=task, tc=tc)

    IPS(settings.TESTMODE)

    return render(request, 'tasks/cq0_main_simple.html', context_dict)


def _track_result(task, result_list, target_dict):

    if not task.solution_flag:
        res = {}
    else:
        filtered_result_list = [res for res in result_list if res in (True, False)]

        length = len(filtered_result_list)
        if length == 0:
            # there is nothing to solve here. this might occurr for informational "tasks"
            # do not change the dict
            return
        else:
            true_share = filtered_result_list.count(True)/length

        res = {task.id: true_share}

    target_dict.update(res)


def task_collection_view(request, tc_id):
    tc = get_object_or_404(TaskCollection, pk=tc_id)
    tasks = tc.ordered_tasks()

    # temporary hack to reset quiz progress
    if "tc_task_id" in request.session:
        del request.session["tc_task_id"]

    # ensure that the result tracker is empty when starting a new task collection
    request.session["result_tracker"] = {}

    log = ""
    if "log" in request.session:
        log = request.session["log"]
    log += "--- Reset session to allow a new quiz. ---\n"
    request.session["log"] = log

    context_dict = dict(task_list=tasks, tc=tc)

    #post_dict = dict(request.POST)
    request.session['meta_tc_id'] = str(tc_id)

    return render(request, 'tasks/task_collection.html', context_dict)


@staff_member_required
def download_backup_fixtures(request):
    import io
    import time
    from . import auxiliary as auxi

    data_bytes = auxi.make_backup()
    stream = io.BytesIO(data_bytes)
    # open the file and create a FileResponse containing the file's contents

    time_str =time.strftime("%Y-%m-%d__%H-%M-%S")
    dev_mode_str = "_DEV" if settings.DEVMODE else "_PRODUCTION"

    fname = f"{time_str}_codequiz_backup_all{dev_mode_str}.json"

    response = FileResponse(stream, content_type='application/json')

    # set the Content-Disposition header to force the browser to download the file
    response['Content-Disposition'] = f'attachment; filename="{fname}"'

    return response
