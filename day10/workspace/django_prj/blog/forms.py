from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    # Meta클래스는 ModelForm의 메타데이터를 정의하는데 사용
    class Meta:
        model = Comment
        fields = ('content',) # 포함시킬 필드만 가지고 온다.