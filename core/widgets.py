from django.forms.widgets import Input

class RangeInput(Input):
    input_type = 'range'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'min' not in self.attrs:
            self.attrs['min'] = 0  # Default minimum value
        if 'max' not in self.attrs:
            self.attrs['max'] = 100  # Default maximum value
        if 'step' not in self.attrs:
            self.attrs['step'] = 1  # Default step value
