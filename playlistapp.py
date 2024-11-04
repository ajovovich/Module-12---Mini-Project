from flask import Flask, request, jsonify

app = Flask(__name__)

# Data storage
playlists = {}
songs = {}

# Add a song
def add_song(song_id, name, artist, genre):
    songs[song_id] = {'name': name, 'artist': artist, 'genre': genre}

# Update a song
def update_song(song_id, name, artist, genre):
    if song_id in songs:
        songs[song_id] = {'name': name, 'artist': artist, 'genre': genre}
        return True
    return False

# Delete a song
def delete_song(song_id):
    return songs.pop(song_id, None) is not None

# Create a playlist
def create_playlist(playlist_name):
    playlists[playlist_name] = []

# Update a playlist
def update_playlist(playlist_name, new_name):
    if playlist_name in playlists:
        playlists[new_name] = playlists.pop(playlist_name)
        return True
    return False

# Delete a playlist
def delete_playlist(playlist_name):
    return playlists.pop(playlist_name, None) is not None

# Add a song to a playlist
def add_song_to_playlist(playlist_name, song_id):
    if playlist_name in playlists and song_id in songs:
        playlists[playlist_name].append(song_id)

# Remove a song from a playlist
def remove_song_from_playlist(playlist_name, song_id):
    if playlist_name in playlists:
        playlists[playlist_name] = [id for id in playlists[playlist_name] if id != song_id]

# Search for a song by name
def search_song_by_name(name):
    return [song for song in songs.values() if song['name'] == name]

# Sort songs in a playlist by key
def sort_playlist(playlist_name, key):
    if playlist_name in playlists:
        playlists[playlist_name].sort(key=lambda song_id: songs[song_id][key])

# Song Endpoints
@app.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    add_song(data['id'], data['name'], data['artist'], data['genre'])
    return jsonify({'message': 'Song created'}), 201

@app.route('/songs/<song_id>', methods=['PUT'])
def update_song_endpoint(song_id):
    data = request.json
    if update_song(song_id, data['name'], data['artist'], data['genre']):
        return jsonify({'message': 'Song updated'})
    return jsonify({'message': 'Song not found'}), 404

@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song_endpoint(song_id):
    if delete_song(song_id):
        return jsonify({'message': 'Song deleted'})
    return jsonify({'message': 'Song not found'}), 404

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song = songs.get(song_id)
    if song:
        return jsonify(song)
    return jsonify({'message': 'Song not found'}), 404

@app.route('/songs/search', methods=['GET'])
def search_song():
    name = request.args.get('name')
    results = search_song_by_name(name)
    return jsonify(results)

# Playlist Endpoints
@app.route('/playlists', methods=['POST'])
def create_playlist_endpoint():
    data = request.json
    create_playlist(data['name'])
    return jsonify({'message': 'Playlist created'}), 201

@app.route('/playlists/<playlist_name>', methods=['PUT'])
def update_playlist_endpoint(playlist_name):
    new_name = request.json['new_name']
    if update_playlist(playlist_name, new_name):
        return jsonify({'message': 'Playlist updated'})
    return jsonify({'message': 'Playlist not found'}), 404

@app.route('/playlists/<playlist_name>', methods=['DELETE'])
def delete_playlist_endpoint(playlist_name):
    if delete_playlist(playlist_name):
        return jsonify({'message': 'Playlist deleted'})
    return jsonify({'message': 'Playlist not found'}), 404

@app.route('/playlists/<playlist_name>', methods=['GET'])
def get_playlist(playlist_name):
    if playlist_name in playlists:
        playlist_songs = [songs[song_id] for song_id in playlists[playlist_name]]
        return jsonify(playlist_songs)
    return jsonify({'message': 'Playlist not found'}), 404

@app.route('/playlists/<playlist_name>/add_song', methods=['POST'])
def add_song_to_playlist_endpoint(playlist_name):
    song_id = request.json['song_id']
    add_song_to_playlist(playlist_name, song_id)
    return jsonify({'message': 'Song added to playlist'})

@app.route('/playlists/<playlist_name>/remove_song', methods=['POST'])
def remove_song_from_playlist_endpoint(playlist_name):
    song_id = request.json['song_id']
    remove_song_from_playlist(playlist_name, song_id)
    return jsonify({'message': 'Song removed from playlist'})

@app.route('/playlists/<playlist_name>/sort', methods=['POST'])
def sort_playlist_endpoint(playlist_name):
    key = request.json['key']
    sort_playlist(playlist_name, key)
    return jsonify({'message': 'Playlist sorted'})

if __name__ == '__main__':
    app.run(debug=True)
