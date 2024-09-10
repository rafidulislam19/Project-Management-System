from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectNote, ProjectFile
from account.models import User
from task.models import Task
from .forms import ProjectFileForm # type: ignore
from .models import Team
from django.contrib import messages

# Create your views here.

@login_required
def projects(request):
    projects = Project.objects.filter(created_by = request.user)
    return render(request, 'project/projects.html', {
        'projects': projects
    })

# HoD - Access to all projects
@login_required
def projects(request):
    if request.user.is_hod:
        projects = Project.objects.all()
    elif request.user.is_manager:
        projects = Project.objects.filter(team=request.user.team)
    else:
        projects = Project.objects.filter(members=request.user)
    return render(request, 'projects.html', {'projects': projects})

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
# @login_required
# def add_project(request):
#     if not request.user.is_manager:
#         return HttpResponseForbidden("You do not have permission to add projects.")

#     if request.method == "POST":
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         members = request.POST.getlist('members')
        
#         project = Project.objects.create(name=name, description=description, team=request.user.team, manager=request.user)
#         project.members.set(User.objects.filter(id__in=members))
#         project.save()

#         return redirect('/projects/')

#     team_members = User.objects.filter(team=request.user.team)
#     return render(request, 'add.html', {'team_members': team_members})

# Manager - Can add project to their team
@login_required
def add_project(request):
    # Check if the user is a manager
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to add a project.")
        return redirect('/index/')

    teams = Team.objects.filter(members=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team_id = request.POST.get('team')

        if name and team_id:
            team = Team.objects.get(id=team_id)

            # Ensure the manager is assigning to their own team
            if request.user in team.members.all():
                project = Project.objects.create(
                    name=name,
                    description=description,
                    team=team,
                    created_by=request.user
                )
                messages.success(request, "Project added successfully!")
                return redirect('/projects/', project_id=project.id)
            else:
                messages.error(request, "You can only assign projects to your own team.")
        else:
            messages.error(request, "Please fill in all required fields.")

    context = {
        'teams': teams,
    }

    return render(request, 'add.html', context)

# @login_required
# def edit_project(request, pk):
#     if not request.user.is_manager:
#         return HttpResponseForbidden("You do not have permission to add projects.")
    
#     project = Project.objects.filter(created_by = request.user).get(pk=pk)
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         team_id = request.POST.get('team')

#         if name and team_id:
#             team = Team.objects.get(id=team_id)

#             project.name = name
#             project.description = description
#             project.team = team
            
#             project.save()

#             return redirect('/projects/')
#         else:
#             print("Not Valid")

#     return render(request, 'project/edit.html', {
#         'project': project
#     })

@login_required
def edit_project(request, project_id):
    # Retrieve the project or return a 404 if not found
    project = get_object_or_404(Project, id=project_id)

    if not request.user.is_manager or request.user not in project.team.members.all():
        messages.error(request, "You do not have permission to edit this project.")
        return redirect('/projects/') 

    # Get the teams that the user manages
    teams = Team.objects.filter(members=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team_id = request.POST.get('team')

        if name and team_id:
            team = Team.objects.get(id=team_id)

            if request.user in team.members.all():
                project.name = name
                project.description = description
                project.team = team
                project.save()
                messages.success(request, "Project updated successfully!")
                return redirect('/project/', project_id=project.id)
            else:
                messages.error(request, "You can only assign projects to your own team.")
        else:
            messages.error(request, "Please fill in all required fields.")

    context = {
        'project': project,
        'teams': teams,
    }

    return render(request, 'edit.html', context)


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