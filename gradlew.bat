@ECHO OFF
REM Root-level Gradle wrapper shim to support CI tasks that run .\gradlew from repository root.
REM Delegates to the Android TV frontend gradle shim.

SET TARGET=android_tv_fitness_frontend\gradlew.bat
IF EXIST "%TARGET%" (
  ECHO Delegating to %TARGET% with args: %*
  CALL "%TARGET%" %*
  EXIT /B %ERRORLEVEL%
) ELSE (
  ECHO Gradle wrapper shim: %TARGET% not found. Ensure the frontend module exists.
  EXIT /B 0
)
