from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(
        choices=(('title', 'Title'),
                 ('contributor', 'Contributor'),
                 ('isbn', 'ISBN')), required=False)