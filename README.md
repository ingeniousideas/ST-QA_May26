# ST-QA_May26
Adam's demo repo for assessment demonstration

This is Adam's simple (but not great) example API application for the ST&QA module. I have used AI (CoPilot) to generate code for the basic example scenario given on the Jan 26 assessment brief (staff info API). The API is written in Python, using the FastAPI library for simplicity (although this is just what CoPilot suggested). It has 3 endpoints (/health, /staff and /staff/{staff_id})

Basic examples of testing will be added as we go through the module - these won't always be great, and we will discuss as we go!

TO RUN THIS in code spaces: Type the following in the terminal:
pip install fastapi uvicorn

uvicorn app:app --reload

--reload automatically restarts the server when you edit your code (very useful for development!)

Once Uvicorn starts, it prints something like: Uvicorn running on http://127.0.0.1:8000 (if running locally), or if running in codespaces you will see the name of your codespace instead of 127.0.0.1:8000.

Then you can visit:

✔️ Auto generated Swagger UI http://127.0.0.1:8000/docs

✔️ Alternative ReDoc documentation /redoc

Testing the endpoints: Health check /health

Search staff /staff

Get staff by ID /staff/1
