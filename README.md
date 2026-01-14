# decade-diaries

## Deploy to Vercel (Django)

This repo is configured to run Django on Vercel using a Python Serverless Function and a static build step for collected static files.

### Files added for Vercel

- `api/index.py`: serverless WSGI entrypoint
- `vercel.json`: build + routing configuration
- `build_files.sh`: runs `collectstatic` during the build

### Vercel environment variables

- **Required**
  - `SECRET_KEY`: Django secret key
- **Recommended**
  - `DEBUG`: set to `false` in production
  - `DATABASE_URL`: database connection string (if unset, app falls back to SQLite which is not suitable for production on Vercel)
  - `ALLOWED_HOSTS`: space-separated hosts (defaults include `.vercel.app`)
  - `CSRF_TRUSTED_ORIGINS`: space-separated origins (defaults to `https://*.vercel.app`)

### Notes

- Static files are collected into `staticfiles_build/static` and served from `/static/` by Vercel.
- Database migrations are not run automatically by Vercel; run them from your own CI/job or manually against your production DB.
