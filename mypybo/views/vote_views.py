from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from mypybo.models import Question

@login_required(login_url='common:login')
def vote_question(request, question_id):
    """
    mypybo 질문 추천 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('mypybo:detail', question_id=question.id)

from mypybo.models import Answer

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
    mypybo 답글 추천 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('mypybo:detail', question_id=answer.question.id)

