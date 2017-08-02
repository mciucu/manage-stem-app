import json

from django.shortcuts import render
from establishment.funnel.state import State
from establishment.funnel.base_views import single_page_app, global_renderer


def render_ui_widget(request, widget_class, state=None, page_title=None, widget_require=None, widget_options={}):
    context = {}
    if state:
        context["state"] = state.dumps()
    else:
        context["state"] = "{}"

    if widget_class == "MessagesPanel":
        widget_class = "AppClass"
        widget_require = "Bundle"

    # TODO: DEFAULT_PAGE_TITLE should be an option in settings
    context["page_title"] = page_title or "{{project_full_name}}"
    context["widget_class"] = widget_class
    context["widget_require"] = widget_require or widget_class
    context["widget_options"] = json.dumps(widget_options)

    return render(request, "{{project_main_app}}/ui_widget.html", context)


global_renderer.render_ui_widget = render_ui_widget

@single_page_app
def index(request):
    return State()
