from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post

# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     return render(request, 'blog/index.html',{'abc':posts})

class PostList(ListView):
    # ListView : model 속성에 어떤 모델의 데이터를 보여줄지 작성
    #            model_list.html 화면 기본값
    #            model_list 변수를 사용해서 템플릿에서 객체 리스트 엑세스
    model = Post
    ordering = '-pk'
    # template_name = 'blog/index.html'
    # context_object_name = 'abc'


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/single_page.html'
#                   ,{'post':post})

class PostDetail(DetailView):
    model = Post
    # template_name = 'blog/single_page.html' # 모델_detail.html
    # post 변수를 사용해서 템플릿에서 객체 접근 가능





