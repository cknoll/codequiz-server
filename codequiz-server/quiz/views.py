# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.template import Context, loader

from django.template import RequestContext

from django.shortcuts import render, get_object_or_404

from IPython import embed as IPS

from aux import xml_lib

from quiz.models import Task, TaskCollection


class DictContainer(object):
    """
    allows easy dot access to the content of a dict
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def render_toplevel_elt(tle, user_sol_list=None):
    template = loader.get_template(tle.template)
    if user_sol_list == None:
        tle.context.update({'print_solution':False})
    else:
        tle.context.update({'print_solution':True})
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

    return task_collection_view(request, 2)

def get_button(button_type):
    #!! loaded every time!!
    btempl = loader.get_template('tasks/task_buttons1.html')
    bContext = Context({
            'button_type': button_type,})
    return btempl.render(bContext)



def aux_get_tle_list_from_task(task):
    """
    returns list of top level elements (tle) of the task-xml
    """
    root = xml_lib.load_xml(task.body_xml)

    # unpack the taglist:
    # TODO: this should be implemented in the model??
    if isinstance(task.tag_list, str):
        task.tag_list = [tag.strip() for tag in task.tag_list.split(',')]

    tle_list = xml_lib.split_xml_root(root)

    return tle_list





def get_solutions_from_post(request):
    items = request.POST.items()
    items.sort()

    le_sol = [ (k,v) for k,v in items if k.startswith('le')]

    # Problem: unchecked cboxes are not contained in request.POST
    # solution every cbox has a hidden compagnion with the name:
    # hidden_<cbox_name>

    cbox_names = [k[7:] for k,v in items if k.startswith('hidden_cbox')]

#    print cbox_names

    #create a list of tuples like [('cbox1', 'True'), ('cbox2', 'False')]
    cbox_results = [(cbn, str(cbn in request.POST)) for cbn in cbox_names]


    res = dict(le_sol+cbox_results)
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




def task_view(request, task_id, solution_flag = False):
    task = get_object_or_404(Task, pk=task_id)
    tle_list = aux_get_tle_list_from_task(task)

    button_strings = aux_task_button_strings(solution_flag)
    user_solution = aux_task_user_solution(request, solution_flag)
    html_strings = [render_toplevel_elt(tle, user_solution) for tle in tle_list]

    d = dict(task = task, strings = html_strings,
             button_strings = button_strings)

    context = Context(d)
    return render(request, 'tasks/task_detail.html', context)



def next_task(request, task_id):
    """
    returns the next task in current test
    """
    new_id = str(int(task_id)+1)
    return task_view(request, new_id)


def form_result_view(request, task_id):

    p = request.POST
    #IPS()
    if 'next' in request.POST:
        return next_task(request, task_id)
    elif 'result' in request.POST:
        return task_view(request, task_id, solution_flag=True)
    else:
        # this should not happen
        return task_view(request, task_id)

#    le1 = request.POST.get('le1', '')
#    le2 = request.POST.get('le2', '')
#    le3 = request.POST.get('le3', '')
#
#    IPS()
#
#    le_res = """
#    le1 = %s
#    le2 = %s
#    le3 = %s
#    """ % (le1, le2, le3)
#
#
#    txt = "Results for %s %s" %(task_id, le_res)
#    return HttpResponse(txt)


def tc_run_form_process(request, tc_id, tc_task_id):

    if 'next' in request.POST:
        next_id = u"%i" % ( int(tc_task_id)+1 )
        return tc_run_view(request, tc_id, next_id, solution_flag=False)

    elif 'result' in request.POST:
        return tc_run_view(request, tc_id, tc_task_id, solution_flag=True)



def tc_run_final_view(request, tc_id):

    tc = get_object_or_404(TaskCollection, pk=tc_id)

    d = dict(tc = tc)
    context = Context(d)

    return render(request, 'tasks/tc_run_final.html', context)


def tc_run_view(request, tc_id, tc_task_id, solution_flag=False):
    """
    tc_task_id is the relative position of the current task in the
    current TaskCollection. NOT the task_id (pk of tasks)
    """

    tc_task_id = int(tc_task_id)

    tc = get_object_or_404(TaskCollection, pk=tc_id)
    # get current task an next task

    # TODO: this should live in the model:
    ordered_task_list = tc.tc_membership_set.order_by('ordering')
    tc.len = len(ordered_task_list)

    if tc_task_id >= len(ordered_task_list):
        return tc_run_final_view(request, tc_id)

    current_task = ordered_task_list[tc_task_id].task
    current_task.solution_flag = solution_flag
    current_task.tc_task_id = tc_task_id
    current_task.tc = tc
    current_task.tc_len = len(ordered_task_list)


    # construct the main_blocks
    main_blocks = [task_content_block(request, current_task)]

    # construct the meta_blocks
    meta_blocks = [task_meta_block(request, current_task)]
    meta_blocks += [task_collection_meta_block(request, tc)]

    d = dict(main_blocks = main_blocks, meta_blocks = meta_blocks)
    context = Context(d)


    return render(request, 'tasks/cq0_main.html', context)


def task_content_block(request, task):
    """
    returns the rendered html for the content of a task
    """

    tle_list = aux_get_tle_list_from_task(task)

    button_strings = aux_task_button_strings(task.solution_flag)
    user_solution = aux_task_user_solution(request, task.solution_flag)
    html_strings = [render_toplevel_elt(tle, user_solution) for tle in tle_list]

    d = dict(task = task, button_strings = button_strings,
             html_strings = html_strings)

    context = Context(d)
    tmpl = loader.get_template('tasks/cq1_task_content.html')

    return tmpl.render(RequestContext(request, context))

def task_meta_block(request, task):
    """
    returns the rendered html for the meta-info-block for a task
    """

    d = dict(task = task)

    context = Context(d)
    tmpl = loader.get_template('tasks/cq1_task_meta.html')

    return tmpl.render(context)

def task_collection_meta_block(request, tc):
    """
    returns the rendered html for the meta-info-block for a task collection
    """

    d = dict(tc = tc)
    context = Context(d)
    tmpl = loader.get_template('tasks/cq1_taskcollection_meta.html')

    return tmpl.render(context)



def task_collection_view(request, tc_id):
    tc = get_object_or_404(TaskCollection, pk=tc_id)
    tasks = tc.tasks.iterator()

    d = dict(task_list = tasks, tc = tc)
    context = Context(d)

    return render(request, 'tasks/task_collection.html', context)


def task_view0(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', dict(task=task))