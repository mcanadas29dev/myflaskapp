"""
HEALTHWANA — App Factory
========================
Crea y configura la instancia Flask.
Los blueprints se registran aquí; la lógica de rutas vive en routes.py.

Próximos pasos (descomentar cuando estén instalados):
    - Flask-Talisman  : cabeceras de seguridad HTTP / CSP / HSTS
    - Flask-WTF       : protección CSRF en formularios
    - Flask-Limiter   : rate limiting por IP
    - Flask-Mail      : envío de correos desde el formulario de contacto
    - Flask-SQLAlchemy: persistencia en base de datos
"""

import os
import logging
from pathlib import Path
from flask import Flask


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

# /app/app/__init__.py  →  BASE_DIR = /app
BASE_DIR = Path(__file__).resolve().parent.parent

def create_app() -> Flask:
    app = Flask(
        __name__, 
        template_folder="templates", 
        static_folder="static")
       # ,
       # static_folder=str(BASE_DIR / "static"),    # /app/static/ — ruta absoluta
       # static_url_path="/static")

    # ------------------------------------------------------------------
    # Configuración — nunca valores sensibles hardcodeados
    # ------------------------------------------------------------------
    secret = os.environ.get("SECRET_KEY")
    if not secret:
        raise RuntimeError(
            "SECRET_KEY no está definida. "
            "Genera una con: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    app.config["SECRET_KEY"] = secret
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    # ------------------------------------------------------------------
    # Blueprints
    # ------------------------------------------------------------------
    from app.routes import main
    app.register_blueprint(main)

    # ------------------------------------------------------------------
    # Manejadores de error
    # ------------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error("Internal server error: %s", e)
        from flask import render_template
        return render_template("500.html"), 500

    logger.info("App creada correctamente.")
    return app