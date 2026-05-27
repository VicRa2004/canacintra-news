from django import forms
from .models import Comment, News, Category, NewsImage
from django_ckeditor_5.widgets import CKEditor5Widget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and self.errors:
            for field in self.errors:
                if field in self.fields:
                    widget = self.fields[field].widget
                    existing = widget.attrs.get('class', '')
                    widget.attrs['class'] = f"{existing} is-invalid".strip()

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del artículo'}),
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='extends'),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = True
        if self.is_bound and self.errors:
            for field in self.errors:
                if field in self.fields:
                    widget = self.fields[field].widget
                    existing = widget.attrs.get('class', '')
                    widget.attrs['class'] = f"{existing} is-invalid".strip()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la categoría...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and self.errors:
            for field in self.errors:
                if field in self.fields:
                    widget = self.fields[field].widget
                    existing = widget.attrs.get('class', '')
                    widget.attrs['class'] = f"{existing} is-invalid".strip()

class NewsImageForm(forms.ModelForm):
    class Meta:
        model = NewsImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pie de foto'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and self.errors:
            for field in self.errors:
                if field in self.fields:
                    widget = self.fields[field].widget
                    existing = widget.attrs.get('class', '')
                    widget.attrs['class'] = f"{existing} is-invalid".strip()

