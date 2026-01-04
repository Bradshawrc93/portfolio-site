# Portfolio Site

A production-ready Django portfolio platform with automated GitHub integration, deployed on Render.

## Features

- **Project Showcase**: Automated import of repository metadata (stars, forks, language) and READMEs.
- **Activity Tracking**: Visual heatmap and commit history charts generated from live GitHub data.
- **Devlog**: Markdown-based technical blog managed via Django Admin.
- **Modern UI**: Responsive, dark-themed design with "glassmorphism" aesthetics and CSS-only charts.
- **Production Ready**: configured for Render (PostgreSQL, WhiteNoise, Gunicorn).

## Tech Stack

- **Backend**: Python 3.11+, Django 4.2+
- **Database**: PostgreSQL (Supabase via connection pooling)
- **Frontend**: Django Templates, CSS3 (No heavy JS frameworks)
- **Deployment**: Render Web Service + CI/CD via GitHub Actions

## Local Development

1. **Clone & Setup**
   ```bash
   git clone https://github.com/bradshawrc93/portfolio-site.git
   cd portfolio-site
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file:
   ```env
   SECRET_KEY=dev-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   # Optional: DATABASE_URL=... (Defaults to SQLite for local dev)
   # Optional: GITHUB_TOKEN=... (For higher API rate limits)
   ```

3. **Run**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Deployment (Render + Supabase)

### 1. Database (Supabase)
1. Create a new project at [Supabase](https://supabase.com).
2. Go to **Settings > Database > Connection string**.
3. **Crucial**: Select **"Connection pooling"** mode (Port 6543) and **"Transaction"** mode.
4. Copy the URI and replace `[YOUR-PASSWORD]`.

### 2. Web Service (Render)
1. Create a new Web Service connected to this repo.
2. **Environment Variables**:
   - `DATABASE_URL`: Your Supabase connection pool string.
   - `SECRET_KEY`: A strong random string.
   - `DEBUG`: `False`.
   - `GITHUB_TOKEN`: Your GitHub PAT (Classic) with `public_repo` scope (prevents rate limits).
3. **Commands**:
   - **Build**: `./build.sh`
   - **Start**: `gunicorn config.wsgi:application`
   - **Release**: `./release.sh` (Runs migrations automatically).

## Management Commands

### GitHub Sync
Manually syncs repository data, READMEs, and commit activity.
```bash
python manage.py sync_github
```
*Tip: Set this up as a Cron Job in Render (e.g., daily at 02:00) to keep data fresh.*

## Troubleshooting

**Sync Issues ("Stats calculation in progress" / Missing Data)**
- GitHub's API calculates stats asynchronously. If data is missing, wait 5 minutes and re-run.
- Ensure `GITHUB_TOKEN` is set to avoid 60 requests/hour rate limits.
- Verify the `repo_full_name` in Django Admin matches GitHub exactly (case-sensitive).

**Database Connection Errors**
- Ensure you are using the **Supabase Connection Pool** URL (Port 6543), not the direct connection (Port 5432), as Render uses shared IPs.
