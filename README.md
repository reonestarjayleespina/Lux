# LUX

## Structure

- `backend/` Minimal FastAPI API for filter preset metadata.
- `frontend/` Vue 3 + Vite + Tailwind UI for the Snappy-style 3-shot booth flow and stitched strip download.

## Privacy model

- No upload endpoint is included.
- No database, filesystem image persistence, or background storage is configured.
- Captured frames stay in the browser and are saved with a direct download.
- The completed 3-photo strip is composed client-side on a canvas.

## Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server will be available at `http://localhost:5173`.

## Filter presets endpoint

- `GET /api/filter-presets` returns the list of photobooth filter definitions used by the frontend.
- `GET /api/config` returns branding metadata for the watermark text shown on the final strip.
- `GET /api/health` confirms the API is alive and declares that processing is local only.

## Frontend flow

- Tap `Ready? Start` on the landing state when you are set.
- A 5-second on-screen countdown runs before the first shot, followed by 3-second `Strike a Pose` countdowns.
- Three photos are captured automatically, then stitched into a white-bordered vertical strip with a configurable LUX watermark.
- `Download` saves the PNG locally, and `Retake` resets the session without server storage.

## Notes

- The frontend falls back to bundled filter definitions if the backend is offline.
- The app mirrors the live preview for a more natural booth feel, then flips the canvas capture back to a normal orientation.
- The app uses CSS filters for the live preview and the canvas `filter` property for the captured frames.
- The grain preset adds a browser-side texture overlay in preview and on the captured frame.