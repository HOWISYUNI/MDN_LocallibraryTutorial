import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _ # ValidationError에 _(underbar)를 사용하기위한 작업

# 일반 Form : 직접 필드정의, 위젯 설정이 필요
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3)")

    # 클린함수 : view에서 is_valid()함수가 호출될 때 동작하는 함수. 클린함수에는 3가지가 있다.
    # 클린함수의 3가지 종류에 대해서는 https://docs.djangoproject.com/en/3.1/ref/forms/validation/ 참고
    # renewal_date의 유효성(4주안의 기간을 설정했는가) 체크
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


# ModelForm : forms을 간단히 만드는 방법, 모델과 필드를 지정하면 자동으로 폼 필드 생성
# https://developer.mozilla.org/ko/docs/Learn/Server-side/Django/Forms  의 ModelForms 확인