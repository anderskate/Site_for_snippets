from django.contrib import admin
from .models import Snippet, PieceOfCode


admin.site.register(PieceOfCode)

class PiecesOfCodeInline(admin.TabularInline):
	model = PieceOfCode
	extra = 1

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
	inlines = [PiecesOfCodeInline]