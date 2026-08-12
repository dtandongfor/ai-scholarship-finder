# Demo deployment guide

## What is ready now

The frontend can be shared as a static site, and the API can run from any Python-friendly host. Example profiles, feedback, profile deletion, the beta notice, the project overview, and the matching flow all work without paid services.

## Before publishing

1. Deploy the `backend` service using its existing Python environment and start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
2. In the backend host's environment settings, set `DATABASE_URL` to the complete Neon production-branch connection string. Do not put this secret in GitHub or `config.js`.
3. Set `INTELLIBLE_ALLOWED_ORIGINS` to the exact address of the published frontend.
4. Serve the `frontend` folder as a static site.
5. Update `frontend/config.js` so `window.INTELLIBLE_API_BASE` is the public backend address, with no trailing slash.
6. Open the public address on a phone and test an example profile, profile deletion, feedback, and an official scholarship link.

When Intellible connects to a brand-new database, it automatically loads the reviewed, version-controlled scholarship catalog once. Later restarts preserve the database and do not duplicate those records.

## Important beta limitations

- The app does not submit scholarship applications or prefill third-party application sites.
- Matching is intentionally conservative: an opportunity is not shown unless the currently structured criteria confirm eligibility.
- The included SQLite database and in-memory write limit are suitable for a small demo. Before a broader launch, move to a managed database and a shared rate limiter.
- Keep the beta label and official-source reminder visible while the catalog is still growing.

## Simple demo walkthrough

1. Choose **Try an example profile**.
2. Point out the in-state and transfer pathways, when available.
3. Open a match and explain the visible eligibility reasons and remaining official requirements.
4. Show the **Project overview** link for the product’s purpose and scope.
5. Clear the browser demo profile with **Reset demo** when finished.
