from MainApps.models import Website

def website_context(request):
    """
    Load website branding dynamically from the database
    """
    data = {
        'SIMPLEUI_SITE_TITLE': 'Gurukul IT Plaza Admin',
        'SIMPLEUI_SITE_HEADER': 'Gurukul IT Plaza',
        'SIMPLEUI_INDEX_TITLE': 'Welcome to Gurukul IT Plaza Admin Portal',
        'SIMPLEUI_LOGO': '/static/images/default_logo.png',
        'WEBSITE_LOGO1': '/static/images/default_logo.png',
        'WEBSITE_LOGO2': '/static/images/default_logo.png',
        'WEBSITE_FAVICON': '/static/images/default_favicon.png',
        'WEBSITE_NAME': 'Gurukul',
    }

    try:
        website = Website.objects.first()  # pick the first row or implement a filter
        if website:
            data['WEBSITE_NAME'] = website.name
            data['SIMPLEUI_SITE_TITLE'] = f"{website.name} Admin"
            data['SIMPLEUI_SITE_HEADER'] = website.name
            data['SIMPLEUI_INDEX_TITLE'] = f"Welcome to {website.name} Admin Portal"

            # Logos
            if request.user.is_authenticated and request.user.is_superuser and website.logo2:
                data['SIMPLEUI_LOGO'] = website.logo2.url
            elif website.logo1:
                data['SIMPLEUI_LOGO'] = website.logo1.url

            # Frontend logos & favicon
            if website.logo1:
                data['WEBSITE_LOGO1'] = website.logo1.url
            if website.logo2:
                data['WEBSITE_LOGO2'] = website.logo2.url
            if website.favicon:
                data['WEBSITE_FAVICON'] = website.favicon.url
    except Exception:
        pass

    return data
