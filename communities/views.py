from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum
from .models import Community, Sponsor


def directory(request):
    qs = Community.objects.all()

    # Filters
    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    verified = request.GET.get("verified")  # 'on' or None
    sort = request.GET.get("sort", "newest")

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if location:
        qs = qs.filter(location__icontains=location)
    if verified:
        qs = qs.filter(verified=True)

    # Sorting
    if sort == "most-sponsored":
        qs = qs.order_by("-sponsors_count", "-created_at")
    elif sort == "recently-active":
        qs = qs.order_by("-last_active", "-created_at")
    elif sort == "recently-funded":
        qs = qs.order_by("-funded_recently", "-created_at")
    else:  # newest
        qs = qs.order_by("-created_at")

    paginator = Paginator(qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "q": q,
        "location": location,
        "verified_checked": bool(verified),
        "sort": sort,
        "total": qs.count(),
    }
    return render(request, "communities/directory.html", context)


def detail(request, pk: int):
    community = get_object_or_404(Community, pk=pk)
    events = community.events.all()[:6]
    sponsorships = community.sponsorships.select_related("sponsor").order_by("-date")[:6]
    totals = community.sponsorships.aggregate(total_amount=Sum("amount"))
    context = {
        "community": community,
        "events": events,
        "sponsorships": sponsorships,
        "total_amount": totals.get("total_amount") or 0,
    }
    return render(request, "communities/detail.html", context)


def sponsors_directory(request):
    qs = Sponsor.objects.all().order_by('name')
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(name__icontains=q)
    paginator = Paginator(qs, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sponsors/directory.html', {
        'page_obj': page_obj,
        'q': q,
        'total': qs.count(),
    })


def sponsor_detail(request, pk: int):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    sponsorships = sponsor.sponsorships.select_related('community').order_by('-date')
    totals = sponsor.sponsorships.aggregate(total_amount=Sum('amount'))
    return render(request, 'sponsors/detail.html', {
        'sponsor': sponsor,
        'sponsorships': sponsorships,
        'total_amount': totals.get('total_amount') or 0,
    })
