from django import forms


class GithubForm(forms.Form):

    search_field = forms.CharField(max_length=20, required=True,
                                   help_text='search github stars',
                                   label='github_search',)
