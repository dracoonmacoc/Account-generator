# 🚂 Railway Deployment Setup

## Quick Start

### 1. Add to Railway
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select this repository
4. Railway will auto-detect the Dockerfile

### 2. Set Environment Variables

In Railway Dashboard → Variables, add:
```bash
ACCOUNTS_TO_CREATE=1
HEADLESS=true
USE_NOPECHA=true
NOPECHA_KEY=your_actual_key_here
```

### 3. Deploy & Monitor

Click "Deploy" and watch the logs for:
- ✅ Chrome driver initialized successfully
- 🔄 Creating account: [username]
- ✅ Account created successfully

## Important Notes

- **CAPTCHA**: Requires Nopecha key for automatic solving
- **Headless**: Must be true for Railway (no GUI available)
- **Browser**: Uses Chrome (not Edge) in Docker environment
- **Rate Limits**: Start with 1-2 accounts to test

## Get Nopecha Key

1. Visit https://nopecha.com/
2. Sign up and get API key
3. Add to Railway environment variables

## Troubleshooting

### Build fails
- Check Dockerfile syntax
- Verify all dependencies install

### Runtime errors
- Check logs: Railway Dashboard → Deployments → View Logs
- Verify environment variables are set
- Ensure Nopecha key is valid

### No accounts created
- Check CAPTCHA timeout settings
- Verify Nopecha has credits
- Review Roblox rate limiting
