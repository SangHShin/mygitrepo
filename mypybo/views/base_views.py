from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from mypybo.models import Question
from django.db.models import Q, Count

def index(request):
    """
    mypybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
# ---------------------------------- [edit] ---------------------------------- #
    kw = request.GET.get('kw', '')  # 검색어 <--추가
# ---------------------------------- [edit] ---------------------------------- #
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 조회
    #question_list = Question.objects.order_by('-create_date')

    # 조회: 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')
# ---------------------------------------------------------------------------- #
    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
# ---------------------------------------------------------------------------- #

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    # context = {'question_list': question_list} #기존 질문목록 반환 객체
    # context = {'question_list': page_obj} #페이징에서 질문목록으로 page_obj가 반환됨
# ---------------------------------- [edit] ---------------------------------- #
    #context = {'question_list': page_obj, 'page': page, 'kw': kw}  # page와 kw가 추가되었다.
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}  # so가 추가되었다.
# ---------------------------------------------------------------------------- #

    #return HttpResponse("안녕하세요 mypybo에 오신 것을 환영합니다.")
    return render(request, 'mypybo/question_list.html', context)

def detail(request, question_id):
    """
    mypybo 내용 출력
    """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'mypybo/question_detail.html', context)