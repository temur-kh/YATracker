from django import forms


class AuthorizationForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):

    USER_TYPES = (
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
        ('Admin', 'Admin'),
    )

    name = forms.CharField(label="Name", required=True)
    surname = forms.CharField(label="Surname", required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Repeat password", required=True, widget=forms.PasswordInput)
    user_type = forms.ChoiceField(label='I am ...', required=True, widget=forms.Select, choices=USER_TYPES)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password != password_repeat:
            self.add_error(
                'password_repeat',
                "Passwords don't match"
            )

        return cleaned_data
