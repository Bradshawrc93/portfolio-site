# Portfolio Site

A production-ready Django portfolio website with GitHub integration, deployed on Render.

## Features

- **Project Showcase**: Display projects with GitHub repository integration
- **Devlog**: Markdown-powered blog posts created via Django admin
- **GitHub Sync**: Management command to sync repository data and contributions
- **Visual Charts**: HTML/CSS contribution heatmap and activity charts (no JavaScript required)
- **Dark Theme**: Matrix-inspired dark navy with mint green accents
- **Production Ready**: Configured for Render with PostgreSQL, WhiteNoise, and security settings

## Tech Stack

- Django 4.2+
- PostgreSQL (via Render Postgres)
- WhiteNoise for static files
- Markdown for devlog rendering
- GitHub API integration

## Local Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (or use SQLite for local dev)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bradshawrc93/portfolio-site.git
   cd portfolio-site
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root (or export variables):
   ```bash
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgresql://user:password@localhost:5432/portfoliosite  # Optional: use SQLite if not set
   GITHUB_TOKEN=your-github-token-here  # Optional: increases API rate limits
   ADMIN_PATH=admin/  # Optional: custom admin path
   ```

   For local development, you can skip DATABASE_URL to use SQLite.

5. **Create and run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files** (optional for dev)
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the site**
   - Homepage: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/ (or your custom ADMIN_PATH)

## Getting Started

### 1. Create a Superuser

```bash
python manage.py createsuperuser
```

Log in to the admin panel to manage content.

### 2. Add Projects

1. Go to the Django admin (http://127.0.0.1:8000/admin/)
2. Navigate to **Core → Projects**
3. Click **Add Project**
4. Fill in:
   - **Title**: Project name
   - **Slug**: URL-friendly name (auto-generated from title)
   - **Repo Full Name**: GitHub repo in format `username/repo-name` (e.g., `bradshawrc93/my-project`)
   - **Tagline**: Short description
   - **Stack**: Comma-separated tech stack (e.g., `Python, Django, PostgreSQL`)
   - **Demo URL**: Optional link to live demo
   - **Featured**: Check to show on homepage
   - **Status**: Active/Archived/Planning
   - **Sort Order**: Lower numbers appear first

### 3. Create a Devlog Post

1. Navigate to **Devlog → Devlog posts**
2. Click **Add Devlog post**
3. Fill in:
   - **Title**: Post title
   - **Slug**: URL-friendly name
   - **Content MD**: Markdown content
   - **Status**: Draft or Published
   - **Published At**: Set automatically when status is Published
   - **Project**: Optional link to a project
   - **Tags**: Comma-separated tags

### 4. Sync GitHub Data

Run the sync command to fetch repository data and contributions:

```bash
python manage.py sync_github
```

This command will:
- Fetch repository snapshots for all projects
- Get last 90 days of commit activity per repo
- Fetch current year contributions for user `bradshawrc93`

**GitHub Token** (Optional but recommended):
- Create a GitHub personal access token at https://github.com/settings/tokens
- Set `GITHUB_TOKEN` environment variable
- Increases rate limit from 60 to 5000 requests/hour

## Render Deployment

### Prerequisites

- Render account
- Supabase account (free tier works great)
- GitHub repository connected to Render

### Steps

1. **Set up Supabase Database**
   
   **Create Supabase Project:**
   - Go to https://supabase.com and sign up/login
   - Click "New Project"
   - Choose your organization
   - Enter project name: `portfolio-site` (or your preference)
   - Enter a database password (save this securely!)
   - Select a region close to you
   - Click "Create new project"
   - Wait 2-3 minutes for the project to initialize
   
   **Get Connection String:**
   - In your Supabase project, go to **Settings** → **Database**
   - Scroll down to "Connection string"
   - **IMPORTANT**: Select **"Connection pooling"** mode (NOT "Session" mode)
   - Under "URI", copy the connection string
   - It will look like: `postgresql://postgres.lcdgncwgvcukbqzcxgfx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres`
   - Or: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:6543/postgres`
   - **Use port 6543** (connection pooling) - this is required for Render/serverless deployments
   - Replace `[YOUR-PASSWORD]` with the password you set when creating the project

2. **Create a Web Service on Render**
   - Go to Render Dashboard → New → Web Service
   - Connect your GitHub repository
   - Configure:
     - **Name**: portfolio-site (or your preferred name)
     - **Environment**: Python 3
     - **Build Command**: `./build.sh` (migrations run automatically if DATABASE_URL is set)
     - **Start Command**: `gunicorn config.wsgi:application`
     - **Pre-deploy Command** (optional): `./release.sh` - if this field exists, use it for migrations

3. **Set Environment Variables**
   
   In Render Dashboard → Your Web Service → Environment:
   - `SECRET_KEY`: Generate a secure key (you can use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render domain (e.g., `portfolio-site-k2mi.onrender.com`) - or leave blank to auto-detect
   - `DATABASE_URL`: Paste the Supabase connection string from step 1
   - `GITHUB_TOKEN`: (Optional) Your GitHub personal access token for higher API rate limits
   - `ADMIN_PATH`: (Optional) Custom admin path (e.g., `control-room-9f3b2/admin/`)
   
   **Important:** Make sure to set `DATABASE_URL` with your Supabase connection string!

4. **Deploy**
   - Render will automatically deploy on push to your main branch
   - First deployment will run migrations automatically

5. **Create Superuser (One-time)**
   
   After first deployment, create a superuser:
   - Use Render Shell: `python manage.py createsuperuser`
   - Or connect to your database directly

6. **Initial Setup**
   - Add projects via Django admin
   - Create devlog posts
   - Run `python manage.py sync_github` (via Render Shell or scheduled cron job)

### Scheduled GitHub Sync (Optional)

To keep GitHub data fresh, set up a scheduled cron job on Render:

1. Go to Render Dashboard → New → Cron Job
2. Configure:
   - **Name**: github-sync
   - **Schedule**: `0 2 * * *` (daily at 2 AM)
   - **Command**: `cd /opt/render/project/src && python manage.py sync_github`
   - **Environment**: Same as your web service

## Project Structure

```
portfolio-site/
├── config/           # Django project settings
├── core/             # Core app (projects)
├── devlog/           # Devlog app (blog posts)
├── githubsync/       # GitHub sync app (models + management command)
├── templates/        # HTML templates
├── static/           # Static files (CSS)
├── manage.py
├── requirements.txt
├── build.sh          # Render build script
└── README.md
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Django secret key |
| `DEBUG` | No | `False` | Debug mode |
| `ALLOWED_HOSTS` | Yes | `localhost,127.0.0.1` | Comma-separated hostnames |
| `DATABASE_URL` | No* | SQLite | PostgreSQL connection URL |
| `GITHUB_TOKEN` | No | - | GitHub personal access token |
| `ADMIN_PATH` | No | `admin/` | Custom admin URL path |

\* Required for production (Render)

## URLs

- `/` - Homepage
- `/projects/` - Projects list with contribution heatmap
- `/projects/<slug>/` - Project detail page
- `/devlog/` - Devlog posts list
- `/devlog/<slug>/` - Devlog post detail
- `/<ADMIN_PATH>/` - Django admin (default: `/admin/`)

## Security Features

- DEBUG disabled by default
- SECURE_SSL_REDIRECT in production
- Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- XSS protection headers
- Custom admin path support
- Staff-only admin access

## License

MIT

