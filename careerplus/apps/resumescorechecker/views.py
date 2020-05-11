from django.views.generic.base import TemplateView, View


class ScoreCheckerView(TemplateView):
    template_name = 'resumescorechecker/index.html'


class ScoreCheckerView2(TemplateView):
    template_name = 'resumescorechecker/inner.html'


class ScoreCheckerViewMobile(TemplateView):
    template_name = 'resumescorechecker/index.html'