from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text

class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    """ForeignKey()实例,外键是一个数据库术语，它引用了数据库中的另一条记录；这些代码将每个条目关联
        到特定的主题。每个主题创建时，都给它分配了一个键（或ID）。需要在两项数据之间建立联系时，
        Django使用与每项信息相关联的键"""
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """用于管理模型的额外信息"""
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        if len(self.text) < 50:
            return self.text
        else:
            return self.text[:50] + '...'
        # return self.text[:50] + "..."
