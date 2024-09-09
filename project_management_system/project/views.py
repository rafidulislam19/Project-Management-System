from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectNote, ProjectFile
from account.models import User
from task.models import Task
from .forms import ProjectFileForm # type: ignore

# Create your views here.

@login_required
def projects(request):
    projects = Project.objects.filter(created_by = request.user)
    return render(request, 'project/projects.html', {
        'projects': projects
    })

# HoD - Access to all projects
@login_required
def project_list(request):
    if request.user.is_hod:
        projects = Project.objects.all()
    elif request.user.is_manager:
        projects = Project.objects.filter(team=request.user.team)
    else:
        projects = Project.objects.filter(members=request.user)
    return render(request, 'project_list.html', {'projects': projects})

# @login_required
# def add_project(request):
#     if request.method == 'POST':
#         name = request.POST.get('name','')
#         description = request.POST.get('description','')
#         assigned_team = request.POST.get('assigned_team','')

#         if name:
#             Project.objects.create(name=name, description=description, assigned_team=assigned_team, created_by=request.user)

#             return redirect('/projects/')
#         else:
#             print("Not Valid")

#     return render(request, 'project/add.html')



# Manager - Can add project to their team
@login_required
def add_project(request):
    if not request.user.is_manager:
        return HttpResponseForbidden("You do not have permission to add projects.")

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        members = request.POST.getlist('members')
        
        project = Project.objects.create(name=name, description=description, team=request.user.team, manager=request.user)
        project.members.set(User.objects.filter(id__in=members))
        project.save()

        return redirect('/projects/')

    team_members = User.objects.filter(team=request.user.team)
    return render(request, 'add_project.html', {'team_members': team_members})

# @login_required
# def project(request, pk):
#     project = Project.objects.filter(created_by = request.user).get(pk=pk)
#     return render(request, 'project/project.html', {
#         'project': project
#     })

# Regular User - Access to their assigned projects
@login_required
def project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.is_hod or project.manager == request.user or project.members.filter(id=request.user.id).exists():
        tasks = Task.objects.filter(project=project)
        files = ProjectFile.objects.filter(project=project)
        return render(request, 'project/project.html', {'project': project, 'tasks': tasks, 'files': files})
    else:
        return HttpResponseForbidden("You do not have access to this project.")

@login_required
def edit_project(request, pk):
    project = Project.objects.filter(created_by = request.user).get(pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name','')
        description = request.POST.get('description','')
        # assigned_team = request.POST.get('assigned_team','')

        if name:
            project.name = name
            project.description = description
            # project.assigned_team = assigned_team
            project.save()

            return redirect('/projects/')
        else:
            print("Not Valid")

    return render(request, 'project/edit.html', {
        'project': project
    })

@login_required
def delete(request, pk):
    project = Project.objects.filter(created_by = request.user).get(pk=pk)
    project.delete()

    return redirect('/projects/')

# Files


@login_required
def upload_file(request, project_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)

    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)

        if form.is_valid():
            projectfile = form.save(commit=False)
            projectfile.project = project
            projectfile.save()

            return redirect(f'/projects/{project_id}/')
    else:
        form = ProjectFileForm()

    return render(request, 'project/upload_file.html', {
        'project': project,
        'form': form
    })

@login_required
def delete_file(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    projectfile = project.files.get(pk=pk)
    projectfile.delete()

    return redirect(f'/projects/{project_id}/')


@login_required
def add_note(request, project_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        body = request.POST.get('body', '')

        if name and body:
            ProjectNote.objects.create(
                project=project,
                name=name,
                body=body
            )

            return redirect(f'/projects/{project_id}/')

    return render(request, 'project/add_note.html', {
        'project': project
    })

@login_required
def note_detail(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    note = project.notes.get(pk=pk)

    return render(request, 'project/note_detail.html', {
        'project': project,
        'note': note
    })

@login_required
def note_edit(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    note = project.notes.get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        body = request.POST.get('body', '')

        if name and body:
            note.name = name
            note.body = body
            note.save()

            return redirect(f'/projects/{project_id}/')

    return render(request, 'project/note_edit.html', {
        'project': project,
        'note': note
    })

@login_required
def note_delete(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    note = project.notes.get(pk=pk)
    note.delete()

    return redirect(f'/projects/{project_id}/')