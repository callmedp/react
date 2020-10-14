from django import forms
from ckeditor.widgets import CKEditorWidget
from django.forms import inlineformset_factory

from shop.models import Category, ProductCategory, Product


class SkillAddForm(forms.ModelForm):
    name = forms.CharField(label=("Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    slug = forms.SlugField(label=("Slug:"), max_length=90,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    description = forms.CharField(required=True, widget=CKEditorWidget())

    video_link = forms.CharField(label=("Video Link"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    career_outcomes = forms.CharField(label=("Career Outcomes"),
        help_text='semi-colon(;) separated designations, e.g. Project Engineer; Software Engineer; ...', 
        max_length=500,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    graph_image = forms.FileField(label=("Graph Image:"), max_length=100, required=False)


    active = forms.BooleanField(label=("Active:"),
        widget=forms.CheckboxInput())
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'video_link',
        'career_outcomes', 'graph_image', 'active', 'categoryproducts']
        
    def __init__(self, *args, **kwargs):
        super(SkillAddForm, self).__init__(*args, **kwargs)
        self.fields['active'].required = False

    def clean(self):
        fields = ['name', 'slug']
        for field in fields:
            try:
                val = self.cleaned_data.get(field).strip()
                self.cleaned_data[field] = val
            except Exception as e:
                continue
        return super(SkillAddForm, self).clean()

    def save(self, commit=True):
        skill = super(SkillAddForm, self).save(commit=False)
        if commit:
            skill.save()
            categoryproducts = self.cleaned_data['categoryproducts']
            for categoryproduct in categoryproducts:
                ProductCategory.objects.get_or_create(
                    category=skill, product=categoryproduct, active=True)
        return skill


# class ProductCategoryForm(forms.ModelForm):
#     product = forms.ModelChoiceField(label=(""),
#         queryset=Product.objects.filter(active=True), to_field_name='pk', required=True, widget=forms.Select(
#         attrs={'class': ''}))

#     class Meta:
#         model = ProductCategory
#         fields = ['product', 'is_main', 'prd_order', 'active', 'cat_order']

# ProductFormSet = inlineformset_factory(Category, ProductCategory,
#     form=ProductCategoryForm, extra=1, max_num=18)
