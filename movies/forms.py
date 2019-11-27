from django import forms
from .models import Review, SearchedDate


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['score'].widget.attrs['max'] = 5
        self.fields['score'].widget.attrs['min'] = 1
        self.fields['content'].widget.attrs['placeholder'] = '댓글을 입력하세요.'
        self.fields['content'].widget.attrs['size'] = 60
        self.fields['score'].widget.attrs['size'] = 10

    class Meta:
        model = Review
        fields = ['content', 'score', ]


class SearchedDateForm(forms.ModelForm):

    class Meta:
        model = SearchedDate
        fields = ['month', 'day', ]
