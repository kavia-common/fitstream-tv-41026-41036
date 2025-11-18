# Fitness API Backend

Import check
- Verify startup import does not fail due to JSONDecodeError or env parsing:
  ```
  python run_import_check.py
  ```

Run tests
- Execute unit tests (includes CORS parsing tests):
  ```
  pytest -q
  ```

Notes
- CORS env values like CORS_ORIGINS, allowed_origins, allowed_methods, allowed_headers accept JSON arrays or comma-separated strings.
- Empty/whitespace env values are treated as empty lists and defaulted safely by getters.
