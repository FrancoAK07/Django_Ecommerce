from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="Full Name", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Full Name'}), required=True)
    shipping_email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Email'}), required=True)
    shipping_address1 = forms.CharField(label="Address 1", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Address 1'}), required=True)
    shipping_address2 = forms.CharField(label="Address 2", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Address 2'}), required=False)
    shipping_city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'City'}), required=True)
    shipping_state = forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'State'}), required=False)
    shipping_zipcode = forms.CharField(label="Zipcode", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Zipcode'}), required=False)
    shipping_country = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ["shipping_full_name", "shipping_email", "shipping_address1", "shipping_address2", "shipping_city", "shipping_state", "shipping_zipcode", "shipping_country"]
        exclude = ["user",]

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="Card Name", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Card Name'}), required=True)
    card_number = forms.CharField(label="Card Number", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Card Number'}), required=True)
    card_exp_date = forms.CharField(label="Expiration Date", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Expiration Date'}), required=True)
    card_cvv_number = forms.CharField(label="CVV Number", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'CVV Number'}), required=True)
    card_address1 = forms.CharField(label="Address 1", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Address 1'}), required=True)
    card_address2 = forms.CharField(label="Address 2", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Address 2'}), required=False)
    card_city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Billing City'}), required=True)
    card_state = forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Billing State'}), required=True)
    card_zipcode = forms.CharField(label="Zipcode", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Zipcode'}), required=True)
    card_country = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'w-full ps-2', 'placeholder':'Billing Country'}), required=True)
