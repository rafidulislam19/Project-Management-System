from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectNote
from .forms import ProjectFileForm # type: ignore

# Create your views here.

@login_required
def projects(request):
    projects = Project.objects.filter(created_by = request.user)
    return render(request, 'project/projects.html', {
        'projects': projects
    })

@login_required
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        description = request.POST.get('description','')

        if name:
            Project.objects.create(name=name, description=description, created_by=request.user)

            return redirect('/projects/')
        else:
            print("Not Valid")

    return render(request, 'project/add.html')

@login_required
def project(request, pk):
    project = Project.objects.filter(created_by = request.user).get(pk=pk)
    return render(request, 'project/project.html', {
        'project': project
    })

@login_required
def edit_project(request, pk):
    project = Project.objects.filter(created_by = request.user).get(pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name','')
        description = request.POST.get('description','')

        if name:
            project.name = name
            project.description = description
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

