from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import SubscriberForm
from django.urls import reverse
from .models import Subscriber
from django.contrib import messages
import json
import requests
from django.conf import settings

# https://github.com/justdjango/dream_blog/blob/master/marketing/views.py

api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(dc=settings.MAILCHIMP_DATA_CENTER)
members_endpoint = '{api_url}/lists/{list_id}/members'.format(
    api_url=api_url,
    list_id=settings.MAILCHIMP_EMAIL_LIST_ID
)

def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", settings.MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()

def unsubscribe(email):
    data = {
        "email_address": email,
        "status": "unsubscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", settings.MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()

class SubscriberFormView(FormView):
    template_name = 'newsletter/subscribe.html'
    form_class = SubscriberForm
    
    def get_success_url(self):
        return reverse('newsletter:subscribe_view')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            mail_got = form.cleaned_data.get('email')
            existing_user = Subscriber.objects.filter(email=mail_got).first()

            if existing_user: # The email provided exists in db.
                existing_user.status = True
                existing_user.save()
            else:
                # subscribe(mail_got)
                form.save()
            messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Thanks for joining mail list',
                )
            return self.form_valid(form)
        else:
            print("Invalid form")
            return self.form_invalid(form)

class UnSubscriberFormView(FormView):
    template_name = 'newsletter/unsubscribe.html'
    form_class = SubscriberForm
    
    def get_success_url(self):
        return reverse('newsletter:unsubscribe_view')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            mail_got = form.cleaned_data.get('email')
            existing_user = Subscriber.objects.filter(email=mail_got).first()

            if existing_user: # The email provided exists in db.
                existing_user.status = False
                existing_user.save()
                # unsubscribe(mail_got)
            messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Subscription cancelled.',
                )
            return self.form_valid(form)
        else:
            print("Invalid form")
            return self.form_invalid(form)