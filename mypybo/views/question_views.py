from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from mypybo.models import Question
from mypybo.myForms import QuestionForm


@login_required(login_url='common:login')
def question_create(request):
    """
    mypybo 질문등록
    """
    if request.method == 'POST':
      # form = QuestionForm()
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user  # 추가한 속성 author 적용
            question.save()
            return redirect('mypybo:index')
    else:
        form = QuestionForm()  #요청이 POST가 아닐 경우(DELETE, PUT이면???
    context = {'form': form}
    #return render(request, 'mypybo/question_form.html', {'form': form})
    return render(request, 'mypybo/question_form.html', context)

# from django.views import generic
#
# class IndexView(generic.ListView):
#     """
#     pybo 목록 출력
#     """
#     def get_queryset(self):
#         return Question.objects.order_by('-create_date')
#
#
# class DetailView(generic.DetailView):
#     """
#     pybo 내용 출력
#     """
#     model = Question

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    mypybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('mypybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)  #질문수정을  위해 값 덮어쓰기
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('mypybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  #질문 수정화면에 기존 제목 내용 반영을 위해 인스턴스 객체 사용
    context = {'form': form}
    return render(request, 'mypybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    mypybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('mypybo:detail', question_id=question.id)
    question.delete()
    return redirect('mypybo:index')

