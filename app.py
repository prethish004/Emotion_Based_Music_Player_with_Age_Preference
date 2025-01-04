
# import streamlit as st
# import tensorflow as tf
# from PIL import Image
# import numpy as np
# from googleapiclient.discovery import build
# from spellchecker import SpellChecker
# import yt_dlp
# import isodate  # For parsing ISO 8601 duration from YouTube API

# # Load the emotion detection model
# model = tf.keras.models.load_model("./emotion_model.h5")

# # Preprocess the image for the emotion model
# def preprocess_image(image):
#     img = Image.fromarray(image)
#     img = img.convert('L') 
#     img = img.resize((64, 64))  # Resize to match model's input size
#     img_rgb = Image.new('RGB', img.size)  # Create an RGB image
#     img_rgb.paste(img)  # Paste grayscale image onto all three channels
#     img_arr = np.array(img_rgb).reshape(1, 64, 64, 3) / 255.0  # Normalize and reshape
#     return img_arr

# # Emotion-to-Music Mapping
# emotion_music_mapping = {
#     "angry": ["rock", "metal", "energetic"],
#     "disgust": ["calm", "relaxing", "ambient"],
#     "fear": ["uplifting", "motivational", "soft"],
#     "happiness": ["pop", "dance", "party"],
#     "neutrality": ["acoustic", "lofi", "chill"],
#     "sadness": ["sad", "melancholic", "slow"],
#     "surprise": ["exciting", "upbeat", "electronic"]
# }

# # Fetch the audio URL using yt_dlp
# def get_audio_url(video_id):
#     ydl_opts = {
#         'format': 'bestaudio/best',  # Fetch best available audio
#         'quiet': True,
#         'noplaylist': True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            
#             # Check video duration
#             duration = info.get("duration", 0)
#             if duration>100:  # Ensure duration is between 2 and 10 minutes
#                 for format in info.get('formats', []):
#                     if format.get('acodec') and format['acodec'] != 'none':
#                         return format['url']
#             else:
#                 return None
#         except Exception as e:
#             st.error(f"Error fetching audio: {e}")
#             return None

# # Fetch trending songs dynamically using YouTube API
# def fetch_trending_songs(emotion, age, languages):
#     api_key = 'AIzaSyAYmxZ0Wg5ZsTTUJ3cijr_IrzjnJSQcy8U'  # Replace with your actual API key
#     youtube = build('youtube', 'v3', developerKey=api_key)

#     genres = emotion_music_mapping.get(emotion, ["popular"])
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
#                 maxResults=5,
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
#                 if duration>100:  # Filter songs between 2 and 10 minutes
#                     title = item['snippet']['title']
#                     songs.append({"title": title, "video_id": video_id})

#     return songs[:6]

# # Initialize state variables
# if "process_completed" not in st.session_state:
#     st.session_state["process_completed"] = False

# st.header("Emotion-Based Music Player with Age Preference")
# spell = SpellChecker()

# # Step 1: Age Input
# age = st.number_input("Enter your age:", min_value=1, max_value=100, step=1,value=25)

# # Input for languages with spell-checking
# languages_input = st.text_input("Enter languages (comma-separated):", value="English")
# corrected_languages = [spell.correction(lang.strip()) for lang in languages_input.split(",")]

# # Step 2: Image and Language Input
# upload_choice = st.radio("Select an option to upload an image:", ("Use Camera", "Upload Photo"))

# placeholder = st.empty()
# uploaded_image = None
# if upload_choice == "Use Camera":
#     uploaded_image = placeholder.camera_input("Capture an image for emotion detection")
# elif upload_choice == "Upload Photo":
#     uploaded_image = placeholder.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "avif"])

# if uploaded_image and corrected_languages:
#     try:
#         # Convert the uploaded/captured image to a format that can be processed
#         image = np.array(Image.open(uploaded_image))

#         # Preprocess and predict the emotion from the image
#         img_arr = preprocess_image(image)
#         prediction = model.predict(img_arr)
#         emotions = ["angry", "contempt", "disgust", "fear", "happiness", "neutrality", "sadness", "surprise"]
#         detected_emotion = emotions[np.argmax(prediction)]

#         st.success(f"Detected Emotion: {detected_emotion}")
#         st.session_state["emotion_detected"] = detected_emotion
#         st.session_state["languages"] = corrected_languages
#         st.session_state["age"] = age
#         st.session_state["process_completed"] = True
#     except Exception as e:
#         st.error(f"Error processing the image: {e}")

# # Step 3: Recommend and Play Songs
# if st.session_state.get("emotion_detected"):
#     st.subheader(f"Emotion Detected: {st.session_state['emotion_detected']}")
#     st.write(f"Preferred Languages: {', '.join(st.session_state['languages'])}")
#     st.write(f"User Age: {st.session_state['age']}")

#     if "songs" not in st.session_state:
#         songs = fetch_trending_songs(
#             st.session_state["emotion_detected"],
#             st.session_state["age"],
#             st.session_state["languages"]
#         )
#         st.session_state["songs"] = songs

#     st.subheader("Trending Songs:")
#     for song in st.session_state["songs"]:
#         st.write(f"**{song['title']}**")
#         audio_url = get_audio_url(song['video_id'])
#         if audio_url:
#             st.audio(audio_url, format="audio/mp4")
#         else:
#             st.warning("Audio not available or duration is less than 2 minutes.")

# if st.button("Fetch others Songs"):
#     # Clear session state variables
#     st.session_state["process_completed"] = False
#     st.session_state.pop("emotion_detected", None)
#     st.session_state.pop("languages", None)
#     st.session_state.pop("age", )
#     st.session_state.pop("songs", None)
    
#     # Clear the image placeholder
#     placeholder.empty()

#     # Refresh the page
#     st.experimental_rerun()


import streamlit as st
from hello import fetch_trending_songs
from spellchecker import SpellChecker
import tensorflow as tf
from PIL import Image
import numpy as np
import yt_dlp

# Load the emotion detection model
model = tf.keras.models.load_model("emotion_model.h5")

# Preprocess the image for the emotion model
def preprocess_image(image):
    img = Image.fromarray(image)
    img = img.convert('L') 
    img = img.resize((64, 64))  # Resize to match model's input size
    img_rgb = Image.new('RGB', img.size)  # Create an RGB image
    img_rgb.paste(img)  # Paste grayscale image onto all three channels
    img_arr = np.array(img_rgb).reshape(1, 64, 64, 3) / 255.0  # Normalize and reshape
    return img_arr
def get_audio_url(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,  # Only extract audio
        'outtmpl': 'temp_audio.%(ext)s',  # Temp file name
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        audio_url = info_dict.get('url', None)  # URL of the audio stream
    
    return audio_url

# Initialize state variables
if "process_completed" not in st.session_state:
    st.session_state["process_completed"] = False

st.header("Emotion-Based Music Player with Age Preference")
spell = SpellChecker()

# Step 1: Age Input
age = st.number_input("Enter your age:", min_value=1, max_value=100, step=1, value=25)

# Input for languages with spell-checking
languages_input = st.text_input("Enter languages (comma-separated):", value="English")
corrected_languages = [spell.correction(lang.strip()) for lang in languages_input.split(",")]

# Step 2: Image and Language Input
upload_choice = st.radio("Select an option to upload an image:", ("Use Camera", "Upload Photo"))

placeholder = st.empty()
uploaded_image = None
if upload_choice == "Use Camera":
    uploaded_image = placeholder.camera_input("Capture an image for emotion detection")
elif upload_choice == "Upload Photo":
    uploaded_image = placeholder.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "avif"])

if uploaded_image and corrected_languages:
    try:
        # Convert the uploaded/captured image to a format that can be processed
        image = np.array(Image.open(uploaded_image))

        # Preprocess and predict the emotion from the image
        img_arr = preprocess_image(image)
        prediction = model.predict(img_arr)
        emotions = ["angry", "contempt", "disgust", "fear", "happiness", "neutrality", "sadness", "surprise"]
        detected_emotion = emotions[np.argmax(prediction)]

        st.success(f"Detected Emotion: {detected_emotion}")
        st.session_state["emotion_detected"] = detected_emotion
        st.session_state["languages"] = corrected_languages
        st.session_state["age"] = age
        st.session_state["process_completed"] = True
    except Exception as e:
        st.error(f"Error processing the image: {e}")

# Step 3: Recommend and Play Songs
if st.session_state.get("emotion_detected"):
    st.subheader(f"Emotion Detected: {st.session_state['emotion_detected']}")
    st.write(f"Preferred Languages: {', '.join(st.session_state['languages'])}")
    st.write(f"User Age: {st.session_state['age']}")

    if "songs" not in st.session_state:
        # Fetch trending songs based on detected emotion and user preferences
        songs = fetch_trending_songs(
            st.session_state["emotion_detected"],
            st.session_state["age"],
            st.session_state["languages"],
            api_key='AIzaSyAYmxZ0Wg5ZsTTUJ3cijr_IrzjnJSQcy8U'  # Replace with your actual API key
        )
        st.session_state["songs"] = songs

    st.subheader("Trending Songs:")
    for song in st.session_state["songs"]:
        st.write(f"**{song['title']}**")

        # Get audio URL and play the song
        audio_url = get_audio_url(song['video_id'])
        if audio_url:
            st.audio(audio_url, format="audio/mp4")
        else:
            st.warning("Audio not available or duration is less than 2 minutes.")
if st.button("Show other songs"):
        st.experimental_rerun()
