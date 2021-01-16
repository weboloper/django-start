from core.models import Attachment
from django import forms

class AttachmentUploadForm(forms.ModelForm):
    class Meta:
        model = Attachment
        guid = forms.FileField()
        fields = ('guid',)
    
    def clean(self):
        
        cleaned_data = super(AttachmentUploadForm, self).clean()
        print(cleaned_data)
        return cleaned_data

    def save(self, *args, **kwargs):
        
        # doc = self.cleaned_data['document']

        # print(doc)
        return None
        # document = Document(title = title, document = doc)
        # document.save()
        # return document