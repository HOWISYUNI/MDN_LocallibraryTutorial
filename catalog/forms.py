import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _ # ValidationError에 _(underbar)를 사용하기위한 작업


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3)")

    # renewal_date의 유효성(4주안의 기간을 설정했는가) 확인하는 메서드
    def clean_renewal_date(self):

        # 검증에 성공한 값은 사전타입으로 form.cleaned_data 라는 변수를 제공
        data = self.cleaned_data['renewal_date']

        # 과거 체크
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # 4주 안의 기간인지 체크
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more tha 4 weeks ahead'))

        # 모든 유효성을 통과하면 리턴
        return data