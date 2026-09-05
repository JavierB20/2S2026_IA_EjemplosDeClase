# CODIGO 2

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


# Cargar variables desde .env.bot2
cargar_env(".env.bot2")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_BASE = f"https://api.telegram.org/bot{TOKEN}"

# Diccionario para almacenar la lista de compras por cada chat_id en memoria
listas_por_chat = {}


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


def procesar_mensaje(chat_id, texto):
    """Maneja los comandos y los elementos agregados a la lista de compras."""
    texto_limpio = texto.strip()
    if not texto_limpio:
        return

    # Inicializar lista si el chat no la tiene
    if chat_id not in listas_por_chat:
        listas_por_chat[chat_id] = []

    lista = listas_por_chat[chat_id]
    partes = texto_limpio.split()
    cmd = partes[0].lower()

    if cmd == "/start":
        msg = (
            "🛒 *¡Bienvenido al Bot de Lista de Compras!*\n\n"
            "*Instrucciones:*\n"
            "• Escribe cualquier texto o producto para agregarlo.\n"
            "• `/print` - Muestra la lista de compras.\n"
            "• `/borrar <número>` - Elimina un producto por su posición.\n"
            "• `/limpiar` - Vacía la lista completa."
        )
        enviar_mensaje(chat_id, msg, parse_mode="Markdown")

    elif cmd == "/print":
        if not lista:
            enviar_mensaje(chat_id, "📝 Tu lista de compras está vacía.", parse_mode=None)
            return

        respuesta = "🛒 *Lista de Compras:*\n\n"
        for i, item in enumerate(lista, 1):
            respuesta += f"{i}. {item}\n"
        enviar_mensaje(chat_id, respuesta, parse_mode="Markdown")

    elif cmd == "/borrar":
        if len(partes) < 2:
            enviar_mensaje(chat_id, "Uso: /borrar <número>. Ejemplo: /borrar 1", parse_mode=None)
            return
        try:
            indice = int(partes[1]) - 1
            if 0 <= indice < len(lista):
                eliminado = lista.pop(indice)
                enviar_mensaje(chat_id, f"🗑️ Eliminado de la lista: \"{eliminado}\".", parse_mode=None)
            else:
                enviar_mensaje(chat_id, f"⚠️ Número inválido. Debe estar entre 1 y {len(lista)}.", parse_mode=None)
        except ValueError:
            enviar_mensaje(chat_id, "⚠️ Por favor escribe un número válido. Ejemplo: /borrar 1", parse_mode=None)

    elif cmd == "/limpiar":
        listas_por_chat[chat_id] = []
        enviar_mensaje(chat_id, "🧹 La lista de compras ha sido vaciada.", parse_mode=None)

    elif cmd.startswith("/"):
        enviar_mensaje(chat_id, "⚠️ Comando no reconocido. Usa /print o escribe un producto para agregarlo.", parse_mode=None)

    else:
        # Texto normal: agregar a la lista
        lista.append(texto_limpio)
        enviar_mensaje(chat_id, f"✅ Agregado: \"{texto_limpio}\" (Total: {len(lista)} ítems).", parse_mode=None)


def main():
    if not TOKEN or TOKEN == "tu_token_aqui":
        print("ERROR: Configura TELEGRAM_TOKEN en .env.bot2")
        return

    # Mensaje inicial al arrancar al CHAT_ID configurado
    if CHAT_ID:
        enviar_mensaje(
            CHAT_ID,
            "🛒 *Bot 2 (Lista de Compras) conectado exitosamente.* (Sin librerías externas)",
            parse_mode="Markdown"
        )

    print(f"🛒 Bot 2 iniciado (Chat ID: {CHAT_ID}). Escuchando mensajes...")
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
                    texto = message.get("text", "")

                    if texto:
                        procesar_mensaje(chat_id, texto)

        except KeyboardInterrupt:
            print("\nBot 2 detenido.")
            break
        except Exception as e:
            print(f"Error en el ciclo principal: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
