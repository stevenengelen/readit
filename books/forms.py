from django import forms
from .models import Book

class ReviewForm(forms.Form) :
    """
    Form for revewing a book
    """

    is_favourite = forms.BooleanField(
            label = 'Favourite?',
            help_text = 'In your top 100 book of all time?',
            required = False,
    )

    review = forms.CharField(
            widget = forms.Textarea,
            min_length = 300,
            error_messages = {
                'required' : 'Please enter your review',
                'min_length' : 'Please write at least 300 characters (you have written %(show_value)s)' }
    )

class BookForm(forms.ModelForm) :
    # provide some meta information
    class Meta :
        # first, the model to use in in this model form
        model = Book
        # and the field of the model to display (default displays all fields)
        fields = ['title', 'authors']

