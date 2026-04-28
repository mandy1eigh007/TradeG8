# TradeG8 - 5 Minute Quickstart

Current implementation note: this repo has the Phase 1 scraper, Supabase schema, starter FastAPI backend, and starter React frontend scaffold. Several API endpoints are placeholders until the scraper, database, auth, and resume engine are fully wired together.

## Option 1: Replit

1. Go to https://replit.com
2. Click "Import from GitHub"
3. Paste: `https://github.com/YOUR_USERNAME/tradeg8`
4. Click "Run"

Done. It works once your environment variables are configured.

## Option 2: Local

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/tradeg8.git
cd tradeg8

# 2. Setup
./setup.sh

# 3. Configure
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys

# 4. Run backend
cd backend && python main.py

# 5. Run frontend in a new terminal
cd frontend && npm start
```

Open: http://localhost:3000

## Get Free API Keys

Supabase: https://supabase.com  
Hugging Face: https://huggingface.co/settings/tokens

All free tier. No credit card.
