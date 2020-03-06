from django.views.generic.base import TemplateView, View


class ScoreCheckerView(TemplateView):
    template_name = 'resumescorechecker/index.html'
