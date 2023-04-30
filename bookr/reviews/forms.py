from django import forms

from .models import Publisher, Review


class SearchForm(forms.Form):
    initial = {'placeholder': "What are you looking for?"}
    search = forms.CharField(required=True, min_length=3,
                             widget=forms.TextInput(attrs={'placeholder': 'What are you looking for?'}))
    # search = forms.CharField(required=True, min_length=3, initial=initial['placeholder'])
    search_in = forms.ChoiceField(
        choices=(('title', 'Title'),
                 ('contributor', 'Contributor'),
                 ('isbn', 'ISBN')), required=False)


# class PublisherForm(forms.Form):
#     name = forms.CharField(max_length=30)
#     website = forms.URLField(help_text="Publisher's website")
#     email = forms.EmailField(help_text="Publisher's email address")

class PublisherForm(forms.ModelForm):
    # email_on_save = forms.BooleanField(required=False, initial=True, help_text="Zaznacz jeśli chcesz otrzymywać powiadomienia o nowych książkach tego wydawcy.")
    class Meta:
        model = Publisher
        fields = '__all__'
        widgets = {"name": forms.TextInput(attrs={'placeholder': 'Publisher name'})}
        # exclude = ()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {"creator": forms.TextInput(attrs={'placeholder': 'Your name'})}

    rating = forms.IntegerField(min_value=0, max_value=5)
