from django.db import models
from django.utils.translation import gettext_lazy as _

class Subscriber(models.Model):
    email = models.EmailField(_("E-mail"), max_length=254)
    status = models.BooleanField(_("Status"), default=True)
    created_at = models.DateTimeField(_("Created At"),  auto_now_add=True)

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.email

    # def get_absolute_url(self):
    #     return reverse("Subscriber_detail", kwargs={"pk": self.pk})

# Create your models here.
class Newsletter(models.Model):
    subject = models.CharField(_("Title"), max_length=50)
    body = models.TextField(_("Body"))
    created_at = models.DateField(_("Created at"), auto_now_add=True )
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateField(_("Sent at"), null=True, blank=True, editable=False)
    subscribers = models.ManyToManyField(Subscriber, verbose_name=_("Subscriber") ,  blank=True)
    
    class Meta:
        verbose_name_plural = "Newsletter"
        verbose_name = "Newsletter"

    def __str__(self):
        return self.subject

 