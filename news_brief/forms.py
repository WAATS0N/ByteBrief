from django import forms

class NewsBriefForm(forms.Form):
    SOURCES_CHOICES = [
        ('bbc', 'BBC News'),
        ('cnn', 'CNN'),
        ('reuters', 'Reuters'),
        ('techcrunch', 'TechCrunch'),
        ('guardian', 'The Guardian'),
    ]
    
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('business', 'Business'),
        ('politics', 'Politics'),
        ('science', 'Science'),
        ('health', 'Health'),
        ('entertainment', 'Entertainment'),
        ('sports', 'Sports'),
    ]
    
    keywords = forms.CharField(
        label='Specific Keywords (Optional)', 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. SpaceX, Election, AI'})
    )
    
    categories = forms.MultipleChoiceField(
        label='Select Categories',
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    sources = forms.MultipleChoiceField(
        choices=SOURCES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        initial=['bbc', 'cnn', 'reuters', 'techcrunch', 'guardian']
    )
