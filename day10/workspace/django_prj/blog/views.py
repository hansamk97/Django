from Tools.scripts.var_access_benchmark import C
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
from .models import Post, Category, Tag, Comment

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
    paginate_by = 5

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
        context['comment_form'] = CommentForm
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
# LoginRequiredMixin : 뷰 클래스에 추가하면,
# 해당 뷰에 접근하려는 사용자가 로그인이 되어 있어야 한다.
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    # Post의 필드에서 어떤한 것들을 정할 것인지
    fields = ['title', 'hook_text','content','head_image',
              'file_upload','category']

    # 오버라이드 기능
    # form_valid : form이 유효성 검사를 통과한 데이터를 처리할 때
    #              실행되는 로직을 담는다.
    def form_valid(self, form):
        # request : 파라미터에서 생략 가능
        current_user = self.request.user
        # is_authenticted : 속성은 사용자 객체가 인증되어
        # 로그인한 상태인지 아닌지를 판별하기 위해 사용
        if current_user.is_authenticated and ( current_user.is_staff or current_user.is_superuser ):
            # createView에서 만들어진 form의 instance에서
            # author부분에 current_user를 채운다.
            form.instance.author = current_user
            result = super(PostCreate,self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip() # 앞뒤 공백제거
                # 문자열을 ,로 분할하고 분할된 각 요소를
                # 리스트로 반환
                tags_list = tags_str.split(',')

                for t in tags_list:
                    t = t.strip()
                    print(t)
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    print("is_tag_created : ", is_tag_created)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return result
        else:
            return redirect('/blog/')

class PostUpdate(UpdateView):
    model = Post
    fields = ['title','hook_text', 'content', 'head_image',
              'file_upload','category']
    # 기본 페이지 : post_form.html, 게시글 등록 화면과 동일
    template_name = 'blog/post_update_form.html'

    # HTTP 요청에 대해 호출되는 메서드
    # HTTP 메서드에 다라 적절한 핸들러 메서드를 호출하고
    # 해당 메서드에서 뷰의 로직이 실행된다.
    def dispatch(self, request, *args, **kwargs):
        # get_object() : author를 획득
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            return PermissionDenied

    # get_context_data : HTTP요청이 왔을때 데이터 처리
    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()  # 빈 리스트 생성
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ','.join(tags_str_list)
        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()  # 앞뒤 공백제거
            # 문자열을 ,로 분할하고 분할된 각 요소를
            # 리스트로 반환
            tags_list = tags_str.split(',')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response

def new_comment(request, pk):
    # 로그인 여부 확인
    if request.user.is_authenticated:
        # get_object_or_404 : 알맞지 않은 pk값이 넘어오면
        # 404 error를 발생시킨다.
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            # 사용자가 입력한 comment를 가지고 
            # CommentForm의 인스턴스를 생성
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        return redirect(post.get_absolute_url())
    else :
        raise PermissionDenied

            
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate,self).dispatch(request, *args, **kwargs)
        else :
            return PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post

    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else :
        raise PermissionError

class PostSearch(PostList):
    paginate_by = None  # 페이징 처리 None

    def get_queryset(self):
        # class형에서 인자를 받아오는 방법
        # path('search/<str:q>/',views.PostSearch.as_view()) 에서
        # str:q 를 받아온다.
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            # title에서 검색, tag에서 검색, distinct()로 중복제거
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search:{q} ({self.get_queryset().count()})'
        return context



