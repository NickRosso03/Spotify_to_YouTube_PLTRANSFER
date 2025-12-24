"""
App per trasferire playlist da Spotify a YouTube
Requisiti: pip install spotipy google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os
import time
import json

# ============================================
# CONFIGURAZIONE
# ============================================

# Spotify credentials (da https://developer.spotify.com/dashboard)
SPOTIFY_CLIENT_ID = 'tuo_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'tuo_spotify_client_secret'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'

# YouTube credentials (da Google Cloud Console)
YOUTUBE_CLIENT_SECRETS_FILE = "client_secrets.json"  # Scaricalo da Google Cloud
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# File per salvare il progresso
PROGRESS_FILE = 'transfer_progress.json'

# ============================================
# GESTIONE PROGRESSO
# ============================================

def salva_progresso(spotify_playlist_id, youtube_playlist_id, indice_traccia, nome_playlist):
    """Salva il progresso del trasferimento"""
    progresso = {
        'spotify_playlist_id': spotify_playlist_id,
        'youtube_playlist_id': youtube_playlist_id,
        'indice_traccia': indice_traccia,
        'nome_playlist': nome_playlist
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progresso, f)

def carica_progresso():
    """Carica il progresso salvato"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return None

def cancella_progresso():
    """Cancella il file di progresso al completamento"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

# ============================================
# AUTENTICAZIONE SPOTIFY
# ============================================

def autentica_spotify():
    """Autentica con Spotify usando OAuth"""
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope='playlist-read-private playlist-read-collaborative'
    ))
    print("✓ Autenticato con Spotify")
    return sp

# ============================================
# AUTENTICAZIONE YOUTUBE
# ============================================

def autentica_youtube():
    """Autentica con YouTube usando OAuth"""
    creds = None
    
    # Carica credenziali salvate
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Se non ci sono credenziali valide, richiedi login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Salva le credenziali per la prossima volta
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    youtube = build('youtube', 'v3', credentials=creds)
    print("✓ Autenticato con YouTube")
    return youtube

# ============================================
# FUNZIONI SPOTIFY
# ============================================

def ottieni_playlist_spotify(sp):
    """Mostra le playlist dell'utente e permette di scegliere"""
    playlists = sp.current_user_playlists(limit=50)
    
    print("\n=== Le tue playlist Spotify ===")
    for idx, playlist in enumerate(playlists['items'], 1):
        print(f"{idx}. {playlist['name']} ({playlist['tracks']['total']} brani)")
    
    scelta = int(input("\nSeleziona numero playlist: ")) - 1
    return playlists['items'][scelta]

def ottieni_tracce_playlist(sp, playlist_id):
    """Estrae tutte le tracce da una playlist Spotify"""
    tracce = []
    results = sp.playlist_tracks(playlist_id)
    
    while results:
        for item in results['items']:
            track = item['track']
            if track:  # Evita tracce nulle
                tracce.append({
                    'nome': track['name'],
                    'artista': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'query': f"{track['name']} {track['artists'][0]['name']}"
                })
        
        # Gestisci paginazione
        results = sp.next(results) if results['next'] else None
    
    return tracce

# ============================================
# FUNZIONI YOUTUBE
# ============================================

def cerca_video_youtube(youtube, query):
    """Cerca un video su YouTube e restituisce il primo risultato"""
    try:
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=1,
            videoCategoryId='10'  # Categoria Musica
        )
        response = request.execute()
        
        if response['items']:
            video = response['items'][0]
            return {
                'video_id': video['id']['videoId'],
                'titolo': video['snippet']['title']
            }
    except Exception as e:
        error_str = str(e)
        # Se è errore di quota, rilancia l'eccezione
        if 'quota' in error_str.lower() or 'quotaExceeded' in error_str:
            raise  # Rilancia l'eccezione per gestirla nel ciclo principale
        print(f"  Errore ricerca: {e}")
    
    return None

def crea_playlist_youtube(youtube, titolo, descrizione=""):
    """Crea una nuova playlist su YouTube"""
    request = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': titolo,
                'description': descrizione
            },
            'status': {
                'privacyStatus': 'private'  # Cambia in 'public' o 'unlisted' se vuoi
            }
        }
    )
    response = request.execute()
    print(f"✓ Playlist creata: {titolo}")
    return response['id']

def aggiungi_video_a_playlist(youtube, playlist_id, video_id):
    """Aggiunge un video a una playlist YouTube"""
    try:
        request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
        request.execute()
        return True
    except Exception as e:
        print(f"  Errore aggiunta video: {e}")
        return False

# ============================================
# FUNZIONE PRINCIPALE
# ============================================

def trasferisci_playlist():
    """Funzione principale per trasferire la playlist"""
    print("=" * 50)
    print("TRASFERIMENTO PLAYLIST: Spotify → YouTube")
    print("=" * 50)
    
    # Autenticazione
    sp = autentica_spotify()
    youtube = autentica_youtube()
    
    # Controlla se c'è un trasferimento in corso
    progresso = carica_progresso()
    
    if progresso:
        print(f"\n⚠️  TRASFERIMENTO INTERROTTO TROVATO")
        print(f"Playlist: {progresso['nome_playlist']}")
        print(f"Ultima traccia processata: {progresso['indice_traccia']}")
        risposta = input("Vuoi continuare da dove avevi interrotto? (s/n): ").lower()
        
        if risposta == 's':
            # Continua dal trasferimento precedente
            playlist_id = progresso['spotify_playlist_id']
            playlist_youtube_id = progresso['youtube_playlist_id']
            nome_playlist = progresso['nome_playlist']
            indice_inizio = progresso['indice_traccia'] + 1
            
            print(f"\n✓ Riprendo dalla traccia {indice_inizio}")
        else:
            # Inizia nuovo trasferimento
            cancella_progresso()
            playlist_spotify = ottieni_playlist_spotify(sp)
            nome_playlist = playlist_spotify['name']
            playlist_id = playlist_spotify['id']
            indice_inizio = 0
            playlist_youtube_id = None
    else:
        # Nuovo trasferimento
        playlist_spotify = ottieni_playlist_spotify(sp)
        nome_playlist = playlist_spotify['name']
        playlist_id = playlist_spotify['id']
        indice_inizio = 0
        playlist_youtube_id = None
    
    print(f"\n📋 Playlist: {nome_playlist}")
    
    # Ottieni tracce
    print("⏳ Recupero tracce da Spotify...")
    tracce = ottieni_tracce_playlist(sp, playlist_id)
    print(f"✓ Trovate {len(tracce)} tracce totali")
    
    # Crea playlist YouTube solo se è un nuovo trasferimento
    if not playlist_youtube_id:
        print("\n⏳ Creo playlist su YouTube...")
        descrizione = f"Playlist trasferita da Spotify: {nome_playlist}"
        playlist_youtube_id = crea_playlist_youtube(youtube, nome_playlist, descrizione)
    else:
        print(f"\n✓ Uso playlist YouTube esistente")
    
    # Trasferisci tracce (dalla posizione salvata)
    if indice_inizio > 0:
        print(f"\n⏳ Riprendo trasferimento dalla traccia {indice_inizio + 1}...\n")
    else:
        print(f"\n⏳ Trasferimento in corso...\n")
    
    successi = 0
    fallimenti = 0
    
    for idx in range(indice_inizio, len(tracce)):
        traccia = tracce[idx]
        print(f"[{idx + 1}/{len(tracce)}] {traccia['nome']} - {traccia['artista']}")
        
        try:
            # Cerca video su YouTube
            video = cerca_video_youtube(youtube, traccia['query'])
            
            if video:
                # Aggiungi alla playlist
                if aggiungi_video_a_playlist(youtube, playlist_youtube_id, video['video_id']):
                    print(f"  ✓ Aggiunto: {video['titolo']}")
                    successi += 1
                else:
                    print(f"  ✗ Errore aggiunta")
                    fallimenti += 1
            else:
                print(f"  ✗ Video non trovato")
                fallimenti += 1
            
            # Salva progresso dopo ogni traccia
            salva_progresso(playlist_id, playlist_youtube_id, idx, nome_playlist)
            
            # Pausa per evitare rate limiting
            time.sleep(1)
            
        except Exception as e:
            # Se errore quota YouTube, salva e interrompi
            if 'quota' in str(e).lower() or 'quotaExceeded' in str(e):
                print(f"\n⚠️  QUOTA YOUTUBE ESAURITA")
                print(f"Progresso salvato alla traccia {idx}")
                print(f"Riavvia il programma domani per continuare!")
                salva_progresso(playlist_id, playlist_youtube_id, idx, nome_playlist)
                return
            else:
                print(f"  ✗ Errore: {e}")
                fallimenti += 1
                salva_progresso(playlist_id, playlist_youtube_id, idx, nome_playlist)
    
    # Trasferimento completato - cancella progresso
    cancella_progresso()
    
    # Riepilogo
    print("\n" + "=" * 50)
    print("TRASFERIMENTO COMPLETATO")
    print("=" * 50)
    print(f"✓ Successi: {successi}/{len(tracce)}")
    print(f"✗ Fallimenti: {fallimenti}/{len(tracce)}")
    print(f"📺 Link playlist: https://www.youtube.com/playlist?list={playlist_youtube_id}")

# ============================================
# ESECUZIONE
# ============================================

if __name__ == "__main__":
    # Verifica che le credenziali siano configurate
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("❌ ERRORE: Credenziali Spotify mancanti!")
        print("Configura SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET come variabili d'ambiente")
        print("Oppure modifica direttamente il file Python.")
        exit(1)
    
    if not os.path.exists(YOUTUBE_CLIENT_SECRETS_FILE):
        print(f"❌ ERRORE: File {YOUTUBE_CLIENT_SECRETS_FILE} non trovato!")
        print("Scarica il file OAuth da Google Cloud Console e salvalo nella stessa cartella.")
        exit(1)
    
    try:
        trasferisci_playlist()
    except KeyboardInterrupt:
        print("\n\n⚠ Trasferimento interrotto dall'utente")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
