# Community Hub (Django)

This is a Django project scaffolding for a universal community listing and sponsorship platform. The initial Landing Page implements the sections described in `platform.md`.

## Quick start (Windows PowerShell)

1. Activate the virtual environment (auto-configured by VS Code):
   - Interpreter path: `E:\Work\Websites\Common Php\htdocs\caas\.venv\Scripts\python.exe`

2. Install dependencies (already installed if you ran the assistant steps):

```powershell
"E:\Work\Websites\Common Php\htdocs\caas\.venv\Scripts\python.exe" -m pip install -U Django
```

3. Apply migrations:

```powershell
$py="E:\Work\Websites\Common Php\htdocs\caas\.venv\Scripts\python.exe"; & $py manage.py migrate
```

4. Run the server:

```powershell
$py="E:\Work\Websites\Common Php\htdocs\caas\.venv\Scripts\python.exe"; & $py manage.py runserver 0.0.0.0:8000
```

5. Open http://127.0.0.1:8000/ to view the landing page.

## Project structure

- `manage.py` — Django entry point
- `commhub/` — Project settings and URLs
- `landing/` — App for the landing page
- `templates/` — Global templates (`base.html`, `landing/index.html`)
- `static/` — Static assets (`css/styles.css`, `js/network.js`)
- `platform.md` — Product blueprint driving the initial design

## Notes

- The project name is `commhub` (not `platform`) to avoid a conflict with Python's built-in `platform` module which Django disallows for project names.
- The landing page currently uses placeholder data in `landing/views.py`. When you add real models, you can replace that with database queries.

## Next steps

- Add pages for Communities Directory, Community Profile, and Sponsor Portal.
- Create models for Community, Sponsor, Event, and Funding.
- Replace placeholders with real data and admin management.
- Add authentication (users, leaders, sponsors) and role-based access.
