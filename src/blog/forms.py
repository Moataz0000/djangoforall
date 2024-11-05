from django import forms 
from .models import Comment, Subscription




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'border border-gray-300 rounded-md p-4 w-full shadow-sm focus:ring focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }






class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
     