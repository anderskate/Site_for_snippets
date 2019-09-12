from django.shortcuts import render
from .models import PieceOfCode, Snippet
from .forms import SnippetForm, CodeForm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.generic import View
from .tools import get_filename_from_cd, get_data_by_link

from .forms import CodeFormset

def snippets_list(request):
    snippets = Snippet.objects.all()
    paginator = Paginator(snippets, 2)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    languages_in_snippets = snippets.values('language')
    languages_in_snippets_formating = [i['language'] for i in languages_in_snippets]
    language_statistics = {
        'Python': languages_in_snippets_formating.count('py'),
        'Javascript': languages_in_snippets_formating.count('js'),
        'PHP': languages_in_snippets_formating.count('php'),
        'Java': languages_in_snippets_formating.count('java'),
        'Swift': languages_in_snippets_formating.count('swift'),
    }

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'language_statistics': language_statistics,
    }

    return render(request, 'catalog/base_catalog.html', context=context)


def snippet_datail(request, id):
    snippet = Snippet.objects.get(id=id)
    code_parts = snippet.pieceofcode_set.all()
    return render(
        request, 
        'catalog/snippet.html', 
        context={'snippet': snippet, 'code_parts': code_parts}
    )


class Snippet_Create(View):
    def get(self, request):
        snippet_form = SnippetForm()
        code_form = CodeFormset()

        return render(
            request, 
            'catalog/snippet_create_form.html', 
            context={'snippet_form': snippet_form, 'code_form': code_form,}
        )


    def post(self, request):
        bound_snippet_form = SnippetForm(request.POST)
        bound_code_form = CodeFormset(request.POST, request.FILES)

        if bound_code_form.is_valid() and bound_snippet_form.is_valid():
            
            last_post_data_element = list(request.POST.values())[-1]

            if request.POST['language'] == '' and len(request.FILES) > 0:
                uploaded_file = list(request.FILES.values())[0]
                extension_file = uploaded_file.name.split('.')[1]
                bound_snippet_form.cleaned_data['language'] = extension_file
            elif request.POST['language'] == '' and 'http' in last_post_data_element:
                link = last_post_data_element
                file_name = get_data_by_link(link).headers.get('content-disposition')
                extension_file = get_filename_from_cd(file_name).split('.')[1]
                bound_snippet_form.cleaned_data['language'] = extension_file

            new_snippet = bound_snippet_form.save()

            for form in bound_code_form:
                form.save(new_snippet)
            return redirect(new_snippet)

        return render(
            request, 
            'catalog/snippet_create_form.html',
            context={'snippet_form': bound_snippet_form, 'code_form': bound_code_form},
        )

