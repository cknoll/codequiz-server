from models import Task
from django.shortcuts import *


def admin_add_view(request, model_admin):
    print("blaaaaa")
    opts = model_admin.model._meta
    admin_site = model_admin.admin_site
    has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())
    context = {'admin_site': admin_site.name,
               'title': "Add Task",
               'opts': opts,
               #'root_path': '/%s' % admin_site.root_path,
               'app_label': opts.app_label,
               'has_change_permission': has_perm}
    template = 'admin/admin_add_view.html'
    return render_to_response(template, context, context_instance=RequestContext(request))


def admin_change_view(request, model_admin, taskid=None):
    opts = model_admin.model._meta
    admin_site = model_admin.admin_site
    has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())

    # Here you do your own thing!
    obj = None
    if taskid:
        print("taskid: " + taskid)
        obj = Task.objects.get(id=taskid)
        print("obj: " + str(obj))

    # Here you can add to the context - the marked items are new, the rest is
    # required by the admin site
    context = {'admin_site': admin_site.name,
               'title': 'Edit Task',
               'opts': opts,
               #'root_path': '/%s' % admin_site.root_path,
               'app_label': opts.app_label,
               'task': obj,
               'has_change_permission': has_perm}
    template = 'admin/admin_change_view.html'  # = Your new template
    return render_to_response(template, context,
                              context_instance=RequestContext(request))