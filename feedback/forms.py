from django import forms
from .models import Feedback

class FeedbackFrom(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'flex-space-x-2'}),
        label='How would you rate this translation?'
    )
    class Meta:
        model = Feedback
        fields = ['rating','comments']
        widgets =  {
            'comments': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full border rounded p-2',
                'placeholder': 'Your suggestions for improvements...',
            })
        } 
        labels = {
            'comments': 'Additional comments'
        }
        