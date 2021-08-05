from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):  # ModelForm根据模型创建表单，一直表单中包含的字段
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}