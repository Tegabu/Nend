from django import forms

from .models import Listing, ChatMessage

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }


class NewListing(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('category', 'name', 'description',
                  'location', 'charge', 'img', 'is_available')
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'img': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-500file: mr-4 file: py-2 file: px-4 file: rounded-full file: border-0 file: text-sm file: font-semibold file: bg-violet-50 file: text-violet-700hover: file: bg-violet-100',

            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,

            }),
            'name': forms.Textarea(attrs={
                'class': INPUT_CLASSES,

            }),
            'is_available': forms.NullBooleanSelect(attrs={
                'class': INPUT_CLASSES,
            }),
            'location': forms.Textarea(attrs={
                'class': INPUT_CLASSES,

            }),
            'charge': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,

            }),
        }


class EditListing(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('name', 'description',
                  'location', 'charge', 'img', 'is_available')
        widgets = {

            'img': forms.FileInput(attrs={
                'class': 'form-control',

            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 70px'
            }),
            'name': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 30px'
            }),
            'is_available': forms.NullBooleanSelect(attrs={
                'class': 'form-control',
            }),
            'location': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 30px'
            }),
            'charge': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'height: 30px'
                'display: flex'
                'flex-direction: row'
                'color: blue'
            }),
        }
