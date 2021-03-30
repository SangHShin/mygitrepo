from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
# import datetime

# Create your models here.
# # ---------------------------------- Question Class ---------------------------------- #

class Question(models.Model):   # 항상 Model 클래스를 상속받는다, pk(id) 는 자동으로 생성됨
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    voter = models.ManyToManyField(User, related_name='voter_question')

#     # pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.subject
#
#     # def was_published_recently(self):
#     #     # 날짜가 최근 24시간 이내 작성된거라면 True를 리턴한다.
#     #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#
# # ---------------------------------------------------------------------------- #
#from django.contrib.auth.models import User

class Answer(models.Model):   # 항상 Model 클래스를 상속받는다
    question = models.ForeignKey(Question, on_delete=models.CASCADE)   # 질문을 삭제 했을 때 연관 항목 - 자동 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

    def __str__(self):
        return self.content


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
