from django.db import migrations
from django.utils import timezone


def seed_data(apps, schema_editor):
    Community = apps.get_model('communities', 'Community')
    now = timezone.now()
    data = [
        dict(name='Open Arts Collective', description='Workshops and exhibitions for emerging artists', location='Mumbai, IN', verified=True, funded_recently=True, sponsors_count=5, last_active=now),
        dict(name='Code for All', description='Free coding bootcamps for underserved youth', location='Bengaluru, IN', verified=True, funded_recently=False, sponsors_count=8, last_active=now),
        dict(name='Green Earth Club', description='Community cleanups and tree drives', location='Pune, IN', verified=False, funded_recently=False, sponsors_count=2, last_active=now),
        dict(name='Readers Circle', description='Monthly book club and author talks', location='Delhi, IN', verified=True, funded_recently=True, sponsors_count=3, last_active=now),
        dict(name='Dance United', description='Inclusive dance workshops', location='Kolkata, IN', verified=False, funded_recently=False, sponsors_count=1, last_active=now),
        dict(name='Makers Lab', description='Hands-on STEM and robotics', location='Chennai, IN', verified=True, funded_recently=False, sponsors_count=4, last_active=now),
        dict(name='Health & Wellness Co-op', description='Community fitness and mental health', location='Hyderabad, IN', verified=False, funded_recently=True, sponsors_count=6, last_active=now),
        dict(name='Neighborhood Theatre', description='Local plays and youth productions', location='Ahmedabad, IN', verified=True, funded_recently=False, sponsors_count=2, last_active=now),
    ]
    for row in data:
        Community.objects.create(**row)


def unseed_data(apps, schema_editor):
    Community = apps.get_model('communities', 'Community')
    Community.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=unseed_data),
    ]
