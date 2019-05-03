import datetime
from django.test import TestCase
from .models import Question
from django.utils import timezone
from django.urls import reverse


class QuestionModelTests(TestCase):
    def test_is_published_recently_with_future_question(self):
        """
        如果Question的提出时间pub_date是未来时间，应该返回false
        :return: False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published_recently(), False)

    def test_is_published_recently_with_old_question(self):
        """
        问题的提出时间与现在时间在一天之外，应该返回false
        :return: false
        """
        old_time_limit = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=old_time_limit)
        self.assertIs(old_question.is_published_recently(), False)

    def test_is_published_recently_with_recent_question(self):
        """
        问题的提出时间与现在时间在一天之内，应该返回True
        :return: True
        :return:
        """
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.is_published_recently(), True)


def create_question(question_text, days):
    """
    公用的快捷函数，生成一个基于当前时间并增加days天的Question
    这里生成的数据都是填充到一个临时测试环境数据，并不会影响正式数据，测试环境下也不会
    从正式环境取数据
    :param question_text: 创建Question的question_text参数
    :param days: 推迟的天数
    :return: Question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    # 向数据库中中插入一个Question对象/数据
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """
    测试视图view是否正确返回，包含测试response的返回状态码，返回的text内容，Query返回集/对象
    """

    def test_no_questions(self):
        """
        如果没有question，应该返回空的QuerySet
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['last_question_list'], [])

    def test_past_question(self):
        """
        如果一个Question是过去的，应该被显示
        """
        create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['last_question_list'],
                                 ['<Question: Past question.>'])

    def test_future_question(self):
        """
        如果一个Question是将来时间的，应该不被显示
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['last_question_list'], [])

    def test_future_and_past_question(self):
        """
        如果过去的问题和将来的问题同时存在，应该只显示已经发生的（过去的）
        """
        # create_question(question_text='Past question.', days=-30)
        # create_question(question_text='Future question.', days=30)
        # response = self.client.get(reverse('polls:index'))
        # self.assertEqual(response.context['last_question_list'],
        #                  ['<Question: Past question.>'])

        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['last_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        有两个已经发生的question对象，应该都显示
        """
        create_question(question_text='Past question1', days=-10)
        create_question(question_text='Past question2', days=-20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['last_question_list'],
                                 ['<Question: Past question1>', '<Question: Past question2>'])


class QuestionDetialViewTests(TestCase):
    def test_future_question(self):
        """
        访问一个时间是比当前晚的Question，应该返回404
        """
        future_question = create_question(question_text='Future Question', days=20)
        response = self.client.get(reverse('polls:detail', args=(future_question.pk,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        访问一个时间是比当前早（已经发生）的Question，应该正常返回
        """
        past_question = create_question(question_text='Past question', days=-10)
        response = self.client.get(reverse('polls:detail', args=(past_question.pk,)))
        self.assertContains(response, past_question.question_text)
