from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, NewReplyForm
from django.conf import settings
from utils.mail.mail_sender import MailSender
import json
from api.models import User

# Create your views here.

def registerPage(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def loginPage(request):
    form = LoginForm()

    if request.method == 'POST':
        try:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'login.html', context)

@login_required(login_url='register')
def logoutPage(request):
    logout(request)
    return redirect('login-new')

@login_required(login_url='register')
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'new-question.html', context)

def homePage(request):
    questions = Question.objects.all().order_by('-created_at')
    mainQuestions = []
    for q in questions:
      if q.likes.filter(id=request.user.id).exists():
        mainQuestions.append({
          "id":q.id,
          "title":q.title,
          "authorname":q.author.username,
          "doeslike": True,
          "count":q.likes.filter().count() 
        })
      else:
        mainQuestions.append({
          "id":q.id,
          "title":q.title,
          "authorname":q.author.username,
          "doeslike": False,
          "count":q.likes.filter().count() 
        })
    context = {
        'questions': mainQuestions,
    }
    return render(request, 'homepage.html', context)

def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question(id=id)
                question_object = Question.objects.get(id=id)
                mail = MailSender(question_object.author.email)
                mail.sendUserAnswerNotification(question_object, response.user)
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    theResponses=[]
    for r in question.get_responses():
      if r.likes.filter(id=request.user.id).exists():
        theResponses.append({
          "id":r.id,
          "body":r.body,
          "authorname":r.user.username,
          "doeslike": True,
          "count":r.likes.filter().count() 
        })
      else:
        theResponses.append({
          "id":r.id,
          "body":r.body,
          "authorname":r.user.username,
          "doeslike": False,
          "count":r.likes.filter().count() 
        })
      
    theResponses.sort(key=lambda x: x["count"], reverse=True)
    print(theResponses)
    context = {
        'question': question,
        'theResponses':theResponses,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'question.html', context)


@login_required(login_url='register')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('index')

############################################################################

def registerPageNew(request):
  return render(request,'accounts/register-new.html')

def loginPageNew(request):
  return render(request,'accounts/login-new.html')

def verifyemailsuccess(request):
  return render(request,'accounts/verify-email-success.html')

def verifyemailfailed(request):
  return render(request,'accounts/verify-email-failed.html')

def logoutMain(request):
    logout(request)
    return redirect('login-new')

################################################################################################
def userprofile(request,username):
  user = User.objects.filter(username=username)
  if user.exists():
    questionLikes=0
    answerLikes=0
    totalLikes=0
    q=Question.objects.filter(author=user[0])
    r=Response.objects.filter(user=user[0])
    questioncount = q.count()
    answercount = r.count()
    for i in q:
      questionLikes = questionLikes + i.likes.count()
    for i in r:
      answerLikes = answerLikes + i.likes.count()
    totalLikes = questionLikes + answerLikes
    if (questioncount+answercount) != 0:
      reputationscore = totalLikes/(questioncount+answercount)
    else:
      reputationscore=0
    data  = {'username':user[0].username,
              'questioncount': questioncount,
              'answercount': answercount,
              'questionlikescount': questionLikes,
              'answerlikescount': answerLikes,
              'totallikescount': totalLikes,
              'reputationscore': reputationscore,
              }
  else:
    data  = {'username':"No Such User Found",
              'questioncount': "No Data To Display",
              'answercount': "No Data To Display",
              'questionlikescount': "No Data To Display",
              'answerlikescount': "No Data To Display",
              'totallikescount': "No Data To Display",
              'reputationscore': "No Data To Display",
              }
  return render(request,'accounts/userprofile.html',data)

