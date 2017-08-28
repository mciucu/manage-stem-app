from django.shortcuts import render
from establishment.webapp.state import State
from establishment.webapp.base_views import single_page_app, global_renderer


def render_single_page_app(request):
    return render(request, "{{project_main_app}}/app.html", {})


global_renderer.render_single_page_app = render_single_page_app


@single_page_app
def index(request):
    return State()
