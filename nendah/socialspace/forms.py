from django import forms

from .models import Listing

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'


class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('category', 'name', 'description',
                  'location', 'charge', 'img', 'is_available')
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            })
        }
