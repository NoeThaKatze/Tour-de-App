import os

import uvicorn
from dotenv import load_dotenv

_ = load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
