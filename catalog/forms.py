from django import forms
from .models import PieceOfCode, Snippet
from django.core.exceptions import ValidationError
from .tools import (
    get_filename_from_cd, 
    check_file_extension,
    get_data_by_link,
    get_filename
)

from django.forms import formset_factory
from django.forms.formsets import BaseFormSet

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ('title', 'status', 'language')

    def save(self):
        new_snippet = Snippet.objects.create(
            title = self.cleaned_data['title'],
            status = self.cleaned_data['status'],
            language = self.cleaned_data['language'],
        )
        return new_snippet


class CodeForm(forms.Form):
    code = forms.CharField(label='Код', widget=forms.Textarea, required=False)
    file = forms.FileField(label='Файл', required=False)
    link_to_file = forms.CharField(label='Ссылка на файл', required=False)

    def clean(self):
        cleaned_data = super().clean()

        code = cleaned_data.get('code')
        file = cleaned_data.get('file')
        link_to_file = cleaned_data.get('link_to_file')


        if code == '' and file == link_to_file == None:
            raise forms.ValidationError(
                'Введите код сниппета в поле ниже, загрузите файл или укажите ссылку на файл кода'
            )


    def clean_file(self):
        if self.cleaned_data['file'] is not None:
            new_file = self.cleaned_data['file']
            max_size = 5000
            if new_file.size > max_size:
                raise ValidationError('Большой размер файла')
            if not check_file_extension(new_file.name):
                raise ValidationError('Данное расширение файла не поддерживается')

            file_data = new_file.read().decode("utf-8")
            return file_data



    def clean_link_to_file(self):
        if self.cleaned_data['link_to_file'] != '':
            new_link = self.cleaned_data['link_to_file']

            if 'http://' not in new_link and 'https://' not in new_link:
                raise ValidationError('Некорректная ссылка. Введите с "http://"')

            data = get_data_by_link(new_link)
            if data == False:
                raise ValidationError('Нет доступа по данной ссылке')
            header = data.headers

            content_type = header.get('content-type')

            if 'text/html' in content_type.lower():
                raise ValidationError('Данная ссылка не для загрузки файла')

            content_length = header.get('content-length', None)
            max_size = 5000
            if int(content_length) > max_size:
                raise ValidationError('Большой размер файла')

            filename = get_filename(data)

            if not check_file_extension(filename):
                raise ValidationError('Данное расширение файла не поддерживается')

            file_data = data.content.decode("utf-8")
            return file_data
        

    def save(self, new_snippet):
        if self.cleaned_data['code'] != '':
            code = self.cleaned_data['code']
        elif self.cleaned_data['file'] != None:
            code = self.cleaned_data['file']
        elif self.cleaned_data['link_to_file'] != None:
            code = self.cleaned_data['link_to_file']

        new_code = PieceOfCode.objects.create(
            snippet = new_snippet,
            code = code,
        )


class CodeRequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(CodeRequiredFormSet, self).__init__(*args, **kwargs)

        for form in self.forms:
            form.empty_permitted = False


CodeFormset = formset_factory(CodeForm, formset=CodeRequiredFormSet, extra=1, max_num=5)
