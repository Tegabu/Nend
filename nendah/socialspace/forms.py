from django import forms

from .models import Listing

INPUT_CLASSES = 'bg-gray-50 border border-gray-300 py-4 px-6 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-white-400 dark:border-gray-600 dark:placeholder-gray-400 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500'


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
                'class': "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-white-700 dark:border-gray-600 dark:placeholder-gray-400",

            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 4,
                'cols': 100,
            }),
            'name': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 1,
                'cols': 100,
            }),
            'is_available': forms.NullBooleanSelect(attrs={
                'class': INPUT_CLASSES
            }),
            'location': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 1,
                'cols': 100,
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
                'class': INPUT_CLASSES,

            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 4,
                'cols': 100,

            }),
            'name': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 1,
                'cols': 100,

            }),
            'is_available': forms.NullBooleanSelect(attrs={
                'class': INPUT_CLASSES,
            }),
            'location': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 1,
                'cols': 100,
            }),
            'charge': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
            }),
        }
