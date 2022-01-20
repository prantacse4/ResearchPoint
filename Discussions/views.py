from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Discussion, Topic, Comment
from Accounts.models import User
from .forms import DiscussionForm, UserForm
# Create your views here.


def wrong(request):
    context = {}
    return render(request, 'Discussions/wrong.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    discussions = Discussion.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains=q)|Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    topics_c = Topic.objects.all()
    topics_count = topics_c.count()
    discussion_count = discussions.count()
    discussion_comments = Comment.objects.filter(Q(discussion__topic__name__icontains=q))[0:10]
    context = {'discussions':discussions,'topics_count':topics_count, 'discussion_comments':discussion_comments, 'topics':topics, 'discussion_count':discussion_count}
    return render(request, 'Discussions/home.html', context)



def discussion(request, pk):
    thisdiscussion = Discussion.objects.get(pk=pk)
    discussion_comments = thisdiscussion.comment_set.all()
    participants = thisdiscussion.participants.all()
    if request.method == 'POST':
        if request.user.is_authenticated == False:
            return redirect('login')
        comment = Comment.objects.create(
            user = request.user,
            discussion = thisdiscussion,
            body = request.POST.get('body')
        )
        thisdiscussion.participants.add(request.user)
        return redirect('discussion', pk=thisdiscussion.id)
    
    diction = {'discussion':thisdiscussion, 'participants':participants, 'discussion_comments':discussion_comments}
    return render(request, 'Discussions/Discussion.html', context=diction)






@login_required(login_url='login')
def creatediscussion(request):
    form = DiscussionForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        if request.user.is_user:
            Discussion.objects.create(
                host=request.user,
                topic=topic,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                file=None,
            )
        if request.user.is_researcher:
            try:
                file = request.FILES['file']
            except:
                file = None
            Discussion.objects.create(
                host=request.user,
                topic = topic,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                file = file
            )
        return redirect('home')
        
        # form = DiscussionForm(request.POST)
        # if form.is_valid():
        #     discussion = form.save(commit=False)
        #     Discussion.host = request.user
        #     Discussion.save()
    diction = {'form':form, 'topics':topics}
    return render(request, 'Discussions/discussion_form.html', context=diction)

@login_required(login_url='login')
def updatediscussion(request, pk):
    discussion = Discussion.objects.get(pk=pk)
    form = DiscussionForm(instance=discussion)
    topics = Topic.objects.all()
    if request.user != discussion.host:
        return HttpResponse('You are not allowed here !!')
    if request.method == 'POST':
        if request.user.is_researcher == True:
            files = request.FILES or None
            form = DiscussionForm(request.POST, files, instance=discussion)
        else:
            form = DiscussionForm(request.POST, instance=discussion)

        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        discussion.name = request.POST.get('name')
        discussion.topic = topic
        discussion.description = request.POST.get('description')
        if request.user.is_researcher == True:
            if files is not None:
                discussion.file = request.FILES['file']
        discussion.save()
        return redirect('home')
    context = {'form':form, 'topics':topics, 'discussion':discussion}
    return render(request, 'Discussions/discussion_form.html', context)

@login_required(login_url='login')
def deletediscussion(request, pk):
    discussion = Discussion.objects.get(pk=pk)
    if request.user != discussion.host:
        return HttpResponse('You are not allowed here !!')
    if request.method == 'POST':
        discussion.delete()
        return redirect('home')
    context ={ 'obj':discussion }
    return render(request, 'Discussions/delete.html', context)



@login_required(login_url='login')
def deletecomment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.user != comment.user:
        return HttpResponse('You are not allowed here !!')
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    context ={ 'obj':comment }
    return render(request, 'Discussions/delete.html', context)




def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request, 'Discussions/topics.html', context)



def activityPage(request):
    discussion_comments = Comment.objects.all()
    context = {'discussion_comments':discussion_comments}
    return render(request, 'Discussions/activity.html', context)






@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form':form}
    return render(request, 'Discussions/update-user.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(pk=pk)
    discussions = user.discussion_set.all()
    discussion_comments = user.comment_set.all()
    topics = Topic.objects.all()[0:5]
    topics_c = Topic.objects.all()
    topics_count = topics_c.count()
    context = {'user':user,'topics_count':topics_count, 'discussions':discussions, 'discussion_comments':discussion_comments, 'topics':topics}
    return render(request, 'Discussions/profile.html', context)
