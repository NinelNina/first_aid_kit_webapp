from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Firstaidkit, MedicationUse, Disease, DiseaseCatalog, Symptom
from .models import Medicine


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email адрес'}))
    username = forms.CharField(label="", max_length="100", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Логин'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Логин не должен содержать больше 15 символов</span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted"><small><li>Пароль не должен содержать личную информацию</li><li>Пароль должен быть не менее 8 символов.</li><li>Пароль должен состоять из букв и цифр.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтверждение пароля'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Введите пароль ещё раз</span>'


class AddFirstAidKitRecord(forms.ModelForm):
    input_formats = ['%Y-%m', '%m/%Y', '%m.%y']
    expiration_date = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(attrs={'type': 'month', "placeholder": "Срок годности", "class": "form-control"}),
        label="",
        input_formats=input_formats
    )

    medicine = Medicine.objects.all().order_by('medicine_name')

    id_medicine = forms.ModelChoiceField(
        required=True,
        queryset=medicine,
        empty_label='Выберите лекарство',
        to_field_name='id_medicine',
        widget=forms.Select(),
        label=""
    )

    class Meta:
        model = Firstaidkit
        fields = ('id_medicine', 'expiration_date')

    def __init__(self, *args, **kwargs):
        super(AddFirstAidKitRecord, self).__init__(*args, **kwargs)
        self.fields['id_medicine'].widget.attrs['class'] = 'form-control'
        self.fields['id_medicine'].widget.attrs['placeholder'] = 'Название лекарства'
        self.fields['id_medicine'].label = ''

        self.fields['expiration_date'].widget.attrs['class'] = 'form-control'
        self.fields['expiration_date'].widget.attrs['placeholder'] = 'Срок годности'
        self.fields['expiration_date'].label = 'Срок годности'
        self.fields['expiration_date'].help_text = 'Введите срок годности в формате MM-YYYY'

        if self.instance.pk is not None:
            self.initial['id_medicine'] = self.instance.id_medicine
            self.initial['expiration_date'] = self.instance.expiration_date.strftime('%Y-%m')


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'medicine_descr']


class MedicationUseForm(forms.ModelForm):
    class Meta:
        model = MedicationUse
        fields = ['id_disease']

    def __init__(self, *args, **kwargs):
        super(MedicationUseForm, self).__init__(*args, **kwargs)
        self.fields['id_disease'].queryset = Disease.objects.all()


class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['id_disease', 'disease_name']


class DiseaseCatalogInlineForm(forms.ModelForm):
    class Meta:
        model = DiseaseCatalog
        fields = ['id_symptom']


class DiseaseSearchForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите симптомы',
    )
