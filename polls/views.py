from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context=context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'last_question_list'

    def get_queryset(self):
        """
        pub_date__lte less than or equal,返回pub_date小于等于当前时间的questions，并排序
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


class DetailView(generic.DeleteView):
    """
    Question的pub_datetime如果比现在的时间晚，那么久不应该被展示
    """
    model = Question
    template_name = 'polls/detail.html'

    # 重写、覆盖过滤器，然后再根据pk取值 def get_object(self, queryset=None):
    def get_queryset(self):
        """
        如果不存在或者Question的时间比当前时间晚，则返回404
        :return: Question or 404
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DeleteView):
    model = Question
    template_name = 'polls/results.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {'question': question, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
