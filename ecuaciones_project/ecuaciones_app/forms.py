from django import forms

class EcuacionesForm(forms.Form):
    num_variables = forms.ChoiceField(choices=[(i, i) for i in range(2, 5)], label='Sumas', initial=3)
    suma_maxima = forms.IntegerField(min_value=1, max_value=99999, label='Máximo', initial=10,
                                     widget=forms.NumberInput(attrs={'style': 'width: 100px'}))
    num_ejercicios = forms.ChoiceField(choices=[(i, i) for i in range(1, 10)], label='Ejercicios', initial=1)
