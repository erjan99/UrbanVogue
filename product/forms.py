from django import forms
from .models import Product, Brand, Color

class ProductCreationForm(forms.ModelForm):
    brand_name = forms.CharField(
        label='Brand',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'brand-options',
            'placeholder': 'Select or enter brand name'
        })
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'available_sizes', 'available_colors', 'gender', 'main_image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter product description'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'available_sizes': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'available_colors': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input d-none'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'main_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        brand_name = self.cleaned_data['brand_name'].strip()
        brand, _ = Brand.objects.get_or_create(name=brand_name)
        product.brand = brand

        if commit:
            product.save()
            self.save_m2m()

        return product
