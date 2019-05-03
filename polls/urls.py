from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # 当在polls后传入一个int类型的参数，参数名为question_id
    # /polls/5
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # 当在polls后传入一个int类型的参数，参数名为question_id,并在后面跟results路径
    # 注意URL必须以/结尾
    # /polls/2/results
    path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),
    # example /polls/3/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
