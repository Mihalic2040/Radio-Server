const audioPlayer = document.getElementById('audio-player');
const audioSource = document.getElementById('audio-source');
const currentTrack = document.getElementById('current-track');
const volumeSlider = document.getElementById('volume-slider');
const volumeLabel = document.getElementById('volume-label');
const playlistElement = document.getElementById('playlist');

let playlist = [];
let currentTrackIndex = 0;

// Function to set the player volume
function setVolume(volume) {
    audioPlayer.volume = volume;
    // Save the volume to Local Storage
    localStorage.setItem('playerVolume', volume);
}

// Function to load the player volume from Local Storage
function loadVolume() {
    const savedVolume = localStorage.getItem('playerVolume');
    if (savedVolume !== null) {
        setVolume(parseFloat(savedVolume));
        volumeSlider.value = savedVolume;
        volumeLabel.textContent = `Volume: ${(savedVolume * 100).toFixed(0)}%`;
    }
}

// Function to play the current track
function playCurrentTrack() {
    const track = playlist[currentTrackIndex];
    if (track) {
        audioSource.src = '/music/' + track.file;
        audioPlayer.load();
        audioPlayer.play();
        currentTrack.textContent = track.name;
        displayPlaylist()
    }
}

// Function to fetch and load the playlist from the server
// function loadPlaylist() {
//     fetch('/create_playlist/') // Adjust the URL as needed
//         .then(response => response.json())
//         .then(data => {
//             if (data) {
//                 playlist = Object.values(data);
//                 currentTrackIndex = 0;
//                 playCurrentTrack();
//                 displayPlaylist();
//             }
//         })
//         .catch(error => console.error(error));
// }

// Function to display the playlist on the website
function displayPlaylist() {
    playlistElement.innerHTML = ''; // Clear the existing list

    for (let i = 0; i < playlist.length; i++) {
        const track = playlist[i];
        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center', 'playlist-item');
        
        // Create a div to hold the track icon
        const iconDiv = document.createElement('div');
        iconDiv.classList.add('track-icon');
        iconDiv.innerHTML = '<i class="bi bi-music-note"></i>'; // Example icon

        // Create a span for the track name
        const trackNameSpan = document.createElement('span');
        trackNameSpan.textContent = `${i + 1}. ${track.name}`;

        listItem.appendChild(iconDiv);
        listItem.appendChild(trackNameSpan);
        playlistElement.appendChild(listItem);

        // Add a class to the currently playing track
        if (i === currentTrackIndex) {
            listItem.classList.add('current-track');
        }
    }
}

// Add an event listener to the volume slider to adjust the volume
volumeSlider.addEventListener('input', (e) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    volumeLabel.textContent = `Volume: ${(newVolume * 100).toFixed(0)}%`;
});

// Add an event listener to play the next track when the current track ends
audioPlayer.addEventListener('ended', () => {
    currentTrackIndex++;
    if (currentTrackIndex >= playlist.length) {
        currentTrackIndex = 0; // Loop back to the first track
        loadPlaylist(); // Load a new playlist
    }
    playCurrentTrack();
});

// Initial load of the volume and playlist
loadVolume();
loadPlaylist();
