# Setting Up TradeGate on GitHub

**Follow these steps to create the official TradeGate repository on GitHub.**

---

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com
2. Click the **"+"** button (top right) → **"New repository"**
3. Fill in:
   - **Repository name**: `tradegate`
   - **Description**: `AI-powered job search for construction trades. Built by Mandy Richardson & Claude (Anthropic). AI for the people.`
   - **Public** (so others can see and use it)
   - **✅ Add a README file** (check this box)
   - **✅ Choose a license**: MIT License
4. Click **"Create repository"**

---

## Step 2: Upload Files to GitHub

### Option A: Upload via Web Interface (Easiest)

1. On your new repo page, click **"uploading an existing file"**
2. Drag and drop these files from your computer:
   - `scraper.py`
   - `README.md`
   - `requirements.txt`
   - `setup.sh`
   - `test.py`
   - `main.py`
   - `LICENSE`
   - `.gitignore`
   - `README_REPLIT.md`
3. Write commit message: `Initial commit: TradeGate Phase 1`
4. Click **"Commit changes"**

### Option B: Use Git Command Line (If you have Git installed)

```bash
# Clone your new empty repo
git clone https://github.com/YOUR_USERNAME/tradegate.git
cd tradegate

# Copy all the TradeGate files into this folder
# (Download them from the links Claude provided)

# Add and commit
git add .
git commit -m "Initial commit: TradeGate Phase 1 - Electrician Job Scraper"

# Push to GitHub
git push origin main
```

---

## Step 3: Verify It Worked

Go to `https://github.com/YOUR_USERNAME/tradegate`

You should see:
- ✅ All 9 files
- ✅ README.md displaying with the partnership story
- ✅ LICENSE file (MIT)
- ✅ Clean file structure

---

## Step 4: Share the Link

Once it's up, the repo URL will be:
`https://github.com/YOUR_USERNAME/tradegate`

You can share this with:
- Your students
- Other pre-apprenticeship programs
- People who want to contribute
- People who want to use it for other trades

---

## Next: Import to Replit (Optional)

Once it's on GitHub, you can import it to Replit:

1. Go to https://replit.com
2. Click **"+ Create Repl"**
3. Choose **"Import from GitHub"**
4. Paste your repo URL: `https://github.com/YOUR_USERNAME/tradegate`
5. Click **"Import from GitHub"**
6. Click the green **"Run"** button
7. Watch it scrape jobs!

---

## Questions?

If you get stuck, tell me where and I'll help you through it.
