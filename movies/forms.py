from django import forms
from .models import Review, SearchedDate


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['content', 'score', ]


class SearchedDateForm(forms.ModelForm):

    date = forms.DateField(
        widget = forms.DateInput(format='%m/%d'),
        input_formats=('%m/%d'),
    )

    class Meta:
        model = SearchedDate
        fields = ['date', ]