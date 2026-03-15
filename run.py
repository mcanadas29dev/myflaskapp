"""from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)  
    #app.run(host="0.0.0.0")
"""
"""
HEALTHWANA — Entry Point
========================
Uso desarrollo : python run.py
Uso producción : gunicorn "run:app" --workers 4 --bind 0.0.0.0:5000
 
NUNCA arrancar con debug=True en producción.
El modo debug se controla exclusivamente con la variable de entorno FLASK_DEBUG.
"""
 
import os
from app import create_app
 
app = create_app()
 
if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)