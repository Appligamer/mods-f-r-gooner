import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

# --- KONFIGURATION ---
# Ersetze diesen Link mit dem Direktdownload-Link zu deiner mods.zip auf GitHub
GITHUB_MODS_URL = "https://github.com/DEIN_NUTZERNAME/DEIN_REPO/raw/main/mods.zip"

def install_mods():
    # 1. Pfad zum Minecraft-Ordner ermitteln
    appdata = os.getenv('APPDATA')
    mods_path = Path(appdata) / ".minecraft" / "mods"
    temp_zip = Path(appdata) / "temp_mods.zip"

    print(f"Zielverzeichnis: {mods_path}")

    # 2. Mods-Ordner erstellen, falls er nicht existiert
    if not mods_path.exists():
        os.makedirs(mods_path)
        print("Mods-Ordner wurde erstellt.")

    try:
        # 3. ZIP-Datei von GitHub herunterladen
        print("Lade Mods von GitHub herunter... Bitte warten.")
        with urllib.request.urlopen(GITHUB_MODS_URL) as response, open(temp_zip, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        
        # 4. Alten Inhalt im Mods-Ordner löschen (optional, aber empfohlen für Sauberkeit)
        print("Bereinige alten Mods-Ordner...")
        for file in os.listdir(mods_path):
            file_path = mods_path / file
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Fehler beim Löschen von {file}: {e}")

        # 5. ZIP entpacken
        print("Entpacke Mods direkt in den Ordner...")
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(mods_path)

        # 6. Aufräumen
        os.remove(temp_zip)
        
        print("\n" + "="*40)
        print("INSTALLATION ERFOLGREICH!")
        print(f"Alle Mods für 1.21.5 sind nun im Ordner.")
        print("="*40)

    except Exception as e:
        print(f"\nFEHLER: {e}")
        print("Stelle sicher, dass der GitHub-Link korrekt ist.")

if __name__ == "__main__":
    install_mods()
    input("\nDrücke Enter zum Beenden...")