# Django Developer Guide: A Practical Introduction

This guide is designed for developers new to Django. It explains core concepts using this portfolio project as a real-world reference. Instead of abstract theory, we'll see how Django's pieces fit together to build a production app.

---

## 1. The Core Architecture: MVT

Django follows the **Model-View-Template (MVT)** pattern (similar to MVC).

1.  **Model**: The data layer (database tables).
2.  **View**: The logic layer (fetches data, handles user input).
3.  **Template**: The presentation layer (HTML).

### How it works in this project:
When a user visits `/projects/`:
1.  **URL Router** (`core/urls.py`) sends the request to the `project_list` view.
2.  **View** (`core/views.py`) fetches `Project` objects from the **Model** (`core/models.py`).
3.  **Template** (`templates/core/project_list.html`) renders that data into HTML.

---

## 2. Project Structure

Django projects are split into "Apps" (modular components) and a "Project Configuration".

-   **`config/`**: The main configuration (settings, main URL router).
    -   `settings.py`: Database config, installed apps, security keys.
    -   `urls.py`: The entry point for all URLs.
-   **Apps**:
    -   `core/`: Main pages (Home, Projects).
    -   `devlog/`: Blog functionality.
    -   `githubsync/`: Background tasks/utilities.

**Rule of Thumb**: If you're adding a distinct feature (e.g., "Authentication" or "Payments"), consider creating a new app: `python manage.py startapp payments`.

---

## 3. Models (The Database)

Models define your database structure in Python. Django handles the SQL for you.

**Reference:** `core/models.py`

```python
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(choices=STATUS_CHOICES, default='active')
```

### Migrations
When you change a model, you must propagate changes to the database.
1.  **Make Migrations**: `python manage.py makemigrations` (Creates a plan).
2.  **Migrate**: `python manage.py migrate` (Executes SQL).

---

## 4. Views & URLs (The Logic)

Views are Python functions (or classes) that take a Web request and return a Web response.

**Reference:** `core/views.py`

```python
def project_list(request):
    # 1. Fetch data
    projects = Project.objects.filter(status='active')
    
    # 2. Pass data to context
    context = {'projects': projects}
    
    # 3. Render template
    return render(request, 'core/project_list.html', context)
```

**Connecting URLs:** `core/urls.py` links the URL path to the view.
```python
path('projects/', views.project_list, name='project_list')
```

---

## 5. Templates (The HTML)

Django templates allow you to inject data into HTML using a special syntax.

**Reference:** `templates/core/project_list.html`

-   **Variables**: `{{ project.title }}` (Outputs the title).
-   **Tags**: `{% for p in projects %} ... {% endfor %}` (Loops logic).
-   **Inheritance**: `{% extends 'base.html' %}` (Reuses the layout from `templates/base.html`).

---

## 6. The Admin Interface

One of Django's superpowers is the auto-generated admin panel.

**Reference:** `core/admin.py`

Registering your models here makes them accessible at `/admin/`.
```python
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
```

---

## 7. Management Commands

You can extend Django's CLI (`manage.py`) to run custom scripts.

**Reference:** `githubsync/management/commands/sync_github.py`

This project uses a custom command to fetch data from GitHub:
```bash
python manage.py sync_github
```
This demonstrates how to write backend scripts that interact with your Django models outside of the request/response cycle.

---

## Quick Cheat Sheet

| Task | Command / File |
| :--- | :--- |
| **Run Server** | `python manage.py runserver` |
| **Database Update** | `python manage.py makemigrations` -> `python manage.py migrate` |
| **Create Admin User** | `python manage.py createsuperuser` |
| **Change Settings** | `config/settings.py` |
| **Add Page** | 1. View (`views.py`) -> 2. URL (`urls.py`) -> 3. Template (`.html`) |

