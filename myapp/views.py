from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("Hello, world index.")

def hello_world(request):
    return render(request, 'index.html')

def home_view(request):
    return HttpResponse(f"Hello {request.user.username}, you're logged in!")
def register_view(request):
    if request.user.is_authenticated:
        return redirect('question_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('question_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('question_list')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('question_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'home.html', {
        'username': request.user.username,
        'questions': questions
    })

def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'home.html', {
        'username': request.user.username,
        'questions': questions
    })


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            body = request.POST.get('body')
            if body:
                Answer.objects.create(
                    question=question,
                    body=body,
                    author=request.user
                )
                return redirect('question_detail', pk=pk)
    
    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers
    })

@login_required
def ask_question(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')

        if title and body:
            Question.objects.create(
                title=title,
                body=body,
                author=request.user
            )
            return redirect('question_list')

    return render(request, 'ask_question.html')


@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect('question_detail', pk=answer.question.pk)