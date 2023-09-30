import spotipy
import os
import subprocess
from spotipy.oauth2 import SpotifyOAuth
from pyfiglet import Figlet

# Get CLIENT_ID and Secret from Spotify Development Page
# https://developer.spotify.com/dashboard

SPOTIPY_CLIENT_ID = "your_client_id"
SPOTIPY_CLIENT_SECRET = "your_client_secret"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
    )
)


green_color = "\033[38;5;40m"
blue_color = "\033[38;5;32m"
reset_color = "\033[0m"


def clear_console():
    subprocess.call("clear" if os.name == "posix" else "cls", shell=True)


def print_ascii_text():
    clear_console()
    f = Figlet(font="chunky")  
    ascii_text = f.renderText("dupeRemover")

    
    colored_ascii_text = f"{green_color}{ascii_text}{reset_color}"

    
    print(colored_ascii_text)

    
    print(f" {blue_color}Made with <3 by Alex{reset_color}\n")


def list_user_playlists():
    playlists = sp.current_user_playlists()
    for i, playlist in enumerate(playlists["items"], start=1):
        print(f"{green_color}{i}. {playlist['name']}{reset_color}")

    if not playlists["items"]:
        print("You have no playlists.")
        return None

    print()

    while True:
        try:
            selection = int(
                input("Enter the number of the playlist you want to check: ")
            )
            if 1 <= selection <= len(playlists["items"]):
                return playlists["items"][selection - 1]["id"]
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = [item["track"]["name"] for item in results["items"]]
    return tracks


def find_duplicates(tracks):
    seen = set()
    duplicates = set()

    for track in tracks:
        if track in seen:
            duplicates.add(track)
        else:
            seen.add(track)

    return list(duplicates)


def remove_all_duplicates(playlist_id, duplicate):
    
    playlist = sp.playlist(playlist_id)
    tracks_to_remove = [
        item["track"]["id"]
        for item in playlist["tracks"]["items"]
        if item["track"]["name"] == duplicate
    ]

    if tracks_to_remove:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, tracks_to_remove)


def remove_duplicate_tracks(playlist_id, duplicate):
    
    playlist = sp.playlist(playlist_id)
    tracks_to_remove = [
        item["track"]["id"]
        for item in playlist["tracks"]["items"]
        if item["track"]["name"] == duplicate
    ]

    if tracks_to_remove:
        
        sp.playlist_remove_all_occurrences_of_items(playlist_id, [tracks_to_remove[0]])


def main():
    while True:
        print_ascii_text()
        selected_playlist_id = list_user_playlists()

        if selected_playlist_id:
            tracks = get_playlist_tracks(selected_playlist_id)
            duplicates = find_duplicates(tracks)

            if duplicates:
                print(f"{blue_color}Duplicates found ({len(duplicates)}):{reset_color}")
                for i, duplicate in enumerate(duplicates):
                    print(f"[{i}] {duplicate}")

                print("[X] Remove all")

                while True:
                    option = input(
                        "Enter the number of the duplicate to remove or 'X' to remove all: "
                    )

                    if option.upper() == "X":
                        for duplicate in duplicates:
                            remove_all_duplicates(selected_playlist_id, duplicate)
                        break
                    elif option.isdigit():
                        index = int(option)
                        if 0 <= index < len(duplicates):
                            remove_duplicate_tracks(
                                selected_playlist_id, duplicates[index]
                            )
                            break
                        else:
                            print(
                                "Invalid index. Please enter a valid number or 'X' to remove all."
                            )
                    else:
                        print(
                            "Invalid input. Please enter a number or 'X' to remove all."
                        )
            else:
                print("No duplicates found.")

        restart_option = input("Do you want to process another playlist? (y/n): ")
        if restart_option.lower() != "y":
            print("Exiting the program. Goodbye!")
            break


if __name__ == "__main__":
    main()
