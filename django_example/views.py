from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['simple_variable'] = 'hello world'
        context['dict_variable'] = {'hello': 'world'}
        return context
