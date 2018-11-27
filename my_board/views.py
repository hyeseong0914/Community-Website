from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from .models import Board, Comment
from .forms import RegisterationForm, LoginForm, ProfileChangeForm
from board.settings import EMAIL_HOST_USER
from django.utils.http import urlquote
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, views, update_session_auth_hash
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
import math
import os

UPLOAD_DIR = "C:\\Users\\hyese\\blog\\board\\upload"
# Create your views here.

@csrf_exempt
def index(request):
    return render(request, 'index.html', {'logged_in': request.user.is_authenticated})

@csrf_exempt
def list(request):
    board_list = Board.objects.order_by('-id')

    query = request.GET.get('query')
    if query:
        board_list = board_list.filter(
            Q(title=query) |
            Q(author=query) |
            Q(content=query)
            ).distinct()

    paginator = Paginator(board_list, 5)
    page = request.GET.get('page')
    try:
        board_lists = paginator.page(page)
    except PageNotAnInteger:
        board_lists = paginator.page(1)
    except EmptyPage:
        board_lists = paginator.page(paginator.num_pages)
    board_count = Board.objects.all().count()

    return render(request, 'list.html', {'board_list': board_lists, 'board_count': board_count, 'logged_in': request.user.is_authenticated, 'page': page})

@csrf_exempt
def write(request):
    return render(request, 'write.html', {'logged_in': request.user.is_authenticated})

@csrf_exempt
def insert(request):
    file_name = ''
    file_size = 0
    if 'file' in request.FILES:
        file = request.FILES['file']
        file_name = file._name
        file_size = file._size

        fop = open("%s%s" % (UPLOAD_DIR, file_name), 'wb')

        for chunk in file.chunks():
            fop.write(chunk)
        fop.close()

    user = request.user
    dto = Board(author=user.username, title=request.POST['title'], content=request.POST['content'], file_name=file_name, file_size=file_size)
    dto.save()
    return redirect('/list')

@csrf_exempt
def download(request):
    id = request.GET['id']
    dto = Board.objects.get(id=id)
    path = UPLOAD_DIR + dto.file_name
    print("path:", path)
    file_name = os.path.basename(path)
    file_name = urlquote(file_name)
    print("pfilename:", os.path.basename(path))
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename*=UTF-8''{0}'.format(file_name)
        dto.down_up()
        dto.save()
        return response

@csrf_exempt
def edit_post(request):
    dto = Board.objects.get(id=request.GET['id'])
    dto.save()
    file_size = "{0:.2f}".format(dto.file_size / 1024)
    return render(request, 'edit.html', {'dto': dto, 'file_size': file_size, 'logged_in': request.user.is_authenticated})

@csrf_exempt
def edit_post_form(request):
    id = request.POST['id']
    dto = Board.objects.get(id=id)
    dto.set_title(request.POST['title'])
    dto.set_content(request.POST['content'])
    dto.save()
    messages.success(request, '수정이 완료되었습니다.')
    return redirect('/showpost?id='+id)

@csrf_exempt
def showpost(request):
    id = request.GET['id']
    dto = Board.objects.get(id=id)
    dto.hit_up()
    dto.save()
    comments = Comment.objects.filter(board_id=int(id)).order_by('-id')
    comments_count = Comment.objects.filter(board_id=int(id))

    return render(request, 'showpost.html', {'dto': dto, 'comments': comments, 'comments_count': comments_count ,'id': id, 'logged_in': request.user.is_authenticated})

@csrf_exempt
def delete_post(request):
    id = request.POST['id']
    dto = Board.objects.get(id=id)
    dto.delete()
    messages.success(request, '삭제가 완료되었습니다.')
    return redirect('/list')
    
@csrf_exempt
def comment(request):
    id = request.POST['id']
    user = request.user
    comment = Comment(board_id=id, author=user.username, content=request.POST['content'])
    comment.save()
    return redirect('/showpost?id='+id)

@csrf_exempt
def delete_comment(request):
    post_id = request.POST['id']
    id = request.POST['comment_id']
    comment = Comment.objects.get(id=id)
    comment.delete()
    messages.success(request, '댓글 삭제가 완료되었습니다.')
    return redirect('/showpost?id='+post_id)

@csrf_exempt
def edit_comment(request):
    comment_id = request.GET['id']
    comment = Comment.objects.get(id=comment_id)
    return render(request, 'edit_comment.html', {'comment': comment, 'logged_in': request.user.is_authenticated})

@csrf_exempt
def edit_comment_form(request):
    id = request.POST['id']
    comment = Comment.objects.get(id=id)
    comment.set_content(request.POST['content'])
    comment.save()
    messages.success(request, '댓글이 수정 되었습니다.')
    return redirect('/showpost?id='+str(comment.board_id))

@csrf_exempt
def register(request):
    if request.user.is_authenticated == False:
        if request.method == 'POST':
            form = RegisterationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                messages.success(request, '회원가입이 완료되었습니다.')
                return redirect('/index')
            else:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
        else:
            form = RegisterationForm()
    else:
        messages.error(request, '이미 로그인이 되어 있습니다.')
        form = RegisterationForm()
    return render(request, 'register.html', {'form': form, 'logged_in': request.user.is_authenticated})

def logout_user(request):
    logout(request)
    messages.error(request, '로그아웃 하였습니다.')
    return redirect('/index')

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated == False:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                messages.success(request, '로그인 되었습니다.')
                login(request, user)
                # if not form.cleaned_data.get('remember_me'):
                #     form.request.session.set_expiry(0)
                return redirect('/index')
            else:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
        else:
            form = LoginForm()
    else:
        messages.error(request, '이미 로그인이 되어 있습니다.')
        form = LoginForm()
    return render(request, 'login.html', {'logged_in': request.user.is_authenticated, 'form': form})

@csrf_exempt
def dashboard(request):
    user = request.user
    board_list = Board.objects.filter(author=user.username).order_by('-id')
    board_count = Board.objects.filter(author=user.username).count()
    paginator = Paginator(board_list, 5)
    page = request.GET.get('page')
    try:
        board_lists = paginator.page(page)
    except PageNotAnInteger:
        board_lists = paginator.page(1)
    except EmptyPage:
        board_lists = paginator.page(paginator.num_pages)

    return render(request, 'dashboard.html', {'board_list': board_lists, 'board_count': board_count, 'logged_in': request.user.is_authenticated, 'page': page})

@csrf_exempt
def find(request):
    return render(request, 'find.html', {})

def send_email(request):
    email = request.POST.get('email', False)
    try:
        account = User.objects.get(email=email)
    except:
        messages.error(request, '해당 이메일 주소를 찾을 수 없습니다.')
        return render(request, 'find.html', {})

    subject = '계정 아이디 문의'
    message = '계정찾기.\n 아이디:' + account.username
    from_email = EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email], fail_silently=False)
    messages.success(request, '찾으시는 아이디를 발송하였습니다.')
    return redirect('/login_user')

def profile(request):
    return render(request, 'profile.html', {'logged_in': request.user.is_authenticated})

def profile_edit(request):
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, user=request.user, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '계정 정보가 수정 되었습니다.')
            return redirect('/profile')
        else:
            messages.error(request, '입력 정보가 올바르지 않습니다.')
    else:
        form = ProfileChangeForm(user=request.user)
    return render(request, 'profile_edit.html', {'form': form, 'logged_in': request.user.is_authenticated})

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, '비밀번호가 재설정 되었습니다.')
            return redirect('/profile')
        else:
            messages.error(request, '입력 정보가 올바르지 않습니다.')
            return redirect('/password_change')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request,  'password_change.html', {'form': form, 'logged_in': request.user.is_authenticated})