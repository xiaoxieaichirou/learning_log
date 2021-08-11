# Create your views here.

from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, EntryForm


def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')  # render()根据视图提供的数据渲染响应


# 使用@login_required装饰器限制访问没自由已登录的用户才能访问
@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  # filter()获取合适的数据
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')  # -date_added按降序排列，如是+则是正序排
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():  # is_valid()核实用户填写了所有必不可少的字段
            new_topic = form.save(commit=False)  # 实参commit=False为创建一个新的条目对象，并将其存储到new_entry中，但不将它保存到数据库中
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(
                reverse('learning_logs:topics'))  # HttpResponseRedirect类，用户提交主题后使用此类将用户重定向到网页topics
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # 实参commit=False为创建一个新的条目对象，并将其存储到new_entry中，但不将它保存到数据库中
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(request, topic)

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)  # 根据既有条目对象创建一个表单实例，并根据request.POST中的相关数据对其进行修改
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_entry(id):
    """删除既有条目"""
    entry = Entry.objects.get(id=id)


def check_topic_owner(request, topic):
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        # 手动触发异常，没有请求资源，返回404响应
        raise Http404
