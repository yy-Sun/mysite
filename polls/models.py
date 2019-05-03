from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    """
    问题：
    包含问题的详细描述和提出日期
    """
    question_text = models.CharField('问题内容', max_length=200)
    pub_date = models.DateTimeField('提出日期')

    def __str__(self):
        return self.question_text

    def is_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)


class Choice(models.Model):
    """
    选项:
    包含：问题，选项内容，支持人数
    问题是此选项的外键，一个选项（当前class）只能有一个问题，但一个问题可以有多个选项，从
    当前class来看，是多对一，使用ForeignKey
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Python中字段起名最好符合数据库的规则，因为数据库一般使用下划线，所以建议使用下划线
    choice_text = models.CharField('选项内容', max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
