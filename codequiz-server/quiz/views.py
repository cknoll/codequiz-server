# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from datetime import *
import hashlib

from IPython import embed as IPS

from aux import xml_lib, json_lib
from quiz.models import Task, TaskCollection, QuizResult


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


def render_segment(segment, user_sol_list=None, tc=None):
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

        if not isinstance(segment, json_lib.GapText):
            segment.update_user_solution(user_sol_list)

    return template.render(Context(segment.context))


def simple(request, **kwargs):
    """
    Renders a single page with the HTML contents from the kwarg 'template' (html file path)
    """
    text = loader.get_template(kwargs['template']).render(RequestContext(request))
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
    in case just a simple url is opend
    """

    p = dict(request.POST)  # POST itself is immutable
    p['meta_task_id'] = "12"
    p['meta_no_form'] = True  # indicate that this data is "pseudo"
    request.POST = p

    return debug_task_process(request)


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

    return debug_task_process(request)


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

        if tc_id and not tc_id == u'None':  # FIXME Somehow the tc_id sometimes is a unicode that says None.
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


def debug_task_process(request):
    """
    # currently this docstring describes the situation we want

    This function is the main entry point for rendering a task
    all relevant data (task_id, tc_task_id etc) is obtained via request.POST

    """

    post = request.POST
    if len(post) == 0:
        # this happens if the form_process url is opend directly
        return debug_url_landing(request)
    task = get_task_to_process(post)
    tc = get_taskcollection_from_post_dict(post)

    main_block = debug_main_block_object(request, task)

    context_dict = dict(main_block=main_block, task=task, tc=tc)

    context = Context(context_dict)

    return render(request, 'tasks/cq0_main_simple.html', context)


def debug_main_block_object(request, task):
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
    if user_solution is not None:
        expected_solutions = []
        question_index = 0

        for segment in segment_list:
            expected_solutions.append(question_index)
            question_index += 1
        user_solution_keys = user_solution.keys()
        missing_solutions = []
        for sol in expected_solutions:
            if sol not in user_solution:
                missing_solutions.append((sol, ""))
        user_solution.update(dict(missing_solutions))

    button_list = []

    try:
        tc_id = task.tc_id
    except AttributeError, err:
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
    html_strings = [render_segment(segment, user_solution, tc) for segment in
                    filter_segment_list(segment_list, tc, task.solution_flag)]

    res = myContainer(task=task, button_strings=button_strings, html_strings=html_strings)

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
        return filter(lambda s: not (hasattr(s, "c_comment") and s.c_comment), segment_list)


def get_button(button_type):
    #!! loaded every time!!
    button_template = loader.get_template('tasks/task_buttons1.html')
    bContext = Context({
        'button_type': button_type, })

    #!!++
    return button_template.render(bContext)


def get_solutions_from_post(request):
    items = request.POST.items()
    items.sort()

    transformed_items = [(int(k.split("_")[1]), v) for k, v in items if k.startswith("answer")]

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


def tc_run_form_process(request, tc_id, tc_task_id):
    post = request.POST
    if 'next' in post:
        next_id = u"%i" % (int(tc_task_id) + 1)
        return tc_run_view(request, tc_id, next_id, solution_flag=False)

    elif 'result' in post:
        return tc_run_view(request, tc_id, tc_task_id, solution_flag=True)

    else:
        return redirect('quiz_ns:index', )


def tc_run_final_view(request, tc_id):
    tc = get_object_or_404(TaskCollection, pk=tc_id)

    response = HttpResponse()

    if "tc_task_id" not in request.session:
        response.write("<p>You haven't even started the quiz yet.</p>")
        return response

    if "tc_id" in request.session:
        if int(tc_id) != request.session["tc_id"]:
            response.write("<p>You can't switch task collections on your own.</p>")
            return response

    tc_task_id = request.session["tc_task_id"]
    if tc_task_id < tc.number_of_tasks() - 1:
        response.write("<p>You're not done with the quiz yet.</p>")
        return response

    log = ""
    if "log" in request.session:
        log = request.session["log"]
    log += "Show final page."

    request.session.clear()

    current_date = datetime.now()
    date_iso8601 = current_date.isoformat(" ")
    hash_string = compute_hash(log, date_iso8601)

    quiz_result = QuizResult()
    quiz_result.date = current_date
    quiz_result.hash = hash_string
    quiz_result.log = log
    quiz_result.save()

    context_dict = dict(tc=tc)
    context_dict["hash"] = hash_string
    context = Context(context_dict)

    return render(request, 'tasks/tc_run_final.html', context)


def compute_hash(string, date):
    result = hashlib.sha256(string + date).hexdigest()
    return result


def tc_run_view(request):
    """

    """
    post_dict = request.POST

    if len(post_dict) <= 0:
        if request.session.has_key("tc_id") and request.session.has_key("tc_task_id"):

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

    main_block = debug_main_block_object(request, task)
    main_block.tc_run_flag = True  # trigger the correct url in the template
    main_block.tc_id = tc_id
    main_block.tc_task_id = tc_task_id

    tc = None if not tc_id else get_object_or_404(TaskCollection, pk=tc_id)

    context_dict = dict(main_block=main_block, task=task, tc=tc)
    context = Context(context_dict)

    return render(request, 'tasks/cq0_main_simple.html', context)


def task_collection_view(request, tc_id):
    tc = get_object_or_404(TaskCollection, pk=tc_id)
    tasks = tc.tasks.iterator()

    # temporary hack to reset quiz progress
    if "tc_task_id" in request.session:
        del request.session["tc_task_id"]

    log = ""
    if "log" in request.session:
        log = request.session["log"]
    log += "--- Reset session to allow a new quiz. ---\n"
    request.session["log"] = log

    context_dict = dict(task_list=tasks, tc=tc)
    context = Context(context_dict)

    #post_dict = dict(request.POST)
    request.session['meta_tc_id'] = unicode(tc_id)

    return render(request, 'tasks/task_collection.html', context)
