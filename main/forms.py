from django import forms
from .models import Category, Product, SubCategory, Brand


class new_product(forms.ModelForm):
    '''handle new products addition through HTML Form'''
    class Meta:
        model = Product
        exclude = ('instock','active')

    
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
    