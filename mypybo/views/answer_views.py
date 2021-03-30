#from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from mypybo.models import Question, Answer
from mypybo.myForms import AnswerForm

from django.shortcuts import render, get_object_or_404, redirect, resolve_url

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    mypybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    #question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    #return redirect('mypybo:detail', question_id=question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user  # 추가한 속성 author 적용
            answer.save()
            #return redirect('mypybo:detail', question_id=question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('mypybo:detail', question_id=question.id), answer.id))

    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'mypybo/question_detail.html', context)

# def answer_create(request, question_id):
#     """
#     mypybo 답변등록
#     """
#     question = get_object_or_404(Question, pk=question_id)
#     if request.method == "POST":
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.create_date = timezone.now()
#             answer.question = question
#             answer.author = request.user  # 추가한 속성 author 적용
#             answer.save()
#             return redirect('mypybo:detail', question_id=question.id)
#     else:
#         form = AnswerForm()
#     context = {'question': question, 'form': form}
#     return render(request, 'mypybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    mypybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('mypybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            #return redirect('mypybo:detail', question_id=answer.question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('mypybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'mypybo/answer_form.html', context)



@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    mypybo 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다')
    else:
        answer.delete()
    return redirect('mypybo:detail', question_id=answer.question.id)