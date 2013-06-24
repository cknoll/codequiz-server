# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404

from IPython import embed as IPS

from aux import xml_lib

from quiz.models import Task


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


def aux_get_task(task_id):

    task = get_object_or_404(Task, pk=task_id)
    root = xml_lib.load_xml(task.body_xml)


    task.tag_list = [tag.strip() for tag in task.tag_list.split(',')]
    tle_list = xml_lib.split_xml_root(root)

    return task, tle_list

def get_solutions_from_post(request):
    items = request.POST.items()
    items.sort()

    le_sol = [v for k,v in items if k.startswith('le')]

    #!! cbox

    return le_sol

def task_view(request, task_id, solution = False):
    task, tle_list = aux_get_task(task_id)

    if not solution:
        button_strings = [get_button(t) for t in ['solution', 'next']]
        user_solution = None
    else:
        button_strings = [get_button('next') ]

        user_solution = get_solutions_from_post(request)


    html_strings = [render_toplevel_elt(tle, user_solution) for tle in tle_list]
    context = Context({
            'task' : task,
            'strings' : html_strings,
            'button_strings' : button_strings
        })
    return render(request, 'tasks/detail.html', context)



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


def task_view0(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/detail.html', dict(task=task))