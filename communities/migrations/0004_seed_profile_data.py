from django.db import migrations
from django.utils import timezone


def seed_profile(apps, schema_editor):
    Community = apps.get_model('communities', 'Community')
    Sponsor = apps.get_model('communities', 'Sponsor')
    Sponsorship = apps.get_model('communities', 'Sponsorship')
    Event = apps.get_model('communities', 'Event')

    now = timezone.now().date()

    acme = Sponsor.objects.create(name='Acme Corp')
    globex = Sponsor.objects.create(name='Globex')

    # attach to first two communities if exist
    comms = list(Community.objects.all()[:2])
    if not comms:
        return

    c1 = comms[0]
    c1.tagline = c1.tagline or 'Empowering local creators'
    c1.about = c1.about or 'We host workshops, exhibitions, and community meetups to grow the creative ecosystem.'
    c1.website_url = c1.website_url or 'https://example.org'
    c1.save(update_fields=['tagline','about','website_url'])

    Event.objects.create(community=c1, title='Community Art Fair', date=now, description='Showcase of local artists')
    Event.objects.create(community=c1, title='Workshop: Digital Illustration', date=now, description='Hands-on session for beginners')

    Sponsorship.objects.create(community=c1, sponsor=acme, amount=250000, contribution_type='grant', date=now)
    Sponsorship.objects.create(community=c1, sponsor=globex, amount=50000, contribution_type='cash', date=now)

    if len(comms) > 1:
        c2 = comms[1]
        c2.tagline = c2.tagline or 'Coding for everyone'
        c2.about = c2.about or 'We provide free bootcamps and mentorship for youth to start careers in tech.'
        c2.website_url = c2.website_url or 'https://codeforall.example'
        c2.save(update_fields=['tagline','about','website_url'])

        Event.objects.create(community=c2, title='Hack for Good', date=now, description='Build solutions for local NGOs')
        Sponsorship.objects.create(community=c2, sponsor=acme, amount=100000, contribution_type='cash', date=now)


def unseed_profile(apps, schema_editor):
    Sponsor = apps.get_model('communities', 'Sponsor')
    Sponsorship = apps.get_model('communities', 'Sponsorship')
    Event = apps.get_model('communities', 'Event')
    Sponsorship.objects.all().delete()
    Event.objects.all().delete()
    Sponsor.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('communities', '0003_profile_models'),
    ]

    operations = [
        migrations.RunPython(seed_profile, reverse_code=unseed_profile),
    ]
