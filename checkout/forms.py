from django import forms
from main.models import Address
from .models import Order
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class new_address(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your Lirst name'}))
    phone_number = forms.CharField(widget=PhoneNumberPrefixWidget(country_choices=[
                ("EG", "Eg +20"),
                ("US", "USA +1"),
                ("TR", "TR +90"),
                ],
                attrs={'placeholder':'Phone number'}))
    phone_number2= forms.CharField(widget=PhoneNumberPrefixWidget(country_choices=[
                ("EG", "Eg +20"),
                ("US", "USA +1"),
                ("TR", "TR +90"),
                ],
                attrs={'placeholder':'additional phone number'}))
    address= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your Address'}))
    additional_info= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Side Notes'}))
    class Meta:
        model = Address
        exclude = ('user',)
        labels = {
        "phone_number": "Phone Number",
        "phone_number2": "Phone Number 2",
        "first_name": "First Name",
        "last_name": "Last Name"   
        }
    
    
    required_css_class = 'required'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.widgets[0].attrs['class'] = 'col-2 h-100'
        self.fields['phone_number'].widget.widgets[1].attrs['class'] = 'col-9 float-end'
        self.fields['phone_number2'].widget.widgets[0].attrs['class'] = 'col-2 h-100'
        self.fields['phone_number2'].widget.widgets[1].attrs['class'] = 'col-9 float-end'
        self.fields['phone_number2'].required = False
        self.fields['additional_info'].required = False

