from django.urls import path
from .views import snippets_list, Snippet_Create, snippet_datail

urlpatterns = [
	path('', snippets_list, name='snippets_list_url'),
	path('snippet/create/', Snippet_Create.as_view(), name='snippet_create_url'),
	path('snippet/<str:id>/', snippet_datail, name='snippet_datail_url'),
]