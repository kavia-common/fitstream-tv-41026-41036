# fitstream-tv-41026-41036

Backend import verification:
- To ensure the FastAPI app imports without JSONDecodeError from env parsing, run:
  ```
  cd fitness_api_backend
  python -m src.api._import_verify
  ```
- Expected output: `OK import. CORS_ORIGINS(len)=<n>` and exit code 0.

Run backend unit tests:
- From the backend root:
  ```
  cd fitness_api_backend
  pytest -q
  ```