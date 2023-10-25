from django import forms
from .models import Category, Product, SubCategory, Brand
# from allauth.account.forms import SignupForm

# class register(SignupForm):
#     name = forms.CharField(max_length=30, label='First Name')
    
#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.save()
#         return user
class new_product(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('instock',)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['brand'] = forms.CharField(max_length=128, label='Brand')
        
        if 'category' in self.data:
            try:
                id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category__id=id)
            except (ValueError, TypeError):
                pass
        elif self.instance.category_id:
            self.fields['subcategory'].queryset = self.instance.category.subcategories
    
    def clean_brand(self):
        '''
            form method to deal with Brand instances as the site is designed
            to allow product owners to add new brands if brand doesn't exists
            new brand is created and returned to form for addition
        '''
        brand_name = self.cleaned_data.get("brand",  False)
        if brand_name:
            name = brand_name.lower().capitalize()
            if Brand.objects.filter(name=name).exists():
                brand = Brand.objects.get(name=name)
            else:
                brand = Brand.objects.create(name=name)
            return brand
        else:
            raise ValueError
        
# class new_product(forms.Form):
#   name = forms.CharField(max_length=128, label='Product name')
#   price = forms.DecimalField(max_digits=7, decimal_places=2, label='Price')
#   stock = forms.IntegerField(initial=0)
#   category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.TextInput(attrs={'id': 'category'}))
#   subcategory = forms.ModelChoiceField(queryset= ,widget=forms.TextInput(attrs={'id': 'sub_category'}))
#   brand = forms.CharField(max_length=128, label='Brand')
#   description = forms.CharField(max_length=4096, label='Description')
#   picture = forms.ImageField(upload_to="img")
    