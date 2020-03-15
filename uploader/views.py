import os
from shutil import rmtree
from wsgiref.util import FileWrapper

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from .forms import UploadFileForm
from .models import StoredObject
from .upload import Uploader

uploader = Uploader()


def index(request):
    template = loader.get_template("uploader/index.html")
    return HttpResponse(template.render({}, request))


def profile(request):
    objs = StoredObject.objects.filter(owner=request.user.username)
    template = loader.get_template("uploader/profile.html")
    context = {
        'upload_list': objs
    }
    return HttpResponse(template.render(context, request))


def registration(request):
    if request.method == 'POST':
        create_user(request)
        return profile(request)
    return render(request, "uploader/user_creation.html")


def create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create_user(username, email, password)
    user.save()
    login(request, user)


def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if uploader.upload(request.user, request.FILES['file']):
                s = StoredObject(name=request.FILES['file'], submit_date=timezone.now(), owner=request.user.username)
                s.save()
            return render(request, "uploader/upload_success.html")
    else:
        form = UploadFileForm()
    return render(request, "uploader/upload.html", {'form': form})


def handle_file_manager(request):
    if 'download' in request.POST:
        return download_view(request)
    elif 'delete' in request.POST:
        return delete_view(request)


def delete_view(request):
    for file in request.POST.getlist("checks[]"):
        StoredObject.objects.filter(name=file).delete()
        uploader.delete(request.user, file)
    return render(request, "uploader/delete_success.html")


def download_view(request):
    clean_tmp()
    if not os.path.isdir(f"tmp_media/{request.user}"):
        os.mkdir(f"tmp_media/{request.user}")
    else:
        rmtree(f"tmp_media/{request.user}")
        os.mkdir(f"tmp_media/{request.user}")
    file_list = request.POST.getlist("checks[]")
    if len(file_list > 0):
        for file in file_list:
            uploader.download(request.user, file)
        dl_path = ""
        if len(file_list) > 1:
            os.system(f"zip -r tmp_media/{request.user}.z tmp_media/{request.user}")
            dl_path = f"tmp_media/{request.user}.z"
        else:
            dl_path = f"tmp_media/{request.user}/{file_list[0]}"
        f = FileWrapper(open(dl_path, 'rb'))
        response = HttpResponse(f, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(dl_path)}"'
        return response
    else:
        return render(request, "uploader/download_success.html")
    #return render(request, "uploader/download_success.html")


def clean_tmp():
    for file in os.listdir("tmp_media"):
        if file.endswith(".z"):
            os.remove(f"tmp_media/{file}")