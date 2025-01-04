import isodate
from googleapiclient.discovery import build

# Emotion-to-Music Mapping
emotion_music_mapping = {
    "angry": ["rock", "metal", "energetic", "animated movie"],
    "disgust": ["calm", "relaxing", "ambient", "animated movie"],
    "fear": ["uplifting", "motivational", "soft", "animated movie"],
    "happiness": ["pop", "dance", "party", "animated movie"],
    "neutrality": ["acoustic", "lofi", "chill", "animated movie"],
    "sadness": ["sad", "melancholic", "slow", "animated movie"],
    "surprise": ["exciting", "upbeat", "electronic", "animated movie"]
}

# def fetch_trending_songs(emotion, age, languages, api_key):
#     youtube = build('youtube', 'v3', developerKey=api_key)

#     genres = emotion_music_mapping.get(emotion, ["Trending"])
#     songs = []
    
#     for lang in languages:
#         for genre in genres:
#             if age <= 18:
#                 search_query = f"latest {genre} songs in {lang} for teenagers"
#             elif age <= 35:
#                 search_query = f"top trending {genre} songs in {lang}"
#             else:
#                 search_query = f"classic {genre} songs in {lang}"

#             request = youtube.search().list(
#                 q=search_query,
#                 part="snippet",
#                 maxResults=6,  # Fetch 6 songs instead of 5
#                 type="video"
#             )
#             response = request.execute()
#             for item in response['items']:
#                 video_id = item['id']['videoId']
#                 video_details = youtube.videos().list(
#                     part="contentDetails",
#                     id=video_id
#                 ).execute()

#                 # Get the duration in seconds
#                 duration = isodate.parse_duration(video_details['items'][0]['contentDetails']['duration']).total_seconds()
#                 if duration <= 6000:  # Filter songs between 2 and 10 minutes
#                     title = item['snippet']['title']
#                     songs.append({"title": title, "video_id": video_id})

#     return songs[:6]  # Return only the top 6 songs

def fetch_trending_songs(emotion, age, languages, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    genres = emotion_music_mapping.get(emotion, ["animated movie"])
    songs = []
    fallback_songs = []  # To store animated movie songs

    for lang in languages:
        for genre in genres:
            if age <= 18:
                search_query = f"latest {genre} songs in {lang} for teenagers"
            elif age <= 35:
                search_query = f"top trending {genre} songs in {lang}"
            else:
                search_query = f"classic {genre} songs in {lang}"

            request = youtube.search().list(
                q=search_query,
                part="snippet",
                maxResults=6,  # Fetch up to 6 songs per query
                type="video"
            )
            response = request.execute()
            for item in response['items']:
                video_id = item['id']['videoId']
                video_details = youtube.videos().list(
                    part="contentDetails",
                    id=video_id
                ).execute()

                # Get the duration in seconds
                duration = isodate.parse_duration(video_details['items'][0]['contentDetails']['duration']).total_seconds()
                if 120 <= duration <= 600:  # Filter songs between 2 and 10 minutes
                    title = item['snippet']['title']
                    song_data = {"title": title, "video_id": video_id}

                    if "animated" in genre.lower() or "movie" in genre.lower():
                        fallback_songs.append(song_data)  # Track animated movie songs

                    songs.append(song_data)

    # Ensure at least one animated movie song is included
    if fallback_songs:
        # Insert one animated movie song at the start, if not already present
        songs = fallback_songs[:1] + [song for song in songs if song not in fallback_songs]

    return songs[:6]  # Return only the top 6 songs

