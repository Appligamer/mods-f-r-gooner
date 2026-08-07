# --- KONFIGURATION ---
$mcVersion = "1.21"
$loader = "fabric"
$modsDir = "$env:APPDATA\.minecraft\mods"

# Liste der Mod-Slugs von Modrinth (Teil der URL, z.B. modrinth.com/mod/sodium)
$modSlugs = @(
    "sodium", "iris", "distant-horizons", "fabric-api", "modmenu", 
    "cloth-config", "lithium", "starlight", "zoomify", "continuity",
    "ambient-sounds", "architectury", "balm", "better-xray", "creativecore",
    "dynamic-fps", "fancy-menu", "konkrete", "waystones", "voicechat"
)

# Ordner erstellen, falls nicht vorhanden
if (!(Test-Path $modsDir)) {
    New-Item -Path $modsDir -ItemType Directory -Force
}

Write-Host "--- Minecraft Mod-Prüfung gestartet ---" -ForegroundColor Cyan

foreach ($slug in $modSlugs) {
    try {
        # API-Abfrage für die neueste Version
        $apiUrl = "https://api.modrinth.com/v2/project/$slug/version?game_versions=['$mcVersion']&loaders=['$loader']"
        $versions = Invoke-RestMethod -Uri $apiUrl -Method Get
        
        if ($versions.Count -gt 0) {
            $latestVersion = $versions[0]
            $file = $latestVersion.files[0]
            $fileName = $file.filename
            $downloadUrl = $file.url
            $targetPath = Join-Path $modsDir $fileName

            # Prüfen, ob die Datei bereits existiert
            if (Test-Path $targetPath) {
                Write-Host "[OK] $fileName ist bereits vorhanden." -ForegroundColor Green
            } else {
                Write-Host "[..] Lade $fileName herunter..." -ForegroundColor Yellow
                Invoke-WebRequest -Uri $downloadUrl -OutFile $targetPath
                Write-Host "[+] $fileName erfolgreich installiert." -ForegroundColor Cyan
            }
        } else {
            Write-Host "[!] Keine Version für $slug auf $mcVersion gefunden." -ForegroundColor Gray
        }
    } catch {
        Write-Host "[X] Fehler bei Mod $slug : $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nFertig! Alle Mods wurden geprüft." -ForegroundColor Green