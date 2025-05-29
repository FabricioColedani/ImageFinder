@echo off
cd /d "%~dp0"

REM Ejecutar la app Python en segundo plano
start python app.py

REM Esperar unos segundos para que el servidor arranque (podés ajustar el tiempo)
timeout /t 5 /nobreak > nul

REM Abrir el navegador con la URL local
start http://localhost:5000

REM Mantener la ventana abierta para ver mensajes
pause
