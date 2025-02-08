from typing import Optional
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

class SpotifyPlayer:
    def __init__(self) -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="",
            client_secret="",
            redirect_uri="http://localhost:3000/callback",
            scope="user-modify-playback-state user-read-playback-state"
        ))

        self.artist_mapping = {
            "1234": "spotify:artist:06HL4z0CvFAxyc27GXpf02",  # Taylor Swift
            "5678": "spotify:artist:3TVXtAsR1Inumwj472S9r4",  # Drake
            "9012": "spotify:artist:1uNFoZAHBGtllmzznpCI3s"   # Justin Bieber
        }

        self.last_card_read = None
        
    def get_active_device(self) -> Optional[str]:
        """Get the first available Spotify device."""
        devices = self.sp.devices()
        if devices:
            if not devices['devices']:
                return None
            # Return the first active device, or the first available device
            active_devices = [d for d in devices['devices'] if d['is_active']]
            return active_devices[0]['id'] if active_devices else devices['devices'][0]['id']

    def play_artist(self, artist_id) -> bool:
        """Play top tracks from the given artist."""
        try:
            # Get device to play on
            device_id = self.get_active_device()
            if not device_id:
                print("No available Spotify devices found")
                return False
            
            # Get artist's top tracks
            results = self.sp.artist_top_tracks(artist_id)
            if results:
                if not results['tracks']:
                    print("no tracks found for artist")
                    return False 
                
                # create list of track uris
                track_uris = [track['uri'] for track in results['tracks'][:5]]
            
            # Start playback
                self.sp.start_playback(device_id=device_id, uris=track_uris)
                return True

            raise RuntimeError("No results found for artist") 
            
        except Exception as e:
            print(f"Error playing music: {str(e)}")
            return False
    def run(self, rfid_scanner)-> None:
        while True:
            card_id, text = rfid_scanner.read_no_block()
            if card_id and card_id != self.last_card_read:
                print(f"Card ID: {card_id}")
                self.last_card_read = card_id
                artist_id = self.artist_mapping.get(str(card_id))
                if artist_id:
                    print(f"Playing music for card: {card_id}")
                    if self.play_artist(artist_id):
                        print("Playback started successfully")
                    else:
                        print("Failed to start playback")
                else:
                    print(f"Unknown card: {card_id}")
                
                time.sleep(0.1)  # Small delay to prevent CPU overhead

if __name__ == "__main__":
    player = SpotifyPlayer()
    rfid_scanner = SimpleMFRC522()
    player.run(rfid_scanner)
