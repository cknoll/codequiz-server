# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404

from IPython import embed as IPS

from aux import xml_lib

from quiz.models import Task, TaskCollection


class Container(object):
    pass

C = Container()

def render_toplevel_elt(tle, user_sol_list=None):
    template = loader.get_template(tle.template)
    if user_sol_list == None:
        tle.context.update({'print_solution':False})
    else:
        tle.context.update({'print_solution':True})
        tle.update_user_solution(user_sol_list)
    return template.render(Context(tle.context))

def index(request):
    task_list = Task.objects.order_by('pub_date')[:5]
    #raise Http404, "Ach wie schade"
    return render(request, 'tasks/index.html', dict(task_list=task_list))


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

    le_sol = [v for k,v in items if k.startswith('le')]

    #!! cbox

    return le_sol


def aux_task_strings(task, solution=False):
    if not solution:
        button_strings = [get_button(t) for t in ['solution', 'next']]
        user_solution = None
    else:
        button_strings = [get_button('next') ]

        user_solution = get_solutions_from_post(request)

    return button_strings, user_solution

def aux_task_button_strings(solution):

    if not solution:
        button_strings = [get_button(t) for t in ['solution', 'next']]
    else:
        button_strings = [get_button('next') ]

    return button_strings


def aux_task_user_solution(request, solution):

    if not solution:
        user_solution = None
    else:
        user_solution = get_solutions_from_post(request)

    return user_solution




def task_view(request, task_id, solution = False):
    task = get_object_or_404(Task, pk=task_id)
    tle_list = aux_get_tle_list_from_task(task)

    button_strings = aux_task_button_strings(solution)
    user_solution = aux_task_user_solution(request, solution)
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

    if 'next' in request.POST:
        return next_task(request, task_id)
    elif 'solution' in request.POST:
        return task_view(request, task_id, solution=True)
        #return solution_task(request, task_id)
    else:
        # this should not happen
        return task_view(request, task_id)

    le1 = request.POST.get('le1', '')
    le2 = request.POST.get('le2', '')
    le3 = request.POST.get('le3', '')

    IPS()

    le_res = """
    le1 = %s
    le2 = %s
    le3 = %s
    """ % (le1, le2, le3)


    txt = "Results for %s %s" %(task_id, le_res)
    return HttpResponse(txt)


def tc_run_view(request, tc_id, tc_task_id):
    """
    tc_task_id is the relative position of the current task in the
    current TaskCollection. NOT the task_id (pk of tasks)
    """

    tc_task_id = int(tc_task_id)

    tc = get_object_or_404(TaskCollection, pk=tc_id)
    # get current task an next task
    ordered_task_list = tc.tc_membership_set.order_by('ordering')
#    IPS()
    # TODO: do we need it?
    if tc_task_id >= len(ordered_task_list):
        raise Http404('No such task_id (%s) for task collection %s' % (tc_task_id, tc_id))
    current_task = ordered_task_list[tc_task_id].task


    solution=False
    tle_list = aux_get_tle_list_from_task(current_task)

    button_strings = aux_task_button_strings(solution)
    user_solution = aux_task_user_solution(request, solution)
    html_strings = [render_toplevel_elt(tle, user_solution) for tle in tle_list]


    d = dict(task = current_task, tc = tc, button_strings = button_strings,
             html_strings = html_strings, ID = tc_task_id+1,
             LEN = len(ordered_task_list))
    context = Context(d)

    return render(request, 'tasks/tc_run_task_detail.html', context)



def task_collection_view(request, tc_id):
    tc = get_object_or_404(TaskCollection, pk=tc_id)
    tasks = tc.tasks.iterator()

    d = dict(task_list = tasks, title = tc.title, author = tc.author)
    context = Context(d)

    return render(request, 'tasks/task_collection.html', context)


def task_view0(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', dict(task=task))