from django.forms import TextInput, Widget, Select, RadioSelect, DateInput
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


class DropdownWidget(Select):
    template_name = "widgets/dropdown_widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class RadioWidget(RadioSelect):
    template_name = "widgets/radio_widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class DatePickerWidget(DateInput):
    template_name = "widgets/date_picker_widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
