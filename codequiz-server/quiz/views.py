# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
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


def render_toplevel_element(tle, user_sol_list=None):
    # TODO: rename to tle to segment
    template = loader.get_template(tle.template)
    if user_sol_list is None:
        tle.context.update({'print_solution': False})
    else:
        tle.context.update({'print_solution': True})
        tle.update_user_solution(user_sol_list)
    return template.render(Context(tle.context))


def index_old(request):
    task_list = Task.objects.order_by('pub_date')[:5]
    #raise Http404, "Ach wie schade"
    return render(request, 'tasks/index.html', dict(task_list=task_list))


def index(request):
    """
    temporary solution for the python lecture 2013/07/08
    """

    return task_collection_view(request, 1)


def aux_get_task_from_tc_ids(tc_id, tc_task_id = None, next_task = False):
    """
    tc_task_id = None -> first task in this collection
    """

    # TODO !! get the real task_id
    task_id = 0
    task = aux_get_json_task(task_id)

    task.tc_id = tc_id
    task.tc_task_id = tc_task_id
    return task



def aux_get_json_task(task_id):
    """
    currently returns only pseudo stuff
    """


    # for the moment return the pseodo task
    class pseudo_task():
        """
        pseudo task, because json currently comes from a file and
        not a database
        """
        id = task_id
        title = "0815-Test-Task"
        author = "Wilhelm, das Kind"
        tags_as_string = "no tags"
        segment_list = json_lib.debug_task()
        solution_flag = False



    db_task = get_object_or_404(Task, pk=task_id)

    if db_task.body_xml.startswith("<?xml"):
        return pseudo_task
    else:
        json_lib.preprocess_task_from_db(db_task)
        return db_task


def debug_url_landing(request):
    """
    Example function how to emulate formular-processing
    in case just a simple url is opend
    """

    p = dict(request.POST) # POST itself is immutable
    p['meta_task_id'] = "23"
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

    task_id = post_dict['meta_task_id']

    if 'meta_no_form' in post_dict:
        task =  aux_get_json_task(task_id = task_id)
        return task

    elif 'button_next' in post_dict:
        if post_dict.get('meta_tc_id', "") != "":
            tc_id = post_dict['meta_tc_id']
            tc_task_id = post_dict['meta_tc_task_id']
            task = aux_get_task_from_tc_ids(tc_id, tc_task_id, next_task = True)
        else:
            # TODO:!! In explict mode there should not be a "next" button
            raise Http404, "For explictly adressed tasks, there is no successor!"
            aux_get_json_task(task_id = task_id, next_task = True)
        return task

    elif 'button_result' in post_dict:
        if  post_dict.get('meta_tc_id', "") != "":
            tc_id = post_dict['meta_tc_id']
            tc_task_id = post_dict['meta_tc_task_id']
            task = aux_get_task_from_tc_ids(tc_id, tc_task_id)
        else:
            task = aux_get_json_task(task_id = task_id)
        task.solution_flag = True

        return task
    else:
        raise Http404, "Unknown formular content."



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
    tmb = get_task_meta_block(request, task)

    context_dict = dict(main_block = main_block, task = task)

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

    button_strings = aux_task_button_strings(task.solution_flag)
    html_strings = [render_toplevel_element(tle, user_solution) for tle in segment_list]

    res = myContainer(task=task, button_strings=button_strings,
                        html_strings=html_strings)

    res.debug_flag = True
    res.tc_id = ""
    res.tc_task_id = ""

    return res

def debug1(request, tc_id=None, tc_task_id=None):


    task = aux_get_json_task(task_id = 12) # 12 is the test-json-task

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
    return button_template.render(bContext)


def aux_get_tle_list_from_task(task):
    """
    returns list of top level elements (tle) of the task-xml
    """
    root = xml_lib.load_xml(task.body_xml)

    tle_list = xml_lib.split_xml_root(root)

    return tle_list


def get_solutions_from_post(request):
    # TODO: this function probably could be simplified
    items = request.POST.items()
    items.sort()

    le_solution = [(k, v) for k, v in items if k.startswith('le')]

    # Problem: unchecked cboxes are not contained in request.POST
    # solution: every cbox has a hidden companion with the name:
    # hidden_<cbox_name>

    checkbox_names = [k[7:] for k, v in items if k.startswith('hidden_cbox')]

    #create a list of tuples like [('cbox1', 'True'), ('cbox2', 'False')]
    checkbox_results = [(cbn, str(cbn in request.POST)) for cbn in checkbox_names]

    # new keys: just the index (number after '_idx_'-part of the name)

    items = le_solution + checkbox_results

    new_items = []
    for k,v in items:
        assert '_idx_' in k
        idx = k.split('_idx_')[-1]
        new_items.append( (int(idx), v) )


    res = dict(new_items)
    return res


def aux_task_button_strings(solution_flag):
    if not solution_flag:
        button_strings = [get_button(t) for t in ['result']]
    else:
        button_strings = [get_button(t) for t in ['result', 'next']]

    return button_strings


def aux_task_user_solution(request, solution_flag):
    if not solution_flag:
        user_solution = None
    else:
        user_solution = get_solutions_from_post(request)

    return user_solution

## TODO: obsolete
#def task_view(request, task_id, solution_flag=False):
#    """
#    Show a task by itself
#
#    Dirty workaround for now. Used only for previewing/debugging
#    """
#
#    tc_task_id = 0
#    tc_id = 1
#    tc = get_object_or_404(TaskCollection, pk=tc_id)
#
#    current_task = get_object_or_404(Task, pk=task_id)
#    current_task.solution_flag = solution_flag
#    current_task.tc_task_id = tc_task_id
#    current_task.tc = tc
#
#    # construct the main_blocks
#    main_blocks = [task_content_block(request, current_task, preview_only=True)]
#    tmb = [get_task_meta_block(request, current_task)]
#
#    context_dict = dict(main_blocks=main_blocks, meta_blocks=tmb)
#    context = Context(context_dict)
#
#    return render(request, 'tasks/cq0_main.html', context)


def next_task(request, task_id):
    """
    returns the next task in current test
    """
    new_id = str(int(task_id) + 1)
    return task_view(request, new_id)


def form_result_view(request, task_id):
    post = request.POST
    #IPS()
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


def tc_run_view(request, tc_id, tc_task_id, solution_flag=False):
    """
    render a task from a task collection (TC) by position in that TC

    @param {int} tc_id: which task collection
    @param tc_task_id: relative position of the task in the task collection. NOT the task_id (pk of tasks)
    @param solution_flag: show solution or not?
    """

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
    print(log)

    return render(request, 'tasks/cq0_main.html', context)


def task_content_block(request, task, preview_only=False):
    """
    @param task: the task to render
    @param preview_only: True disables rendering of buttons
    @return the rendered html for the content of a task
    """

    tle_list = aux_get_tle_list_from_task(task)

    if not preview_only:
        button_strings = aux_task_button_strings(task.solution_flag)
    else:
        button_strings = None
    user_solution = aux_task_user_solution(request, task.solution_flag)
    html_strings = [render_toplevel_element(tle, user_solution) for tle in tle_list]

    context_dict = dict(task=task, button_strings=button_strings,
                        html_strings=html_strings)

    context = Context(context_dict)
    template = loader.get_template('tasks/cq1_task_content.html')

    return template.render(RequestContext(request, context))


def get_task_meta_block(request, task):
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

    return render(request, 'tasks/task_collection.html', context)


def task_view0(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', dict(task=task))