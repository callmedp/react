from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.

class SkillPageView(TemplateView):
	template_name = "skillpage/skill.html"

	def get(self, request, *args, **kwargs):
		return super(SkillPageView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		return super(SkillPageView, self).get_context_data(**kwargs)

