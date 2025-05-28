from django.forms import TextInput, Widget
from django.template import loader
from django.utils.safestring import mark_safe


class InputWidget(TextInput):
    template_name = "widgets/input_widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class ColorPickerWidget(Widget):
    template_name = "widgets/color_picker_widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)