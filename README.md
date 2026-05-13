# Ancient Vietnam AI Server (Simple Starter)

## Features
- FastAPI server
- Upload user face image
- Random ancient Vietnamese occupation costume prompt
- Stable Diffusion generation
- Placeholder architecture for future:
  - InsightFace
  - ControlNet
  - IP-Adapter
  - GFPGAN
  - Redis queue

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Endpoint
POST `/generate`

Form-data:
- file: image

## Notes
Current version is MVP only.
Face preservation/compositing is placeholder for architecture learning.
