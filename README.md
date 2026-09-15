# 🎵 Spotify to YouTube Playlist Transfer

A simple Python tool to automatically transfer your playlists from Spotify to YouTube using their official APIs. Handles authentication, intelligent video matching, automatic resume on interruption, and YouTube's daily quota limits.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Limitations](#limitations--quota-management)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

✅ **Automatic Playlist Transfer** — Copy entire playlists from Spotify to YouTube in one command  
✅ **Smart Video Matching** — Searches YouTube for each track by title and artist  
✅ **Resume on Interruption** — Automatically saves progress; continue from where you left off  
✅ **Quota-Aware** — Gracefully pauses when YouTube's daily limit is reached  
✅ **Real-Time Progress** — Visual feedback on transfer status  
✅ **Error Handling** — Skips unavailable tracks without stopping the entire transfer  

---

## Requirements

| Requirement | Minimum Version |
|---|---|
| **Python** | 3.7+ |
| **Spotify Account** | Free or Premium |
| **Google/YouTube Account** | Any valid Gmail account |
| **Time for Setup** | ~15 minutes (one-time) |

---

## Installation

### 1. Clone or Download the Repository

```bash
git clone https://github.com/NickRosso03/Spotify_to_YouTube_PLTRANSFER.git
cd Spotify_to_YouTube_PLTRANSFER
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What's included:**
- `spotipy` — Spotify Web API wrapper
- `google-auth-oauthlib` — Google OAuth authentication
- `google-auth-httplib2` — HTTP transport for Google Auth
- `google-api-python-client` — YouTube Data API v3

---

## Configuration

### Step 1: Set Up Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **"Create an App"**
3. Fill in the form:
   - **App name:** "Playlist Transfer" (or any name)
   - **App description:** "Transfer playlists to YouTube"
   - **Accept the terms** and create the app
4. In the app settings, copy your:
   - **Client ID**
   - **Client Secret**
5. Add a **Redirect URI**:
   - Click **Edit Settings**
   - Under "Redirect URIs," add: `http://127.0.0.1:8888/callback`
   - ⚠️ Use this exact URL — custom URLs may cause authentication errors
   - Save
6. Register your account as a test user:
   - Go to **Users Management** → **Add New User**
   - Enter the email of the Spotify account you'll transfer playlists from

### Step 2: Set Up YouTube Data API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Create a new project:**
   - Click **Select Project** (top-left)
   - Click **NEW PROJECT**
   - Name it "Playlist Transfer" and create it
3. **Enable YouTube Data API v3:**
   - Go to **APIs & Services** → **Library**
   - Search for "YouTube Data API v3"
   - Click **Enable**
4. **Configure OAuth consent screen:**
   - Go to **APIs & Services** → **OAuth consent screen**
   - User Type: **External**
   - App name: "Playlist Transfer"
   - Add your email as a **Test user**
   - Save and continue
5. **Create OAuth credentials:**
   - Go to **APIs & Services** → **Credentials**
   - Click **+ Create Credentials** → **OAuth client ID**
   - Application type: **Desktop application**
   - Name: "Playlist Transfer Desktop"
   - Click **Create**
6. **Download and save the credentials file:**
   - Click the download button (⬇️) next to your newly created credential
   - Rename the file to `client_secrets.json`
   - Move it to the repository folder (same directory as `app.py`)

### Step 3: Add Credentials to the App

**Option A: Set environment variables** (Recommended for security)

```bash
# Linux / macOS
export SPOTIFY_CLIENT_ID='your_client_id'
export SPOTIFY_CLIENT_SECRET='your_client_secret'

# Windows (Command Prompt)
set SPOTIFY_CLIENT_ID=your_client_id
set SPOTIFY_CLIENT_SECRET=your_client_secret

# Windows (PowerShell)
$env:SPOTIFY_CLIENT_ID='your_client_id'
$env:SPOTIFY_CLIENT_SECRET='your_client_secret'
```

**Option B: Edit `app.py` directly**

Open `app.py` and replace lines 21–22:
```python
SPOTIFY_CLIENT_ID = 'your_client_id_here'
SPOTIFY_CLIENT_SECRET = 'your_client_secret_here'
```

---

## Usage

### First Run

```bash
python app.py
```

The app will:
1. Open a browser window for **Spotify authentication** — log in with your Spotify account
2. Open a browser window for **YouTube authentication** — log in with your Google account
3. Display your Spotify playlists with track counts
4. Prompt you to select a playlist by number
5. Create a matching playlist on YouTube and start transferring tracks

**Example output:**
```
==================================================
TRASFERIMENTO PLAYLIST: Spotify → YouTube
==================================================
✓ Autenticato con Spotify
✓ Autenticato con YouTube

=== Le tue playlist Spotify ===
1. Workout Mix (45 brani)
2. Chill Vibes (120 brani)
3. 80s Classics (67 brani)

Seleziona numero playlist: 1

📋 Playlist: Workout Mix
⏳ Recupero tracce da Spotify...
✓ Trovate 45 tracce totali
...
```

### Resume After Interruption

If the transfer is interrupted (YouTube quota exhausted, network issue, or manual stop):

```bash
python app.py
```

The app will detect the saved progress:
```
⚠️ TRASFERIMENTO INTERROTTO TROVATO
Playlist: Workout Mix
Ultima traccia processata: 28
Vuoi continuare da dove avevi interrotto? (s/n): s

✓ Riprendo dalla traccia 29
...
```

Type **`s`** to resume or **`n`** to start a new transfer.

### After Completion

Once the transfer finishes, you'll see:
```
==================================================
TRASFERIMENTO COMPLETATO
==================================================
✓ Successi: 45/45
✗ Fallimenti: 0/45
📺 Link playlist: https://www.youtube.com/playlist?list=PLxx...
```

---

## Limitations & Quota Management

### YouTube API Quota

YouTube imposes a **daily free quota** of **10,000 units**:

| Action | Cost | Examples |
|---|---|---|
| Search video | ~100 units | 1 search = ~100 units |
| Add to playlist | ~50 units | 1 add = ~50 units |
| **Total per track** | ~150 units | Search + Add |
| **Daily capacity** | ~60–70 tracks | 10,000 ÷ 150 |

**When quota is exceeded:**
- The app saves your progress and exits
- ⏸️ **You must wait until the next calendar day** to resume
- Run `python app.py` the next day to continue automatically
- Your progress is preserved in `transfer_progress.json`

### Track Matching Accuracy

- ⚠️ YouTube results may differ from Spotify originals (live versions, covers, remixes)
- 🎯 Tracks not found on YouTube are skipped (logged in progress output)
- 🔍 The app searches YouTube's **Music category** for the best results

### Privacy & Playlist Settings

By default, transferred playlists are created as **private** on YouTube. To change this:

1. Open `app.py` and find line 181:
   ```python
   'privacyStatus': 'private'  # Change to 'public' or 'unlisted'
   ```
2. Replace with:
   ```python
   'privacyStatus': 'public'   # Public playlists (or 'unlisted')
   ```
3. Run the app again for new transfers

---

## Troubleshooting

### ❌ "Invalid redirect URI" (Spotify authentication fails)

**Cause:** Mismatch between configured and actual redirect URI  
**Solution:**
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Edit your app settings
3. Verify the Redirect URI is **exactly**: `http://127.0.0.1:8888/callback`
4. Save and try again

---

### ❌ "Access denied" or "403" (YouTube authentication fails)

**Cause:** Your account isn't registered as a test user  
**Solution:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to **APIs & Services** → **OAuth consent screen**
4. Under **Test users**, click **+ Add user**
5. Enter your Gmail address
6. Save and try the app again

---

### ❌ "Quota exceeded" (YouTube)

**Cause:** Daily API quota limit reached (~60–70 playlists per day)  
**Solution:**
- ⏸️ The app automatically saves your progress
- 🕐 Wait until the next calendar day (12:00 AM UTC)
- Run `python app.py` to resume from where it stopped
- Your `transfer_progress.json` file preserves your position

---

### ❌ "User not registered" (Spotify)

**Cause:** The Spotify account hasn't been registered as a test user  
**Solution:**
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Edit your app
3. Go to **Settings** → **User Management**
4. Click **Add New User**
5. Enter the email of your Spotify account
6. Try the app again

---

### ❌ "File `client_secrets.json` not found" (YouTube credentials missing)

**Cause:** OAuth credentials file not in the repo folder  
**Solution:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Credentials**
3. Find your OAuth 2.0 Client ID (Desktop app)
4. Click the **download button** (⬇️)
5. Rename the downloaded file to **`client_secrets.json`**
6. Move it to the **same folder as `app.py`**
7. Try again

---

### ❌ "Spotipy/Google module not found"

**Cause:** Dependencies not installed  
**Solution:**
```bash
pip install -r requirements.txt
```

---

## File Structure

```
Spotify_to_YouTube_PLTRANSFER/
├── app.py                        # Main transfer script
├── requirements.txt              # Python dependencies
├── config.example.py             # Configuration template (unused in current version)
├── client_secrets.json           # YouTube OAuth credentials (create after setup)
├── transfer_progress.json        # Auto-generated progress file (resume data)
└── README.md                     # This file
```

---

## Future Improvements

- [ ] Graphical User Interface (GUI) using Tkinter or Flask
- [ ] Choose from multiple YouTube results for ambiguous tracks
- [ ] Export detailed log of unmatched tracks
- [ ] Intelligent matching using track duration and audio features
- [ ] Support for collaborative playlists
- [ ] Batch playlist transfer mode

---

## Disclaimer & Legal

This tool is **for personal use only**. Please respect the terms of service:

- [Spotify Developer Terms](https://developer.spotify.com/terms)
- [YouTube API Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service)

Ensure you have the right to transfer content from the playlists you're moving. This tool does not modify, copy, or redistribute content — it only links existing YouTube videos to a new YouTube playlist.

---

## Built With

- 🎵 [Spotipy](https://spotipy.readthedocs.io/) — Spotify Web API wrapper
- 🎬 [Google API Python Client](https://github.com/googleapis/google-api-python-client) — YouTube Data API v3
- 🔐 [google-auth-oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib) — OAuth 2.0 authentication

---

## Contributing

Found a bug or have an idea? Feel free to:
- Open an [Issue](https://github.com/NickRosso03/Spotify_to_YouTube_PLTRANSFER/issues)
- Submit a [Pull Request](https://github.com/NickRosso03/Spotify_to_YouTube_PLTRANSFER/pulls)

---

## License

This project is open source and available under the MIT License (or license of your choice).

---

**⭐ If this project saved you time, please consider leaving a star on GitHub!**
