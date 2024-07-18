import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CLIENT_ID = '84b2a106838b4135b2ba33bbb0b24df5';
const REDIRECT_URI = 'http://localhost:3000';
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'token';
const POLLING_INTERVAL = 500; // Polling interval in milliseconds (e.g., 5000 ms = 5 seconds)

function App() {
  const [token, setToken] = useState('');
  const [song, setSong] = useState(null);
  const [genreSeeds, setGenreSeeds] = useState([]);

  useEffect(() => {
    const hash = window.location.hash;
    let token = window.localStorage.getItem('token');

    if (!token && hash) {
      token = hash.substring(1).split('&').find(elem => elem.startsWith('access_token')).split('=')[1];
      window.location.hash = '';
      window.localStorage.setItem('token', token);
    }

    setToken(token);
  }, []);

  useEffect(() => {
    if (token) {
      const fetchCurrentSong = () => {
        axios.get('https://api.spotify.com/v1/me/player/currently-playing', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }).then(response => {
          if (response.data && response.data.item) {
            setSong(response.data.item);
            console.log(response.data.item.album.id);
            fetchGenreSeeds(response.data.item.album.id); // Fetch genre from the album of the current song
          } else {
            setSong(null); // No song is currently playing
            setGenreSeeds([]); // Clear genre seeds
          }
        }).catch(error => {
          console.error('Error fetching currently playing song:', error);
          setSong(null);
          setGenreSeeds([]); // Clear genre seeds on error
        });
      };

      // Initial fetch
      fetchCurrentSong();

      // Set up polling
      const intervalId = setInterval(fetchCurrentSong, POLLING_INTERVAL);

      // Clear interval on component unmount
      return () => clearInterval(intervalId);
    }
  }, [token]);

  const fetchGenreSeeds = (albumId) => {
    axios.get(`https://api.spotify.com/v1/albums/${albumId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).then(response => {
      console.log(response.data)
      if (response.data && response.data.genres) {
        setGenreSeeds(response.data.genres); // Set genre seeds in state
      } else {
        setGenreSeeds([]); // Clear genre seeds if not found
      }
    }).catch(error => {
      console.error('Error fetching genre seeds:', error);
      setGenreSeeds([]); // Clear genre seeds on error
    });
  };

  const logout = () => {
    setToken('');
    window.localStorage.removeItem('token');
  };

//   return (
//     <div className="App">
//       <header className="App-header">
//         {!token ? (
//           <a
//             href={`${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}&scope=user-read-playback-state`}
//           >
//             Login to Spotify
//           </a>
//         ) : (
//           <div className="container"                
//             style={{
//               textAlign: "center"
//           }}>
//             <button onClick={logout}>Logout</button>
//             {song ? (
//               <div>
//                 <h1>Now Playing</h1>
//                 <img src={song.album.images[0].url} alt={song.name} style={{ width: 400 }} />
//                 <h2>{song.name}</h2>
//                 <h3>{song.artists[0].name}</h3>
//                 <p>GENRES: {song.artists[0].genres}</p>

//               </div>
//             ) : (
//               <p>No song is currently playing</p>
//             )}
//           </div>
//         )}
//       </header>
//     </div>
//   );
// }

return (
  <div className="App">
    <header className="App-header">
      {!token ? (
        <a
          href={`${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}&scope=user-read-playback-state`}
        >
          Login to Spotify
        </a>
      ) : (
        <div className="container"                
          style={{
            textAlign: "center"
        }}>
          <button onClick={logout}>Logout</button>
          {song ? (
            <div>
              <h1>Now Playing</h1>
              <img src={song.album.images[0].url} alt={song.name} style={{ width: 200 }} />
              <h2>{song.name}</h2>
              <p>{song.artists[0].name}</p>
              {genreSeeds.length > 0 ? (
                <div>
                  <h3>Genre Seeds:</h3>
                  <ul>
                    {genreSeeds.map((genre, index) => (
                      <li key={index}>{genre}</li>
                    ))}
                  </ul>
                </div>
              ) : (
                <p>No genre seeds found for the current song</p>
              )}
            </div>
          ) : (
            <p>No song is currently playing</p>
          )}
        </div>
      )}
    </header>
  </div>
);
}

export default App;