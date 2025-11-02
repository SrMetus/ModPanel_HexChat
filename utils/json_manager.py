# utils/json_manager.py
# Ruta: C:\Users\Metus\AppData\Roaming\HexChat\addons\ModPanel_HexChat\utils\json_manager.py

import json
from pathlib import Path
import hexchat 

# === RUTA DEL ARCHIVO JSON (DENTRO DE LA CARPETA DEL PLUGIN) ===
# HexChat nos da la ruta exacta del addon
ADDON_DIR = Path(hexchat.get_info("configdir")) / "addons" / "ModPanel_HexChat"
DATA_DIR = ADDON_DIR / "data"
REASONS_FILE = DATA_DIR / "reasons.json"


# === ASEGURAR QUE EXISTE LA CARPETA data/ ===
def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# === CARGAR EL JSON ===
def load_reasons():
    ensure_data_dir()
    
    if not REASONS_FILE.exists():
        hexchat.prnt("[ModPanel] ERROR: No se encontró data/reasons.json")
        hexchat.prnt("[ModPanel] Crea el archivo con tu configuración.")
        return {}
    
    try:
        with open(REASONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Asegurar estructura básica
        for key in ["kick", "ban", "warm", "info_kick", "info_ban", "rules"]:
            if key not in data:
                data[key] = {}
        if "contador_total" not in data:
            data["contador_total"] = 0
            
        return data
        
    except json.JSONDecodeError as e:
        hexchat.prnt(f"[ModPanel] JSON inválido: {e}")
        return {}
    except Exception as e:
        hexchat.prnt(f"[ModPanel] Error al leer JSON: {e}")
        return {}


# === GUARDAR EL JSON ===
def save_reasons(data):
    ensure_data_dir()
    try:
        with open(REASONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        hexchat.prnt(f"[ModPanel] Error al guardar JSON: {e}")


# === INCREMENTAR CONTADOR ===
def increment_counter(action_type, motive_id):
    data = load_reasons()
    
    # Solo incrementa si existe la acción (kick, ban, warm)
    if action_type in data and motive_id in data[action_type]:
        # Asegurar que "usado" existe
        if "usado" not in data[action_type][motive_id]:
            data[action_type][motive_id]["usado"] = 0
        data[action_type][motive_id]["usado"] += 1
        
        # Incrementar total global
        data["contador_total"] += 1
        
        save_reasons(data)
        
    return data


# === REEMPLAZAR PLACEHOLDERS (IGUAL QUE EN modpanel.py) ===
def format_motivo(motivo, nick=None, channel=None):
    if channel:
        motivo = motivo.replace("$chan", channel)
        motivo = motivo.replace("%chan", channel)
    if nick:
        motivo = motivo.replace("$nick", nick)
        motivo = motivo.replace("$$1", nick)
    return motivo


# === PRUEBA RÁPIDA (solo si ejecutas el archivo directamente) ===
if __name__ == "__main__":
    print("=== PRUEBA DE json_manager.py ===")
    reasons = load_reasons()
    print(f"Total acciones: {reasons.get('contador_total', 0)}")
    if "info_kick" in reasons and "3" in reasons["info_kick"]:
        print(f"Info Kick 3: {reasons['info_kick']['3']['motivo']}")