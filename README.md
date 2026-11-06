# mono-sample

Two small apps in one repository:

- `api/` — a Python standard-library HTTP handler (`python3 -m unittest discover -s api -t .` runs its tests via the root gate; pytest-compatible).
- `web/` — a Node render module (`node --test web/*.test.js`).

Run the full gate with `bash check.sh`.
