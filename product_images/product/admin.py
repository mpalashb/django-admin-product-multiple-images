# from django.contrib import admin
# from .models import (
#     Product,
#     ProductImage,
# )
# # Register your models here.

# admin.site.register(Product)
# admin.site.register(ProductImage)

from django.contrib import admin
from django import forms
from django.http import HttpRequest
from django.http.response import HttpResponse
from .models import Product, ProductImage


class ProductAdminForm(forms.ModelForm):
    # images = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    change_form_template = 'admin/product/new_change_form.html'
    form = ProductAdminForm

    class Media:
        js = ('admin/js/products.js', )
        css = {'all': ('admin/css/products.css', )}

    def change_view(self, request: HttpRequest, object_id: str, form_url: str = '', extra_context: dict[str, bool] | None = None) -> HttpResponse:
        product = Product.objects.get(id=object_id)
        # Retrieve all related ProductImage objects
        all_images = product.all_images.all()
        extra_context = {
            'all_images': all_images
        }

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Process uploaded images
        if 'images' in request.FILES:
            ProductImage.objects.filter(product=obj).all().delete()
            for f in request.FILES.getlist('images'):

                ProductImage.objects.get_or_create(product=obj, image=f)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
