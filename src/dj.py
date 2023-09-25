from flask import jsonify
import random
import os


def get_random_tracks(num_tracks, music_type):
    # Define the directory path for the specified music type
    music_directory = f'./music/{music_type}'
    
    # Check if the directory exists
    if not os.path.exists(music_directory):
        return []

    track_names = os.listdir(music_directory)
    random.shuffle(track_names)
    return track_names[:num_tracks]


def create_playlist(num_tracks, music_type):
    playlist = {}
    random_tracks = get_random_tracks(num_tracks, music_type=music_type)
    
    for i, track_filename in enumerate(random_tracks, start=1):
        track_name = f"Track {i}"
        playlist[i] = {
            "name": track_filename[0: -4],
            "file": track_filename
        }
    
    return jsonify(playlist)