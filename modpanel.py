# modpanel.py
# Ruta: C:\Users\Metus\AppData\Roaming\HexChat\addons\ModPanel_HexChat\modpanel.py

import hexchat

# === METADATOS DEL PLUGIN (OBLIGATORIOS) ===
__module_name__ = "ModPanel Pro"
__module_version__ = "1.0"
__module_description__ = "Panel de moderación profesional con motivos y contadores"


# === FUNCIÓN: CARGAR EL JSON ===
def load_reasons():
    try:
        from utils.json_manager import load_reasons as load_json
        data = load_json()
        return data
    except Exception as e:
        hexchat.prnt(f"[ModPanel] ERROR al cargar reasons.json: {e}")
        return {}


# === FUNCIÓN: REEMPLAZAR PLACEHOLDERS ===
def format_motivo(motivo, nick=None, channel=None):
    if channel:
        motivo = motivo.replace("$chan", channel)
        motivo = motivo.replace("%chan", channel)
    if nick:
        motivo = motivo.replace("$nick", nick)
        motivo = motivo.replace("$$1", nick)
    return motivo


# === AL CARGAR EL PLUGIN ===
def on_load():
    reasons = load_reasons()
    total = reasons.get("contador_total", 0)
    
    # Mensaje bonito en el chat
    hexchat.prnt("┌────────────────────────────────────────────────────┐")
    hexchat.prnt("│          MODPANEL PRO CARGADO CORRECTAMENTE         │")
    hexchat.prnt("│                                                    │")
    hexchat.prnt(f"│  Total de acciones registradas: {total:>6}          │")
    hexchat.prnt("│                                                    │")
    hexchat.prnt("│  Comandos disponibles:                             │")
    hexchat.prnt("│     /modpanel test     → prueba rápida             │")
    hexchat.prnt("│     /modpanel show     → abrir panel (próximamente)│")
    hexchat.prnt("│     /modpanel reload   → recargar plugin           │")
    hexchat.prnt("└────────────────────────────────────────────────────┘")


# === COMANDO: /modpanel ===
def modpanel_cmd(word, word_eol, userdata):
    # word[0] = "modpanel", word[1] = subcomando
    if len(word) < 2:
        hexchat.prnt("Uso: /modpanel <test|show|reload>")
        return hexchat.EAT_ALL

    subcmd = word[1].lower()

    # --- SUBCOMANDO: test ---
    if subcmd == "test":
        reasons = load_reasons()
        if "info_kick" not in reasons or "3" not in reasons["info_kick"]:
            hexchat.prnt("[TEST] ERROR: No se encontró info_kick 3")
            return hexchat.EAT_ALL
        
        info_text = reasons["info_kick"]["3"]["motivo"]
        full_text = reasons["kick"]["3"]["motivo"]
        final_text = format_motivo(full_text, nick="troll1", channel="#charla")

        hexchat.prnt(f"[TEST] Info Kick 3: {info_text}")
        hexchat.prnt(f"[TEST] Motivo completo: {final_text}")

    # --- SUBCOMANDO: show ---
    elif subcmd == "show":
        hexchat.prnt("Próximamente: ventana GTK flotante sin bordes...")
        hexchat.prnt("Sigue el curso, alumno estrella")

    # --- SUBCOMANDO: reload ---
    elif subcmd == "reload":
        hexchat.prnt("Recargando ModPanel Pro...")
        hexchat.command("py reload modpanel")
        return hexchat.EAT_ALL

    else:
        hexchat.prnt(f"Comando desconocido: {subcmd}")
        hexchat.prnt("Usa: /modpanel <test|show|reload>")

    return hexchat.EAT_ALL


# === REGISTRAR EL COMANDO ===
hexchat.hook_command("modpanel", modpanel_cmd, help="/modpanel <test|show|reload>")


# === AL INICIAR ===
on_load()


# === AL CERRAR HEXCHAT O RECARGAR ===
def on_unload(userdata):
    hexchat.prnt("ModPanel Pro cerrado. ¡Hasta la próxima, moderador!")
hexchat.hook_unload(on_unload)