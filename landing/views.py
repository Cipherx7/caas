from django.shortcuts import render


def index(request):
	"""Render the landing page."""
	# Static showcase data placeholders for now
	featured_communities = [
		{
			"name": "Open Arts Collective",
			"tagline": "Workshops and exhibitions for emerging artists",
			"location": "Mumbai, IN",
			"verified": True,
		},
		{
			"name": "Code for All",
			"tagline": "Free coding bootcamps for underserved youth",
			"location": "Bengaluru, IN",
			"verified": True,
		},
		{
			"name": "Green Earth Club",
			"tagline": "Community cleanups and tree drives",
			"location": "Pune, IN",
			"verified": False,
		},
	]

	sponsors = [
		{"name": "Acme Corp"},
		{"name": "Globex"},
		{"name": "Innotech"},
		{"name": "BlueSky"},
	]

	stats = {
		"communities": "4,200+",
		"funding": "₹12 Cr+",
		"sponsors": "900+",
	}

	testimonials = [
		{
			"quote": "We grew membership 3x after listing here.",
			"author": "Asha, Open Arts Collective",
		},
		{
			"quote": "Discovering verified communities is now effortless.",
			"author": "Rahul, Sponsor at Acme Corp",
		},
	]

	return render(
		request,
		"landing/index.html",
		{
			"featured_communities": featured_communities,
			"sponsors": sponsors,
			"stats": stats,
			"testimonials": testimonials,
		},
	)
