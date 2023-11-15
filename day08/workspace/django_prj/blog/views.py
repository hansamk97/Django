from Tools.scripts.var_access_benchmark import C
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import Post, Category, Tag

# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     return render(request, 'blog/index.html',{'abc':posts})

class PostList(ListView):
    # ListView : model 속성에 어떤 모델의 데이터를 보여줄지 작성
    #            model_list.html 화면 기본값
    #            model_list 변수를 사용해서 템플릿에서 객체 리스트 엑세스

    # template_name = 'blog/index.html'
    # context_object_name = 'abc'
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        # 부모 클래스의 get_context_data()를 호출, 딕셔너리
        context = super(PostList, self).get_context_data()
        # categories라는 키를 가진 context 딕셔너리에 모든 
        # Category 객체를 값으로 추가
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/single_page.html'
#                   ,{'post':post})

class PostDetail(DetailView):
    model = Post
    # template_name = 'blog/single_page.html' # 모델_detail.html
    # post 변수를 사용해서 템플릿에서 객체 접근 가능

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)


    return render(request, 'blog/post_list.html',
            {'category'     : category,
             'post_list'    : post_list,
             'categories'   : Category.objects.all(),
             'no_category_post_count':Post.objects.filter(category=None).count()
        })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all() # tag와 관련된 모든 post list return

    return render(request, 'blog/post_list.html',{
        'post_list' : post_list,
        'categories': Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        'tag' : tag
    })

# insert 화면에서 입력값을 입력받아서 저장
class PostCreate(CreateView):
    model = Post
    # Post의 필드에서 어떤한 것들을 정할 것인지
    fields = ['title', 'hook_text','content','head_image',
              'file_upload','category']




