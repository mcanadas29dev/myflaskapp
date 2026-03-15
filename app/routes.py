"""
HEALTHWANA — Rutas (Blueprint: main)
=====================================
Todas las rutas HTTP y el endpoint de la API de contacto.
La validación server-side es independiente de la validación client-side en JS.
"""

import re
import logging
from flask import Blueprint, render_template, request, jsonify

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


# ----------------------------------------------------------------------
# Páginas
# ----------------------------------------------------------------------

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ----------------------------------------------------------------------
# API: formulario de contacto
# ----------------------------------------------------------------------

@main.route("/api/contact", methods=["POST"])
def api_contact():
    """
    Recibe solicitudes de consulta desde el formulario de contacto.

    TODO (próximos pasos):
        - Flask-Limiter  : @limiter.limit("5 per hour")
        - Flask-WTF      : validación del token CSRF
        - Flask-Mail     : enviar email de confirmación al cliente
        - Flask-SQLAlchemy: guardar solicitud en la base de datos
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Petición no válida."}), 400

    name    = str(data.get("name",    "")).strip()
    email   = str(data.get("email",   "")).strip()
    phone   = str(data.get("phone",   "")).strip()
    goal    = str(data.get("goal",    "")).strip()
    message = str(data.get("message", "")).strip()

    errors = _validate_contact(name, email, phone, goal, message)
    if errors:
        return jsonify({"error": errors[0]}), 422

    # Sin PII en los logs
    logger.info("Nueva solicitud de consulta recibida. Objetivo: %s", goal)

    # TODO: enviar email / guardar en BD

    return jsonify({"message": "Solicitud recibida correctamente."}), 200


# ----------------------------------------------------------------------
# Validación server-side
# ----------------------------------------------------------------------

_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_PHONE_RE = re.compile(r"^\+?[\d\s\-().]{7,25}$")
_ALLOWED_GOALS = frozenset({
    "fat_loss", "muscle_gain", "anti_ageing",
    "performance", "disease_prevention", "general",
})


def _validate_contact(
    name: str,
    email: str,
    phone: str,
    goal: str,
    message: str,
) -> list[str]:
    """Devuelve una lista de errores, o lista vacía si todo es válido."""
    errors: list[str] = []

    if not name or not (2 <= len(name) <= 100):
        errors.append("Introduce un nombre completo válido (2–100 caracteres).")

    if not email or not _EMAIL_RE.match(email) or len(email) > 254:
        errors.append("Introduce una dirección de email válida.")

    if phone and not _PHONE_RE.match(phone):
        errors.append("Introduce un número de teléfono válido.")

    if goal not in _ALLOWED_GOALS:
        errors.append("Selecciona un objetivo válido.")

    if len(message) > 1500:
        errors.append("El mensaje no puede superar los 1.500 caracteres.")

    return errors