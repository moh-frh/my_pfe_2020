from django.forms import ModelForm, Textarea
from .models import Report

class ReportForm(ModelForm):

    class Meta:
        model = Report
        widgets = {
            'text': Textarea(attrs={'cols': 45, 'rows': 2}),
        }
        # fields = '__all__'
        fields = ['type', 'text']