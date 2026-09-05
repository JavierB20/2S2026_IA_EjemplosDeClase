# CODIGO 1

import os
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path


def cargar_env(archivo_env):
    """Carga variables de entorno manualmente desde un archivo .env sin dependencias externas."""
    env_file = Path(__file__).parent / archivo_env
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip("'\"")


# Cargar variables desde .env.bot1
cargar_env(".env.bot1")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_BASE = f"https://api.telegram.org/bot{TOKEN}"


def telegram_api(method, params=None):
    """Realiza una petición HTTP a la API de Telegram usando urllib."""
    url = f"{API_BASE}/{method}"
    if params:
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data)
    else:
        req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error en llamada a API ({method}): {e}")
        return None


def enviar_mensaje(chat_id, texto, parse_mode="Markdown"):
    """Envía un mensaje de texto a un chat específico."""
    params = {
        "chat_id": chat_id,
        "text": texto,
    }
    if parse_mode:
        params["parse_mode"] = parse_mode
    return telegram_api("sendMessage", params)


def procesar_comando(chat_id, user, texto):
    """Procesa los comandos recibidos."""
    cmd = texto.strip().split()[0].lower()
    first_name = user.get("first_name", "amigo/a")

    if cmd == "/start":
        mensaje = (
            f"¡Hola {first_name}! Soy tu bot de saludos (nativo con API HTTP).\n\n"
            "Comandos disponibles:\n"
            "• /saludar - Te da un saludo cordial\n"
            "• /despedir - Te da una despedida\n"
            "• /quiensoy - Muestra tu usuario y chat ID"
        )
        enviar_mensaje(chat_id, mensaje, parse_mode=None)

    elif cmd == "/saludar":
        enviar_mensaje(chat_id, f"¡Hola {first_name}! ¿Cómo estás el día de hoy? 😊", parse_mode=None)

    elif cmd == "/despedir":
        enviar_mensaje(chat_id, f"¡Hasta luego, {first_name}! Que tengas un excelente día. 👋", parse_mode=None)

    elif cmd == "/quiensoy":
        info = (
            "👤 *Información de tu Usuario:*\n"
            f"• *Nombre:* {user.get('first_name', '')}\n"
            f"• *Apellido:* {user.get('last_name', 'No configurado')}\n"
            f"• *Username:* @{user.get('username', 'No configurado')}\n"
        )
        enviar_mensaje(chat_id, info, parse_mode="Markdown")


def main():
    if not TOKEN or TOKEN == "tu_token_aqui":
        print("ERROR: Configura TELEGRAM_TOKEN en .env.bot1")
        return

    # Mensaje inicial al arrancar al CHAT_ID configurado
    if CHAT_ID:
        enviar_mensaje(
            CHAT_ID,
            "🤖 *Bot 1 (Saludos) conectado exitosamente.* (Sin librerías externas)",
            parse_mode="Markdown"
        )

    print(f"🤖 Bot 1 iniciado (Chat ID: {CHAT_ID}). Escuchando mensajes...")
    offset = None

    while True:
        try:
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset

            resultado = telegram_api("getUpdates", params)

            if resultado and resultado.get("ok"):
                for update in resultado.get("result", []):
                    offset = update["update_id"] + 1

                    message = update.get("message")
                    if not message:
                        continue

                    chat_id = message["chat"]["id"]
                    user = message.get("from", {})
                    texto = message.get("text", "")

                    if texto.startswith("/"):
                        procesar_comando(chat_id, user, texto)

        except KeyboardInterrupt:
            print("\nBot 1 detenido.")
            break
        except Exception as e:
            print(f"Error en el ciclo principal: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
