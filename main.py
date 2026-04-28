#!/usr/bin/env python3
"""
Compatibility launcher for the TradeG8 backend.

The active FastAPI app now lives in backend/main.py. This root module keeps
older commands such as `python main.py` and `import main` working.
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.main import app  # noqa: E402


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
