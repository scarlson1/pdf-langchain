# Deploying to Koyeb

This guide will help you deploy your Flask PDF application to Koyeb.

## Prerequisites

1. A Koyeb account (sign up at [koyeb.com](https://koyeb.com))
2. Your application code in a Git repository (GitHub, GitLab, or Bitbucket)
3. Required environment variables configured

## Step 1: Prepare Your Repository

Make sure your repository contains all the necessary files:

- `Dockerfile` (already created)
- `requirements.txt` (already created)
- `.koyeb.yaml` (already created)
- `env.example` (reference for environment variables)

### Alternative Dockerfiles

If you encounter issues with the main Dockerfile, you have several alternatives:

- **`Dockerfile.requirements`**: Uses a more traditional approach with `requirements.txt`
- **`Dockerfile.uv`**: Uses `uv` (fast Python package installer) for faster builds
- **`Dockerfile.uv-venv`**: Uses `uv` with virtual environment for maximum efficiency

#### Benefits of using uv

- **Faster builds**: uv is significantly faster than pip for dependency resolution and installation
- **Better caching**: More efficient Docker layer caching
- **Reliable**: Better dependency resolution and conflict handling
- **Modern**: Built with Rust for performance and reliability

## Step 2: Set Up External Services

### Database (PostgreSQL)

You'll need a PostgreSQL database. You can use:

- **Koyeb Database**: Create a PostgreSQL database in your Koyeb dashboard
- **External service**: Use services like Supabase, PlanetScale, or AWS RDS (using Koyeb)

### Redis

You'll need a Redis instance for Celery:

- **Koyeb Redis**: Create a Redis instance in your Koyeb dashboard
- **External service**: Use services like Redis Cloud, AWS ElastiCache, or Upstash (using Upstash)

### Optional Services

- **File Storage**: If you need file storage, consider AWS S3, Cloudinary, or similar
- **Vector Database**: For embeddings, you might need Pinecone, Weaviate, or similar (using Pinecone)

## Step 3: Configure Environment Variables

In your Koyeb dashboard, you'll need to set these environment variables:

### Required Variables

```
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/database
UPLOAD_URL=https://your-app-name.koyeb.app
REDIS_URI=redis://user:password@host:port/database
```

### Optional Variables (if using these services)

```
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
LANGFUSE_SECRET_KEY=your-langfuse-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-s3-bucket-name
AWS_REGION=us-east-1
```

## Step 4: Deploy to Koyeb

### Method 1: Using Koyeb Dashboard (Recommended)

1. **Connect your repository**:

   - Go to your Koyeb dashboard
   - Click "Create Service"
   - Choose "GitHub", "GitLab", or "Bitbucket"
   - Select your repository

2. **Configure the service**:

   - **Name**: `pdf-app-web`
   - **Type**: Web Service
   - **Dockerfile**: Use the Dockerfile in your repository
   - **Port**: 8000
   - **Environment Variables**: Add all the required variables

3. **Create the worker service**:
   - Create another service for the Celery worker
   - **Name**: `pdf-app-worker`
   - **Type**: Worker Service
   - **Dockerfile**: Use the same Dockerfile
   - **Command**: `celery -A app.celery.worker worker --concurrency=1 --loglevel=INFO --pool=solo`
   - **Environment Variables**: Same as the web service

### Method 2: Using Koyeb CLI

1. **Install Koyeb CLI**:

   ```bash
   curl -fsSL https://cli.koyeb.com/install.sh | sh
   ```

2. **Login to Koyeb**:

   ```bash
   koyeb auth login
   ```

3. **Deploy using the configuration file**:
   ```bash
   koyeb service create --config .koyeb.yaml
   ```

## Step 5: Database Initialization

The application will automatically initialize database tables on startup. However, if you need to manually manage the database:

### Automatic Initialization (Recommended)

- Tables are created automatically when the application starts
- Safe for production - won't drop existing data
- No manual intervention required

### Manual Database Management

If you need to manually manage the database:

1. **Access your web service**:

   - Go to your Koyeb dashboard
   - Find your web service
   - Click on "Logs" or "Shell"

2. **Available commands**:

   ```bash
   # Initialize tables (safe, won't drop existing data)
   flask --app app.web init-db

   # Reset database (destructive - drops all data)
   flask --app app.web reset-db
   ```

## Step 6: Verify Deployment

1. **Check your web service**:

   - Visit your app URL (provided by Koyeb)
   - Ensure the frontend loads correctly

2. **Check your worker service**:

   - Go to the worker service logs
   - Ensure Celery is running without errors

3. **Test the application**:
   - Try uploading a PDF
   - Test the chat functionality
   - Verify that background tasks are processed

## Troubleshooting

### Common Issues

1. **Docker build failures**:

   - If you get pipenv errors, try using `Dockerfile.requirements` instead
   - For faster builds, try `Dockerfile.uv` or `Dockerfile.uv-venv`
   - Ensure all dependencies are listed in `requirements.txt` or `pyproject.toml`
   - Check that Node.js installation completed successfully

2. **Database connection errors**:

   - Verify your `SQLALCHEMY_DATABASE_URI` is correct
   - Ensure your database is accessible from Koyeb
   - If you get `ModuleNotFoundError: No module named 'psycopg2'`, ensure `psycopg2-binary` is in your dependencies

3. **Redis connection errors**:

   - Verify your `REDIS_URI` is correct
   - Ensure your Redis instance is accessible

4. **Worker not processing tasks**:

   - Check that the worker service is running
   - Verify Redis connection in worker logs

5. **Static files not loading**:
   - Ensure the frontend build process completed successfully
   - Check that the `client/build` directory exists in your container

### Monitoring

- Use Koyeb's built-in monitoring to track service health
- Check logs regularly for any errors
- Monitor resource usage and scale as needed

## Scaling

### Automatic Scaling

Your services are configured with auto-scaling:

- **Web service**: 1-3 instances
- **Worker service**: 1-2 instances

### Manual Scaling

You can adjust scaling in the Koyeb dashboard:

1. Go to your service
2. Click "Settings"
3. Adjust the scaling parameters

## Cost Optimization

- Start with `nano` instance types (cheapest)
- Monitor usage and upgrade instance types as needed
- Use auto-scaling to handle traffic spikes efficiently

## Security Considerations

- Use strong, unique secret keys
- Keep your database and Redis instances secure
- Regularly update dependencies
- Monitor for security vulnerabilities

## Support

- Koyeb Documentation: [docs.koyeb.com](https://docs.koyeb.com)
- Koyeb Community: [community.koyeb.com](https://community.koyeb.com)
- This project's issues: Create an issue in your repository
