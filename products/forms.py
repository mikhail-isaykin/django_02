from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Email должен оканчиваться на @gmail.com')
        return email

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError('Cообщение не может быть короче 10 символов')
        return message
