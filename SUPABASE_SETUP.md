# Supabase Setup Guide for Portfolio Site

This guide will help you set up Supabase as your database for the Django portfolio site on Render.

## Quick Setup Steps

### 1. Create Supabase Account & Project

1. Go to https://supabase.com
2. Sign up or log in
3. Click **"New Project"**
4. Fill in:
   - **Name**: `portfolio-site` (or your choice)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to you
5. Click **"Create new project"**
6. Wait 2-3 minutes for initialization

### 2. Get Your Connection String

1. In your Supabase project dashboard
2. Go to **Settings** (gear icon in left sidebar)
3. Click **Database**
4. Scroll down to **"Connection string"** section
5. Find the **"URI"** tab
6. Copy the connection string
   - It looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
7. **Replace `[YOUR-PASSWORD]`** with the actual password you set when creating the project
   - Final format: `postgresql://postgres:your-actual-password@db.xxxxx.supabase.co:5432/postgres`

### 3. Configure in Render

1. Go to your Render Dashboard → Your Web Service
2. Click **Environment** in the left sidebar
3. Find or add `DATABASE_URL`
4. Paste your Supabase connection string (the one with your actual password)
5. **Save Changes**

### 4. Set Release Command (Important!)

1. Still in your Web Service settings
2. Click **Settings** (not Environment)
3. Scroll to **"Release Command"**
4. Set it to: `./release.sh`
5. **Save Changes**

### 5. Deploy

Render will automatically redeploy when you save changes. The release command will:
- Run database migrations
- Create all necessary tables
- Set up your database structure

## Verify It's Working

After deployment completes:

1. Visit your site URL (e.g., `https://portfolio-site-k2mi.onrender.com`)
2. You should see the homepage (even if empty, no database errors)
3. Go to `/admin/` (or your custom admin path)
4. Log in with your superuser credentials

## Create Superuser

If you need to create a superuser:

1. In Render Dashboard → Your Web Service
2. Click **Shell** (top right)
3. Run: `python manage.py createsuperuser`
4. Follow the prompts to create your admin account

## Security Notes

- ✅ Your database password is stored securely in Render's environment variables
- ✅ Supabase connection uses SSL by default
- ✅ Free tier includes 500MB database storage (plenty for a portfolio site)
- ✅ Connection string includes password - keep it private!

## Troubleshooting

**Error: "no such table"**
- Make sure Release Command is set to `./release.sh`
- Check that migrations ran successfully in Render logs

**Error: "connection refused"**
- Verify your DATABASE_URL is correct
- Check that you replaced `[YOUR-PASSWORD]` with actual password
- Ensure Supabase project is active (not paused)

**Can't connect to database**
- Verify the connection string format is correct
- Check Supabase project status
- Try regenerating the connection string in Supabase dashboard

