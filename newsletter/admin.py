from django.contrib import admin
from .models import Newsletter, Subscriber
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from django.utils import timezone

# Register your models here.

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at', 'is_sent', 'sent_at']
    actions = ('send_newsletters',)

    def send_newsletters(self, request, queryset):
        # send_email_newsletter(newsletters=queryset, respect_schedule=False)
        if len(queryset) > 1:
            messages.add_message(
                    request,
                    messages.ERROR,
                    'Multiple newsletter at once not allowed',
                )
            return

        for obj in queryset:
            if not obj.is_sent:
                obj.is_sent=True
                obj.sent_at = timezone.now()
                obj.save()

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Sending selected newsletters(s) to the subscribers',
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Selected newsletter already sent',
                )


 
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'status', 'created_at']


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Subscriber,SubscriberAdmin)