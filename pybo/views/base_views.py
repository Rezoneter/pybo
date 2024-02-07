from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question

def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '') # index word
    question_list = Question.objects.order_by('-create_date')
    # 작성일시의 역순(최신순)으로 정렬, -가 붙으면 역, 없으면 순방향으로 정렬한다
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'page':page, 'kw':kw}
    # context = {'question_list': question_list}
    return render(request,'pybo/question_list.html', context)
    # render 는 파이썬 데이터를 템플릿에 적용하여 HTML  로 반환하는 함수
    # quetions_list 데이터를 question_list.html 파일에 적용,
    # HTML 을 생성한 후 리턴

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context= {'question':question}
    return render(request, 'pybo/question_detail.html', context)
    # question_id 매개변수 추가, URL 매핑시 전달
