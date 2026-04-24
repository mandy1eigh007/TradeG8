#!/bin/bash

echo "=================================="
echo "TradeG8 Complete Setup"
echo "Built by Mandy Richardson & Claude"
echo "=================================="
echo ""

# Backend setup
echo "📦 Setting up backend..."
if [ -f backend/requirements.txt ]; then
    cd backend
    pip install -r requirements.txt
    playwright install chromium
    cd ..
elif [ -f requirements.txt ]; then
    echo "backend/requirements.txt not found; using root requirements.txt"
    pip install -r requirements.txt
    playwright install chromium
else
    echo "No Python requirements file found. Skipping backend dependency install."
fi

# Frontend setup
echo "📦 Setting up frontend..."
if [ -d frontend ]; then
    cd frontend
    npm install
    cd ..
elif [ -f package.json ]; then
    echo "frontend/ not found; using root package.json"
    npm install
else
    echo "No frontend package.json found. Skipping frontend dependency install."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy backend/.env.example to backend/.env"
echo "2. Fill in your Supabase and API keys"
echo "3. Run backend from backend/ when the full backend tree is present"
echo "4. Run frontend from frontend/ when the full frontend tree is present"
echo ""
