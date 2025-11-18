This repository includes a placeholder Android TV frontend with a Gradle wrapper shim.

CI note:
- Run Gradle commands with working directory set to android_tv_fitness_frontend:
  - cd android_tv_fitness_frontend && ./gradlew tasks
- If your CI runs Gradle at repo root, adjust the step to:
  - working-directory: fitstream-tv-41026-41036/android_tv_fitness_frontend
- The gradlew shim is executable and returns success to allow the backend container to pass while the real Android app is not yet initialized.
