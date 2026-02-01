# Vercel Deployment Guide

This guide explains how to deploy both the frontend and backend of the AI-Powered Book Platform to Vercel.

## Prerequisites

- GitHub account
- Vercel account
- Access to external services (PostgreSQL, Qdrant, etc.)

## Deploying the Backend

### 1. Prepare your repository
- Push your backend code to a GitHub repository
- Ensure the `vercel.json` file is present in the root of the backend directory

### 2. Set up external services
Before deploying, ensure you have:
- PostgreSQL database (e.g., from Neon, Supabase, or AWS RDS)
- Qdrant vector database instance
- API keys for OpenRouter or OpenAI
- Redis instance (optional, for caching)

### 3. Deploy to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your backend repository
4. In the configuration:
   - Framework preset: "Other" (Vercel will detect Python automatically)
   - Build Command: Leave empty (auto-detected)
   - Output Directory: Leave empty
   - Install Command: Leave empty
5. Add environment variables in the "Environment Variables" section:
   ```
   DATABASE_URL=your_postgresql_connection_string
   QDRANT_URL=your_qdrant_instance_url
   QDRANT_API_KEY=your_qdrant_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   SECRET_KEY=a_strong_secret_key_for_jwt_tokens
   CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
   ```
6. Click "Deploy"

### 4. Note the backend URL
After deployment, note the assigned URL (e.g., `https://your-backend-project.vercel.app`)

## Deploying the Frontend

### 1. Prepare your repository
- Push your frontend code to a GitHub repository

### 2. Deploy to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your frontend repository
4. In the configuration:
   - Framework preset: "Docusaurus"
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`
5. Add environment variables in the "Environment Variables" section:
   ```
   API_BASE_URL=https://your-backend-project.vercel.app/api
   ```
6. Click "Deploy"

## Post-Deployment Steps

### 1. Database Migrations
Since serverless functions shouldn't run DDL operations, you'll need to run database migrations separately:
- Use a migration script or your database's web interface
- Apply the schema defined in your SQLAlchemy models

### 2. Data Initialization
- If needed, initialize your database with seed data
- Upload your book content to the Qdrant vector database

### 3. Testing
- Visit your frontend URL to ensure it loads correctly
- Test the API endpoints by visiting `https://your-backend-project.vercel.app/health`
- Verify that the chatbot and other features work end-to-end

## Troubleshooting

### Common Issues:

1. **Database Connection Timeouts**: Ensure your PostgreSQL provider allows connections from Vercel's IP ranges
2. **Cold Start Delays**: First requests after inactivity may be slow; subsequent requests will be faster
3. **API Limits**: Monitor your external API usage (OpenRouter, Qdrant) to ensure you don't exceed rate limits
4. **Environment Variables**: Double-check that all required environment variables are set in both deployments

### Performance Tips:

1. **Optimize Package Size**: Keep your Python dependencies minimal to reduce cold start times
2. **Connection Pooling**: The configuration uses NullPool for serverless environments, which is appropriate
3. **Caching**: Consider implementing caching strategies for frequently accessed data
4. **CDN**: Vercel's CDN will cache your frontend assets automatically

## Scaling Considerations

- Monitor your Vercel usage to ensure you stay within your plan's limits
- Consider upgrading to a Pro plan if you expect high traffic
- For very high loads, consider using Vercel's Regions feature to deploy closer to your users