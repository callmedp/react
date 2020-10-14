from django.views.generic import View
from django.shortcuts import render_to_response


class DesignPage(View):
    template_name = ''

    def get(self, request, *args, **kwargs):
        full_path = request.get_full_path()
        path = full_path.lstrip('/').split('?')
        tpl_path = path[0]
        self.template_name = self.template_name + tpl_path
        context = {}
        context.update({'test': 'TEST'})
        return render_to_response(
            self.template_name, context)


class FrontDesignPage(View):
    template_name = ''

    def get(self, request, *args, **kwargs):
        full_path = request.get_full_path()
        path = full_path.lstrip('/').split('?')
        tpl_path = path[0]
        self.template_name = self.template_name + tpl_path
        context = {}
        context.update({'test': 'TEST'})
        return render_to_response(
            self.template_name, context)
