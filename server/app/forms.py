from django import forms
from .models import Items, Images
from multiupload.fields import MultiFileField


class ItemForm(forms.ModelForm):
    files = MultiFileField(min_num=1, max_num=4, max_file_size=1024 * 1024 * 5)

    def save(self, commit=True):
        instance = super(ItemForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Images.objects.create(image=each, item=instance)

        return instance

    class Meta:
        model = Items
        fields = ['name', 'price', 'category', 'rating', 'quantity_in_stock']
