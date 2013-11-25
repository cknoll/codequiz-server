# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
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


def render_segment(segment, user_sol_list=None):
    template = loader.get_template(segment.template)
    if user_sol_list is None:
        segment.context.update({'print_solution': False})
    else:
        segment.context.update({'print_solution': True})
        segment.update_user_solution(user_sol_list)

    return template.render(Context(segment.context))


def simple(request, **kwargs):
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

    ordered_task_list = tc.tc_membership_set.order_by('ordering')
    tc.len = len(ordered_task_list)


    # TODO: prevent confusion with 1 (database) and 0 (list) as first index
    if tc_task_id > len(ordered_task_list):
        raise TC_Finished

    current_task = ordered_task_list[tc_task_id - 1].task

    # TODO: redundance with aux_get_json_task??
    json_lib.preprocess_task_from_db(current_task)
    current_task.tc_id = tc_id
    current_task.tc_task_id = tc_task_id

    return current_task


def aux_get_json_task(task_id):
    """
    currently returns pseudo stuff if the body starts with xml
    """
    db_task = get_object_or_404(Task, pk=task_id)
    json_lib.preprocess_task_from_db(db_task)

    return db_task


def debug_url_landing(request):
    """
    Example function how to emulate formular-processing
    in case just a simple url is opend
    """

    p = dict(request.POST) # POST itself is immutable
    p['meta_task_id'] = "12"
    p['meta_no_form'] = True # indicate that this data is "pseudo"
    request.POST = p

    return debug_task_process(request)


def debug_explicit_task_view(request, task_id):
    """
    this view handles the rendering of a task outside of a TC
    (e.g. in preview mode)
    """
    # TODO: this should be restricted to moderators (session management)

    p = dict(request.POST) # POST itself is immutable
    p['meta_task_id'] = task_id
    p['meta_no_form'] = True # indicate that this data is "pseudo"
    request.POST = p

    return debug_task_process(request)


def get_task_to_process(post_dict):
    """
    This function determines which task should be displayed
    and returns the corresponding object
    """

    task_id = post_dict.get('meta_task_id', None)
    # TODO: simplify!
    if 'meta_no_form' in post_dict:
        task = aux_get_json_task(task_id=task_id)
        return task

    elif 'button_next' in post_dict:
        if post_dict.get('meta_tc_id', "") != "":
            tc_id = post_dict['meta_tc_id']
            tc_task_id = post_dict['meta_tc_task_id']
            task = aux_get_task_from_tc_ids(tc_id, tc_task_id, next_task=True)
            task.solution_flag = False
        else:
            raise Http404("For explictly adressed tasks, there is no successor!")
            #aux_get_json_task(task_id=task_id, next_task=True)
        return task

    elif 'button_result' in post_dict:
        if post_dict.get('meta_tc_id', "") != "":
            tc_id = post_dict['meta_tc_id']
            tc_task_id = post_dict['meta_tc_task_id']
            task = aux_get_task_from_tc_ids(tc_id, tc_task_id)
        else:
            # this is for the explicit mode
            task = aux_get_json_task(task_id=task_id)
        task.solution_flag = True

        return task
    else:
        raise Http404("Unknown formular content.")


def debug_task_process(request):
    """
    # currently this docstring describes the striven situation

    This function is the main entry point for rendering a task
    all relevant data (task_id, tc_task_id etc) is obtained via request.POST

    """

    post = request.POST
    if len(post) == 0:
        # this happens if the form_process url is opend directly
        return debug_url_landing(request)
    task = get_task_to_process(post)

    main_block = debug_main_block_object(request, task)
    #tmb = task_meta_block(request, task)

    context_dict = dict(main_block=main_block, task=task)

    # currently not really clear whats the difference between Context-Object
    # and dict ... anyway
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

        print("missing", missing_solutions)
        print("all", user_solution)


    if task.solution_flag:
        button_list = ['result', 'next']
    else:
        button_list = ['result']

    button_strings = aux_task_button_strings(button_list)
    html_strings = [render_segment(segment, user_solution) for segment in segment_list]

    res = myContainer(task=task, button_strings=button_strings,
                      html_strings=html_strings)

    res.debug_flag = True
    res.tc_id = ""
    res.tc_task_id = ""

    return res


def debug1(request, tc_id=None, tc_task_id=None):
    task = aux_get_json_task(task_id=12) # 12 is the test-json-task

    main_block = debug_main_block_object(request, task)

    # say to the template that we are in debug (i.e. testing) mode



    context_dict = dict(main_block=main_block)

    # currently not really clear whats the difference between Context-Object
    # and dict ... anyway
    context = Context(context_dict)

    return render(request, 'tasks/cq0_main_simple.html', context)


def get_button(button_type):
    #!! loaded every time!!
    button_template = loader.get_template('tasks/task_buttons1.html')
    bContext = Context({
        'button_type': button_type, })

    #!!++
    return button_template.render(bContext)


def aux_get_segment_list_from_task(task):
    """
    returns list of segments
    """
    root = xml_lib.load_xml(task.body_data)

    segments = xml_lib.split_xml_root(root)

    return segments


def get_solutions_from_post(request):
    # TODO: this function probably could be simplified
    items = request.POST.items()
    items.sort()

    print("items", items)

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


def next_task(request, task_id):
    """
    returns the next task in current test
    """
    new_id = str(int(task_id) + 1)
    return task_view(request, new_id)


def form_result_view(request, task_id):
    post = request.POST
    1 / 0 # deprecated
    if 'next' in post:
        return next_task(request, task_id)
    elif 'result' in post:
        return task_view(request, task_id, solution_flag=True)
    else:
        # this should not happen
        return task_view(request, task_id)


def tc_run_form_process(request, tc_id, tc_task_id):
    post = request.POST
    if 'next' in post:
        next_id = u"%i" % ( int(tc_task_id) + 1)
        return tc_run_view(request, tc_id, next_id, solution_flag=False)

    elif 'result' in post:
        return tc_run_view(request, tc_id, tc_task_id, solution_flag=True)

# is also used by new (json) workfolw
def tc_run_final_view(request, tc_id):
    tc = get_object_or_404(TaskCollection, pk=tc_id)

    response = HttpResponse()

    if "tc_task_id" not in request.session:
        response.write("<p>You haven't even started the quiz yet.</p>")
        return response

    if "tc_id" in request.session:
        if tc_id != request.session["tc_id"]:
            response.write("<p>You can't switch task collections on your own.</p>")
            return response

    task_list = tc.tc_membership_set.order_by('ordering')
    collection_length = len(task_list)
    tc_task_id = request.session["tc_task_id"]
    if tc_task_id < collection_length - 1:
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


def tc_run_view2(request):
    """

    """
    post_dict = request.POST
    try:
        task = get_task_to_process(post_dict)
    except TC_Finished:
        tc_id = request.POST['meta_tc_id']
        return tc_run_final_view(request, tc_id)

    request.session['tc_id'] = task.tc_id
    request.session['tc_task_id'] = task.tc_task_id

    log = ""
    if 'log' in request.session:
        log = request.session['log']

    log += "Show {solution} task {task} of collection {coll}.\n".format(
        solution="solution of" if task.solution_flag else "",
        task=str(task.tc_task_id),
        coll=str(task.tc_id)
    )
    request.session["log"] = log
    print(log)

    main_block = debug_main_block_object(request, task)
    main_block.tc_run_flag = True # trigger the correct url in the template
    main_block.tc_id = task.tc_id
    main_block.tc_task_id = task.tc_task_id

    context_dict = dict(main_block=main_block, task=task)
    context = Context(context_dict)

    return render(request, 'tasks/cq0_main_simple.html', context)


def tc_run_view(request, tc_id, tc_task_id, solution_flag=False):
    """
    render a task from a task collection (TC) by position in that TC

    @param {int} tc_id: which task collection
    @param tc_task_id: relative position of the task in the task collection. NOT the task_id (pk of tasks)
    @param solution_flag: show solution or not?
    """

    1 / 0 # this fucntion is deprecated and should not be called

    tc_task_id = int(tc_task_id)
    tc = get_object_or_404(TaskCollection, pk=tc_id)

    ordered_task_list = tc.tc_membership_set.order_by('ordering')
    tc.len = len(ordered_task_list)

    if tc_task_id >= len(ordered_task_list):
        return tc_run_final_view(request, tc_id)

    current_task = ordered_task_list[tc_task_id].task
    current_task.tc_len = len(ordered_task_list)
    current_task.solution_flag = solution_flag
    current_task.tc_task_id = tc_task_id
    current_task.tc = tc

    # construct the main_blocks
    main_blocks = [task_content_block(request, current_task)]

    # construct the meta_blocks
    meta_blocks = [task_meta_block(request, current_task)]
    meta_blocks += [task_collection_meta_block(request, tc)]

    context_dict = dict(main_blocks=main_blocks, meta_blocks=meta_blocks)
    context = Context(context_dict)

    response = HttpResponse()
    if 'tc_task_id' in request.session:
        session_tc_task_id = request.session['tc_task_id']
        session_tc_id = request.session['tc_id']

        if session_tc_id != tc_id:
            response.write("<p>This is not the Task Collection you're looking for.</p>")
            return response

        if session_tc_task_id > tc_task_id:
            response.write("<p>No backtracking!</p>")
            return response

        if (tc_task_id - session_tc_task_id) > 1:
            response.write("<p>No skipping tasks!</p>")
            return response

    else:
        if tc_task_id > 0:
            response.write("<p>Need to start at the beginning.</p>")
            return response

    request.session['tc_id'] = tc_id
    request.session['tc_task_id'] = tc_task_id

    log = ""
    if 'log' in request.session:
        log = request.session['log']

    log += "Show {solution} task {task} of collection {coll}.\n".format(
        solution="solution of" if solution_flag else "",
        task=str(tc_task_id),
        coll=str(tc_id)
    )
    request.session["log"] = log

    return render(request, 'tasks/cq0_main_base.html', context)


def task_content_block(request, task):
    """
    @param task: the task to render
    @return the rendered html for the content of a task
    """

    segments = aux_get_segment_list_from_task(task)

    if task.solution_flag:
        button_list = ['result', 'next']
    else:
        button_list = ['result']

    button_strings = aux_task_button_strings(task.solution_flag)

    user_solution = aux_task_user_solution(request, task.solution_flag)
    html_strings = [render_segment(segment, user_solution) for segment in segments]

    context_dict = dict(task=task, button_strings=button_strings,
                        html_strings=html_strings)

    context = Context(context_dict)
    template = loader.get_template('tasks/cq1_task_content.html')

    return template.render(RequestContext(request, context))


def task_meta_block(request, task):
    """
    returns the rendered html for the meta-info-block for a task
    """

    context_dict = dict(task=task)

    context = RequestContext(request, context_dict)
    tmpl = loader.get_template('tasks/cq1_task_meta.html')

    return tmpl.render(context)


def task_collection_meta_block(request, tc):
    """
    returns the rendered html for the meta-info-block for a task collection
    """

    context_dict = dict(tc=tc)
    context = Context(context_dict)
    tmpl = loader.get_template('tasks/cq1_taskcollection_meta.html')

    return tmpl.render(context)


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


def task_view(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', dict(task=task))