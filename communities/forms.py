from django import forms
from .models import Community, Event, Sponsorship, Sponsor


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = [
            'name', 'tagline', 'description', 'about', 'location',
            'contact_email', 'website_url', 'logo_url'
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 5}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['sponsor', 'amount', 'contribution_type', 'date']


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['name', 'logo_url', 'description']
