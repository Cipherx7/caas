from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from django.contrib.auth.models import Group
from .models import CommunityLeader, Community
from .forms import CommunityForm, EventForm, SponsorshipForm, SponsorForm
from .models import Sponsor


def _get_user_community(user):
    link = CommunityLeader.objects.filter(user=user).select_related('community').first()
    return link.community if link else None


@login_required
def leader_dashboard(request):
    community = _get_user_community(request.user)
    if not community:
        return redirect('/communities/')

    # All communities this user leads
    my_communities = (
        Community.objects.filter(leaders__user=request.user)
        .distinct()
        .order_by('name')
    )

    stats = {
        'sponsors': community.sponsorships.values('sponsor_id').distinct().count(),
        'events': community.events.count(),
        'funding_total': community.sponsorships.aggregate(total=Sum('amount')).get('total') or 0,
    }

    recent_sponsorships = community.sponsorships.select_related('sponsor').order_by('-date')[:5]
    recent_events = community.events.all()[:5]

    return render(request, 'dashboard/leader.html', {
        'community': community,
        'my_communities': list(my_communities),
        'stats': stats,
        'recent_sponsorships': recent_sponsorships,
        'recent_events': recent_events,
    })


@login_required
def new_community(request):
    """Allow any authenticated user to list their community and become a leader."""
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save()
            # Link user as leader
            CommunityLeader.objects.get_or_create(user=request.user, community=community)
            # Add to leader group
            group, _ = Group.objects.get_or_create(name='leader')
            request.user.groups.add(group)
            return redirect('leader_dashboard')
    else:
        form = CommunityForm()
    return render(request, 'communities/community_form.html', {"form": form, "title": "List Your Community"})


@login_required
def edit_community(request):
    """Leaders can edit their community profile."""
    link = CommunityLeader.objects.filter(user=request.user).select_related('community').first()
    if not link:
        return redirect('/communities/new/')
    community = link.community
    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return redirect('leader_dashboard')
    else:
        form = CommunityForm(instance=community)
    return render(request, 'communities/community_form.html', {"form": form, "title": "Edit Community Profile"})


@login_required
def edit_community_pk(request, pk: int):
    """Edit a specific community if the current user is a leader there."""
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return redirect('leader_dashboard')
    else:
        form = CommunityForm(instance=community)
    return render(request, 'communities/community_form.html', {"form": form, "title": f"Edit: {community.name}"})


@login_required
def manage_community_pk(request, pk: int):
    """Manage hub page for a specific community (links to profile, events, sponsorships)."""
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    # Show quick lists
    events = community.events.all()[:5]
    sponsorships = community.sponsorships.select_related('sponsor').order_by('-date')[:5]
    return render(request, 'dashboard/manage.html', {
        'community': community,
        'events': events,
        'sponsorships': sponsorships,
    })


@login_required
def events_list_create(request, pk: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            evt = form.save(commit=False)
            evt.community = community
            evt.save()
            return redirect('events_list_create', pk=pk)
    else:
        form = EventForm()
    events = community.events.all()
    return render(request, 'dashboard/events_list.html', {
        'community': community,
        'form': form,
        'events': events,
    })


@login_required
def event_edit(request, pk: int, event_id: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    evt = get_object_or_404(community.events.model, pk=event_id, community=community)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=evt)
        if form.is_valid():
            form.save()
            return redirect('events_list_create', pk=pk)
    else:
        form = EventForm(instance=evt)
    return render(request, 'dashboard/events_edit.html', {
        'community': community,
        'form': form,
        'event': evt,
    })


@login_required
def event_delete(request, pk: int, event_id: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    evt = get_object_or_404(community.events.model, pk=event_id, community=community)
    if request.method == 'POST':
        evt.delete()
        return redirect('events_list_create', pk=pk)
    return render(request, 'dashboard/confirm_delete.html', {
        'community': community,
        'object': evt,
        'type': 'Event',
    })


@login_required
def sponsorships_list_create(request, pk: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    if request.method == 'POST':
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            sp = form.save(commit=False)
            sp.community = community
            sp.save()
            return redirect('sponsorships_list_create', pk=pk)
    else:
        form = SponsorshipForm()
    sponsorships = community.sponsorships.select_related('sponsor').order_by('-date')
    return render(request, 'dashboard/sponsorships_list.html', {
        'community': community,
        'form': form,
        'sponsorships': sponsorships,
    })


@login_required
def sponsorship_edit(request, pk: int, sponsorship_id: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    model = community.sponsorships.model
    sp = get_object_or_404(model, pk=sponsorship_id, community=community)
    if request.method == 'POST':
        form = SponsorshipForm(request.POST, instance=sp)
        if form.is_valid():
            form.save()
            return redirect('sponsorships_list_create', pk=pk)
    else:
        form = SponsorshipForm(instance=sp)
    return render(request, 'dashboard/sponsorships_edit.html', {
        'community': community,
        'form': form,
        'sponsorship': sp,
    })


@login_required
def sponsorship_delete(request, pk: int, sponsorship_id: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    model = community.sponsorships.model
    sp = get_object_or_404(model, pk=sponsorship_id, community=community)
    if request.method == 'POST':
        sp.delete()
        return redirect('sponsorships_list_create', pk=pk)
    return render(request, 'dashboard/confirm_delete.html', {
        'community': community,
        'object': sp,
        'type': 'Sponsorship',
    })


@login_required
def sponsors_list_create(request, pk: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    # Sponsor is global entity; listing all for convenience
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sponsors_list_create', pk=pk)
    else:
        form = SponsorForm()
    sponsors = Sponsor.objects.all().order_by('name')
    return render(request, 'dashboard/sponsors_list.html', {
        'community': community,
        'form': form,
        'sponsors': sponsors,
    })


@login_required
def sponsor_edit(request, pk: int, sponsor_id: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    sponsor = get_object_or_404(Sponsor, pk=sponsor_id)
    if request.method == 'POST':
        form = SponsorForm(request.POST, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect('sponsors_list_create', pk=pk)
    else:
        form = SponsorForm(instance=sponsor)
    return render(request, 'dashboard/sponsors_edit.html', {
        'community': community,
        'form': form,
        'sponsor': sponsor,
    })


@login_required
def sponsor_delete(request, pk: int, sponsor_id: int):
    community = get_object_or_404(Community, pk=pk)
    allowed = Community.objects.filter(pk=pk, leaders__user=request.user).exists()
    if not allowed:
        return redirect('/dashboard/leader/')
    sponsor = get_object_or_404(Sponsor, pk=sponsor_id)
    if request.method == 'POST':
        sponsor.delete()
        return redirect('sponsors_list_create', pk=pk)
    return render(request, 'dashboard/confirm_delete.html', {
        'community': community,
        'object': sponsor,
        'type': 'Sponsor',
    })
