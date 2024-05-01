from django import forms


class ConnectForm(forms.Form):
    TXNCRNCY = forms.CharField(max_length=3)
    TXNAMT = forms.IntegerField()
    REMARKS = forms.CharField(max_length=50)
