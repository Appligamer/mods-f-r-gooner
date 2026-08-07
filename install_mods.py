import os
import urllib.request
import json
from pathlib import Path

# --- KONFIGURATION ---
MC_VERSION = "1.21" # Modrinth nutzt oft 1.21 für alle Unterversionen
LOADER = "fabric"
# Liste der Mod-IDs von Modrinth (Slugs aus der URL)
MOD_SLUGS = [
    "sodium", "iris", "distant-horizons", "fabric-api", "modmenu", 
    "cloth-config", "lithium", "starlight", "zoomify", "continuity",
    "ambient-sounds", "architectury", "balm", "better-xray", "creativecore",
    "dynamic-fps", "fancy-menu", "konkrete", "waystones", "voicechat"
    # Du kannst hier weitere Slugs aus den URLs von Modrinth hinzufügen
]

def get_download_url(slug):
    """Holt den direkten Download-Link der neuesten Version für 1.21.5 von Modrinth."""
    api_url = f"https://api.modrinth.com/v2/project/{slug}/version?game_versions=['{MC_VERSION}']&loaders=['{LOADER}']"
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'ModDownloader/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data:
                # Nimmt die neueste Version (Index 0) und die primäre Datei
                return data[0]['files'][0]['url'], data[0]['files'][0]['filename']
    except Exception as e:
        print(f"Fehler bei Mod {slug}: {e}")
    return None, None

def install():
    appdata = os.getenv('APPDATA')
    mods_folder = Path(appdata) / ".minecraft" / "mods"
    
    if not mods_folder.exists():
        mods_folder.mkdir(parents=True, exist_ok=True)

    # Liste der bereits vorhandenen Dateien einlesen
    existing_files = [f.name for f in mods_folder.iterdir() if f.is_file()]

    print(f"--- Prüfe Mods für Minecraft {MC_VERSION} ---")
    
    for slug in MOD_SLUGS:
        url, filename = get_download_url(slug)
        
        if not url:
            print(f"[!] Überspringe {slug}: Keine Version für {MC_VERSION} gefunden.")
            continue

        if filename in existing_files:
            print(f"[OK] {filename} ist bereits installiert.")
        else:
            print(f"[..] Lade {filename} herunter...")
            try:
                urllib.request.urlretrieve(url, mods_folder / filename)
                print(f"[+] {filename} erfolgreich installiert.")
            except Exception as e:
                print(f"[X] Fehler beim Download von {filename}: {e}")

    print("\nAlle Mods wurden geprüft und aktualisiert!")

if __name__ == "__main__":
    install()
    input("\nFertig! Drücke Enter...")