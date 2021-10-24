from django import forms

from .models import Report


# 表示页面用。fields 的字段直接取自 models.py的字段
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'remarks')
