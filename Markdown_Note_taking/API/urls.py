from django.urls import path
from . import views
urlpatterns = [
    path('html/',views.md_to_html_view),
    path('grammar/',views.correct_grammar_view),
    path('save/',views.save_text_view),
    path('list/',views.Notes_view),
]
