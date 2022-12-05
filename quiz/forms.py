from django import forms

from quiz.models import QuizCategory, QuizQuestion

class QuizCategoryForm(forms.ModelForm):

    class Meta:
        model = QuizCategory
        fields = ['title', 'image']
        widgets = {
            'title' : forms.TextInput(attrs = {'placeholder' : 'Category Title', 'class' : 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(QuizCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class QuizQuestionForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = QuizQuestion
        fields = ['category', 'question', 'option_1', 'option_2', 'option_3', 'option_4', 'time_limit', 'answer']
        widgets = {
            'question' : forms.Textarea(attrs = {'rows' : 2}),
            'option_1' : forms.Textarea(attrs = {'rows' : 3}),
            'option_2' : forms.Textarea(attrs = {'rows' : 3}),
            'option_3' : forms.Textarea(attrs = {'rows' : 3}),
            'option_4' : forms.Textarea(attrs = {'rows' : 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(QuizQuestionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'