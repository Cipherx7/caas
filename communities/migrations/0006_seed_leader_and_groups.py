from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_groups_and_demo_user(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')
    Community = apps.get_model('communities', 'Community')
    CommunityLeader = apps.get_model('communities', 'CommunityLeader')

    leader_group, _ = Group.objects.get_or_create(name='leader')

    # Create demo user if not exists
    username = 'demo_leader'
    password = 'demo12345'
    user, created = User.objects.get_or_create(username=username, defaults={
        'password': make_password(password),
        'is_active': True,
    })
    user.groups.add(leader_group)

    # Link to first community if available
    community = Community.objects.first()
    if community:
        CommunityLeader.objects.get_or_create(user=user, community=community)


def unseed_groups_and_demo_user(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')
    CommunityLeader = apps.get_model('communities', 'CommunityLeader')

    try:
        user = User.objects.get(username='demo_leader')
        CommunityLeader.objects.filter(user=user).delete()
        user.delete()
    except User.DoesNotExist:
        pass
    Group.objects.filter(name='leader').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('communities', '0005_communityleader'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(seed_groups_and_demo_user, reverse_code=unseed_groups_and_demo_user),
    ]
