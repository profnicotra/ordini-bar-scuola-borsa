	@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"
title Aggiornamento tabella SQLite - note
color 0A

echo ================================================
echo   Aggiornamento tabella ^"note^" SQLite
echo ================================================
echo.
echo Questo script:
echo - apre una finestra per scegliere il file .db/.sqlite
echo - crea una copia di backup del database
echo - ricrea la tabella note con la struttura richiesta
echo.

where sqlite3 >nul 2>nul
if errorlevel 1 (
  echo ERRORE: sqlite3.exe non e' nel PATH di Windows.
  echo.
  echo Soluzioni possibili:
  echo 1) installare SQLite e aggiungere sqlite3.exe al PATH
  echo 2) copiare sqlite3.exe nella stessa cartella di questo .bat
  echo.
  if exist "%~dp0sqlite3.exe" (
    set "SQLITE_EXE=%~dp0sqlite3.exe"
  ) else (
    pause
    exit /b 1
  )
) else (
  set "SQLITE_EXE=sqlite3"
)

for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; $f=New-Object System.Windows.Forms.OpenFileDialog; $f.Title='Seleziona database SQLite'; $f.Filter='Database SQLite (*.db;*.sqlite;*.sqlite3)|*.db;*.sqlite;*.sqlite3|Tutti i file (*.*)|*.*'; if($f.ShowDialog() -eq 'OK'){ $f.FileName }"`) do set "DBFILE=%%I"

if not defined DBFILE (
  echo Nessun file selezionato. Operazione annullata.
  pause
  exit /b 1
)

if not exist "%DBFILE%" (
  echo ERRORE: file non trovato:
  echo %DBFILE%
  pause
  exit /b 1
)

set "STAMP=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "STAMP=%STAMP: =0%"
set "BACKUP=%DBFILE%.backup_%STAMP%"

copy "%DBFILE%" "%BACKUP%" >nul
if errorlevel 1 (
  echo ERRORE: impossibile creare il backup.
  pause
  exit /b 1
)

echo.
echo Backup creato:
echo %BACKUP%
echo.
echo Esecuzione script SQL in corso...

"%SQLITE_EXE%" "%DBFILE%" ".read \"%~dp0rimuovi_unique_note.sql\""
if errorlevel 1 (
  echo.
  echo ERRORE durante l'esecuzione SQL.
  echo Il backup e' stato mantenuto.
  pause
  exit /b 1
)

echo.
echo Operazione completata con successo.
echo Database aggiornato: %DBFILE%
echo.
pause
exit /b 0
