# 🎵 Spotify to YouTube Playlist Transfer

Trasferisci automaticamente le tue playlist da Spotify a YouTube con questo tool Python semplice da usare.

- ✅ Trasferimento automatico di playlist complete
- ✅ Ricerca intelligente dei video su YouTube
- ✅ Ripresa automatica in caso di interruzione (quota YouTube si esaurisce dopo una sesantina di ricerche)
- ✅ Gestione errori e rate limiting
- ✅ Progress tracking in tempo reale

## 📋 Prerequisiti

- Python 3.7 o superiore
- Account Spotify
- Account Google/YouTube
- 15 minuti per la configurazione iniziale

## 🚀 Installazione

### 1. Clona o scarica il repository

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```
### 3. Configura le credenziali

#### Opzione A: Sostituisci le tue credenziali di spotify in app.py':
   
   Ottienili da: https://developer.spotify.com/dashboard
   ...
   SPOTIFY_CLIENT_ID = 'inserisci_qui_il_tuo_client_id'
   SPOTIFY_CLIENT_SECRET = 'inserisci_qui_il_tuo_client_secret'
   ...

#### Opzione B: Usando variabili d'ambiente

```bash
export SPOTIFY_CLIENT_ID='tuo_client_id'
export SPOTIFY_CLIENT_SECRET='tuo_client_secret'
```

## 🔑 Setup Credenziali

### Spotify API

1. Vai su [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Clicca su **"Create app"**
3. Compila i campi:
   - **App name**: "Playlist Transfer" (o qualsiasi nome)
   - **App description**: "Transfer playlists to YouTube"
   - **Redirect URI**: `http://127.0.0.1:8888/callback` ⚠️ IMPORTANTE: usa esattamente questo URL
   - **API/SDKs**: Seleziona "Web API"
4. Dopo la creazione, copia **Client ID** e **Client Secret**
5. Vai in **Settings** → **User Management** → **Add new user**
6. Aggiungi l'email dell'account Spotify da cui vuoi trasferire le playlist

### YouTube Data API

1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto (es. "Playlist Transfer")
3. Abilita **YouTube Data API v3**:
   - Menu laterale: **APIs & Services** → **Library**
   - Cerca "YouTube Data API v3"
   - Clicca **"Enable"**
4. Configura OAuth consent screen:
   - **APIs & Services** → **OAuth consent screen**
   - User Type: **External**
   - App name: "Playlist Transfer"
   - Aggiungi la tua email in **Test users**
5. Crea credenziali OAuth:
   - **APIs & Services** → **Credentials**
   - **Create Credentials** → **OAuth client ID**
   - Application type: **Desktop app**
   - Nome: "Playlist Transfer Desktop"
6. Scarica il file JSON e salvalo come `client_secrets.json` nella cartella del progetto

## 💻 Utilizzo

### Esecuzione base

```bash
python spotify_to_youtube.py
```

### Primo avvio

Al primo avvio:
1. Si aprirà il browser per autenticare con Spotify
2. Si aprirà il browser per autenticare con YouTube
3. Vedrai la lista delle tue playlist Spotify
4. Seleziona il numero della playlist da trasferire
5. L'app inizierà il trasferimento

### Ripresa dopo interruzione

Se il trasferimento si interrompe (quota YouTube esaurita o interruzione manuale):

```bash
python spotify_to_youtube.py
```

L'app ti chiederà:
```
⚠️ TRASFERIMENTO INTERROTTO TROVATO
Playlist: Nome Playlist
Ultima traccia processata: 66
Vuoi continuare da dove avevi interrotto? (s/n):
```

Rispondi **s** per continuare dalla stessa playlist YouTube!

## 📊 Limiti e Considerazioni

### Quota YouTube

- **Limite giornaliero gratuito**: 10,000 unità
- **Ricerca video**: ~100 unità
- **Aggiunta a playlist**: ~50 unità
- **Capacità giornaliera**: circa 60-70 canzoni

### Accuratezza

- Non sempre la canzone su YouTube corrisponde esattamente a quella Spotify
- Potrebbero essere trovate versioni live, cover o remix
- Alcune canzoni potrebbero non essere disponibili su YouTube

### Privacy

- Le playlist YouTube vengono create come **private** per default
- Per cambiarle in pubbliche, modifica questa riga nel codice:
  ```python
  'privacyStatus': 'private'  # Cambia in 'public' o 'unlisted'
  ```

## 📁 Struttura File

```
spotify-to-youtube-transfer/
├── spotify_to_youtube.py      # Script principale
├── requirements.txt           # Dipendenze Python
├── config.example.py          # Template configurazione
├── README.md                
└── transfer_progress.json    # Progresso salvato (creato automaticamente)
```

## 🔧 Troubleshooting

### "Invalid redirect URI" (Spotify)

Verifica che nel Spotify Dashboard sia configurato esattamente:
```
http://127.0.0.1:8888/callback
```

### "Access denied" o "403" (YouTube)

1. Vai su Google Cloud Console
2. **OAuth consent screen** → **Test users**
3. Aggiungi la tua email Gmail

### "Quota exceeded" (YouTube)

Hai esaurito la quota giornaliera. Rilancia il programma domani, l'app riprenderà automaticamente da dove si era fermata.

### "User not registered" (Spotify)

Nel Spotify Developer Dashboard, vai in **Settings** → **User Management** e aggiungi l'email dell'account da cui vuoi trasferire le playlist.

## 📝 To-Do / Idee Future

- [ ] Interfaccia grafica (GUI) con Tkinter o Flask
- [ ] Opzione per scegliere tra risultati multipli su YouTube
- [ ] Export log dettagliato delle canzoni non trovate
- [ ] Matching intelligente basato su durata e features audio

## ⚠️ Disclaimer

Questo tool è per **uso personale**. Rispetta i termini di servizio di:
- [Spotify Developer Terms](https://developer.spotify.com/terms)
- [YouTube API Terms](https://developers.google.com/youtube/terms/api-services-terms-of-service)

Creato usando:
- [Spotipy](https://spotipy.readthedocs.io/) - Spotify Web API wrapper
- [Google API Python Client](https://github.com/googleapis/google-api-python-client) - YouTube Data API

---

**⭐ Se questo progetto ti è stato utile, lascia una stella su GitHub!**
