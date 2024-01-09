import time
from IPython.display import display
import ipywidgets as widgets




def search_song(df, column_title, column_artist, limit=1):
    '''
    Takes a dataframe with two columns: track_name and artists
    Returns a DataFrame with three columns: track_name, artists, id
    '''
    # Initialize Spotipy
    client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame(columns=['track_name', 'artists', 'id'])
    
    # Iterate through each row of the input DataFrame
    for index, row in df.iterrows():
        # Search for the track using the title and artists from the DataFrame
        track_name = row[column_title]
        artists = row[column_artist]
        query = f'track:"{track_name}" artist:"{artists}"'
        results = sp.search(q=query, limit=limit)
        
        # Extract the track ID(s) from the search results
        track_ids = [item['id'] for item in results['tracks']['items']]
        
        # If there are track IDs, append them to the result DataFrame
        if track_ids:
            for track_id in track_ids:
                result_df = pd.concat([result_df, pd.DataFrame({'track_name': [track_name], 'artists': [artists], 'id': [track_id]})], ignore_index=True)
    
    return result_df


def get_audio_features(list_of_song_ids):
    chunk_size = 50
    audio_features_list = []  # List to store audio features
    
    progress_bar = widgets.IntProgress(
        min=0, 
        max=len(list_of_song_ids), 
        description='Processing audio features :', 
        bar_style='', 
        style={'bar_color': '#1ED760'})
    
    display(progress_bar)

    for i in range(0, len(list_of_song_ids), chunk_size):
        chunk = list_of_song_ids[i:i + chunk_size]

        try:
            # Retrieve audio features for the chunk of song IDs
            audio_features = sp.audio_features(chunk)
            audio_features_list.extend(audio_features)
        except Exception as e:
            print("Error retrieving audio features:", e)

        time.sleep(20)  # Sleep to avoid rate limiting
        progress_bar.value = i + chunk_size  # Update progress bar value

    # Create a DataFrame from the list of audio features
    df = pd.DataFrame(audio_features_list)

    return df



    def add_audio_features(df, audio_features_df):
        # Merge the dataframes on the 'id' column
        merged_df = pd.merge(df, audio_features_df, left_on='id', right_on='id', how='left')
        return merged_df