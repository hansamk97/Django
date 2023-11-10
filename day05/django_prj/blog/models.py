from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50) # 제목
    content = models.TextField()            # 내용
    created_at = models.DateTimeField(auto_now_add=True)     # 작성일
    updated_at = models.DateTimeField(auto_now=True)
    # author : 작성자 추후 작성

    def __str__(self):
        return f'[{self.pk}] {self.title}'

    # 사용자 정의 함수
    # get_absolute_url은 장고에서 권장하는 관례
    # 모델의 인스턴스를 대표하는 URL응ㄹ 반환하기 위해 
    # get_absolute_url()을 작성하는 것을 권장
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'






