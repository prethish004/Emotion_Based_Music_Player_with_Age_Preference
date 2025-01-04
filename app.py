# # # # # import streamlit as st
# # # # # import tensorflow as tf
# # # # # from tensorflow.keras.preprocessing import image
# # # # # import numpy as np
# # # # # import requests
# # # # # import random
# # # # # import webbrowser
# # # # # import os
# # # # # from PIL import Image

# # # # # # Load the pre-trained model
# # # # # model = tf.keras.models.load_model("emotion_model.h5")

# # # # # # Emotion-to-Music Mapping
# # # # # emotion_music_mapping = {
# # # # #     "angry": ["rock", "metal", "energetic"],
# # # # #     "disgust": ["calm", "relaxing", "ambient"],
# # # # #     "fear": ["uplifting", "motivational", "soft"],
# # # # #     "happy": ["pop", "dance", "party"],
# # # # #     "neutral": ["acoustic", "lofi", "chill"],
# # # # #     "sad": ["sad", "melancholic", "slow"],
# # # # #     "surprise": ["exciting", "upbeat", "electronic"]
# # # # # }

# # # # # # YouTube Search API Function
# # # # # def get_youtube_video(language, emotion_category):
# # # # #     api_key = "AIzaSyAYmxZ0Wg5ZsTTUJ3cijr_IrzjnJSQcy8U"
# # # # #     query = f"{language} {random.choice(emotion_music_mapping[emotion_category])} music"
# # # # #     url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&type=video&key={api_key}"
# # # # #     response = requests.get(url).json()
    
# # # # #     # Extract video link
# # # # #     if "items" in response and len(response["items"]) > 0:
# # # # #         video_id = response["items"][0]["id"]["videoId"]
# # # # #         return f"https://www.youtube.com/watch?v={video_id}"
# # # # #     else:
# # # # #         return None

# # # # # # Preprocess Uploaded Image
# # # # # def preprocess_image(img_path):
# # # # #     # Load image using PIL and convert to grayscale
# # # # #     img = Image.open(img_path).convert("L")  # Convert to grayscale
# # # # #     img = img.resize((224, 224))  # Resize to target dimensions
# # # # #     img_array = np.array(img) / 255.0  # Normalize pixel values
# # # # #     img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension for grayscale
# # # # #     img_array = np.expand_dims(img_array, axis=0)   # Add batch dimension
# # # # #     return img_array
# # # # # # Predict Emotion
# # # # # def predict_emotion(img_path):
# # # # #     img_array = preprocess_image(img_path)
# # # # #     print(f"Input shape for model: {img_array.shape}")  # Debugging
# # # # #     predictions = model.predict(img_array)
# # # # #     # Handle predictions...
# # # # #     return predictions


# # # # # # Streamlit Interface
# # # # # st.title("Emotion-Based Music Recommendation")
# # # # # st.write("Upload an image or capture one to detect your emotion and play music based on your preferred language and detected emotion.")

# # # # # # File Upload or Camera Input
# # # # # uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# # # # # if st.button("Take a Photo"):
# # # # #     uploaded_file = st.camera_input("Take a photo")

# # # # # # Language Input
# # # # # language = st.text_input("Enter your preferred language for music")

# # # # # # Process Image and Recommend Music
# # # # # if uploaded_file and language:
# # # # #     # Save the uploaded file locally
# # # # #     img_path = "temp_image.jpg"
# # # # #     with open(img_path, "wb") as f:
# # # # #         f.write(uploaded_file.getbuffer())

# # # # #     # Predict Emotion
# # # # #     st.image(Image.open(img_path), caption="Uploaded Image", use_column_width=True)
# # # # #     emotion = predict_emotion(img_path)
# # # # #     st.write(f"Detected Emotion: **{emotion.capitalize()}**")

# # # # #     # Recommend Music
# # # # #     st.write("Searching for music...")
# # # # #     video_url = get_youtube_video(language, emotion)
# # # # #     if video_url:
# # # # #         st.write("Playing music based on your emotion and language...")
# # # # #         webbrowser.open(video_url)
# # # # #         st.video(video_url)
# # # # #     else:
# # # # #         st.error("No music found. Please try again.")

# # # # #     # Cleanup
# # # # #     os.remove(img_path)
# # # # # else:
# # # # #     st.info("Please upload an image and enter your preferred language.")


# # # # import streamlit as st
# # # # import tensorflow as tf
# # # # from PIL import Image
# # # # import numpy as np
# # # # from googleapiclient.discovery import build

# # # # # Load the emotion detection model
# # # # model = tf.keras.models.load_model("emotion_model.h5")

# # # # # Preprocess the image for the emotion model
# # # # def preprocess_image(image):
# # # #     img = Image.fromarray(image)
# # # #     img = img.convert('L')  # Convert to grayscale
# # # #     img = img.resize((64, 64))  # Resize to match model's input size
# # # #     img_rgb = Image.new('RGB', img.size)  # Create an RGB image
# # # #     img_rgb.paste(img)  # Paste grayscale image onto all three channels
# # # #     img_arr = np.array(img_rgb).reshape(1, 64, 64, 3) / 255.0  # Normalize and reshape
# # # #     return img_arr

# # # # # Fetch songs dynamically using YouTube API
# # # # def fetch_songs_from_youtube(emotion, languages):
# # # #     api_key = 'AIzaSyAYmxZ0Wg5ZsTTUJ3cijr_IrzjnJSQcy8U'  # Replace with your actual API key
# # # #     youtube = build('youtube', 'v3', developerKey=api_key)

# # # #     songs = []
# # # #     for language in languages:
# # # #         search_query = f"{emotion} songs in {language}"
# # # #         request = youtube.search().list(
# # # #             q=search_query,
# # # #             part="snippet",
# # # #             maxResults=5,  # Fetch fewer results per language to balance load
# # # #             type="video"
# # # #         )
# # # #         response = request.execute()

# # # #         for item in response['items']:
# # # #             title = item['snippet']['title']
# # # #             video_id = item['id']['videoId']
# # # #             video_url = f"https://www.youtube.com/watch?v={video_id}"
# # # #             songs.append({"title": title, "url": video_url, "language": language})

# # # #     return songs

# # # # # Initialize state variables
# # # # if "process_completed" not in st.session_state:
# # # #     st.session_state["process_completed"] = False

# # # # # Step 1: Input Image and Language
# # # # st.header("Emotion Detection and Multi-Language Music Recommendation")

# # # # # Allow user to choose between uploading an image or using the camera
# # # # upload_choice = st.radio(
# # # #     "Select an option to upload an image:",
# # # #     ("Use Camera", "Upload Photo")
# # # # )

# # # # placeholder = st.empty()
# # # # if not st.session_state["process_completed"]:
# # # #     uploaded_image = None

# # # #     if upload_choice == "Use Camera":
# # # #         uploaded_image = placeholder.camera_input("Capture an image for emotion detection")
# # # #     elif upload_choice == "Upload Photo":
# # # #         uploaded_image = placeholder.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# # # #     # Language selection
# # # #     languages = st.multiselect(
# # # #         "Select your preferred languages (you can choose multiple):",
# # # #         ["English", "Hindi", "Spanish", "French", "German", "Chinese", "Arabic", "Japanese", "Korean"]
# # # #     )

# # # #     if uploaded_image and languages:
# # # #         try:
# # # #             # Convert the captured/uploaded image to a format that can be processed
# # # #             image = np.array(Image.open(uploaded_image))

# # # #             # Preprocess and predict the emotion from the image
# # # #             img_arr = preprocess_image(image)
# # # #             prediction = model.predict(img_arr)
# # # #             emotions = ["angry", "contempt", "disgust", "fear", "happiness", "neutrality", "sadness", "surprise"]
# # # #             detected_emotion = emotions[np.argmax(prediction)]

# # # #             st.success(f"Detected Emotion: {detected_emotion}")
# # # #             st.session_state["emotion_detected"] = detected_emotion
# # # #             st.session_state["languages"] = languages
# # # #             st.session_state["process_completed"] = True
# # # #         except Exception as e:
# # # #             st.error(f"Error processing the image: {e}")

# # # # # Step 2: Recommend Songs
# # # # if st.session_state.get("emotion_detected"):
# # # #     st.subheader(f"Emotion Detected: {st.session_state['emotion_detected']}")
# # # #     st.write(f"Preferred Languages: {', '.join(st.session_state['languages'])}")

# # # #     if "songs" not in st.session_state:
# # # #         songs = fetch_songs_from_youtube(
# # # #             st.session_state["emotion_detected"],
# # # #             st.session_state["languages"]
# # # #         )
# # # #         st.session_state["songs"] = songs

# # # #     st.subheader("Recommended Songs:")
# # # #     if not st.session_state["songs"]:
# # # #         st.info("No songs found for the detected emotion in the selected languages.")
# # # #     else:
# # # #         recommendations = [
# # # #             f"<b>{song['language']}:</b> <a href='{song['url']}' target='_blank'>{song['title']}</a>"
# # # #             for song in st.session_state["songs"]
# # # #         ]
# # # #         st.markdown("<br>".join(recommendations), unsafe_allow_html=True)

# # # # # Step 3: Retake or Upload a New Image
# # # # if st.button("Retake or Upload New Image"):
# # # #     st.session_state["process_completed"] = False
# # # #     st.session_state.pop("emotion_detected", None)
# # # #     st.session_state.pop("languages", None)
# # # #     st.session_state.pop("songs", None)
# # # #     placeholder.empty()


# # # import streamlit as st
# # # import tensorflow as tf
# # # from PIL import Image
# # # import numpy as np
# # # from googleapiclient.discovery import build

# # # # Load the emotion detection model
# # # model = tf.keras.models.load_model("emotion_model.h5")

# # # # Preprocess the image for the emotion model
# # # def preprocess_image(image):
# # #     img = Image.fromarray(image)
# # #     img = img.convert('L')  # Convert to grayscale
# # #     img = img.resize((64, 64))  # Resize to match model's input size
# # #     img_rgb = Image.new('RGB', img.size)  # Create an RGB image
# # #     img_rgb.paste(img)  # Paste grayscale image onto all three channels
# # #     img_arr = np.array(img_rgb).reshape(1, 64, 64, 3) / 255.0  # Normalize and reshape
# # #     return img_arr

# # # # Fetch songs dynamically using YouTube API
# # # def fetch_songs_from_youtube(emotion, languages):
# # #     api_key = 'AIzaSyD4-X0747wo4mXqJrxHwWb7mo1Yq3JhUhE'  # Replace with your actual API key
# # #     youtube = build('youtube', 'v3', developerKey=api_key)

# # #     search_query = f"{emotion} songs in {', '.join(languages)}"
# # #     request = youtube.search().list(
# # #         q=search_query,
# # #         part="snippet",
# # #         maxResults=5,
# # #         type="video"
# # #     )
# # #     response = request.execute()

# # #     songs = []
# # #     for item in response['items']:
# # #         title = item['snippet']['title']
# # #         video_id = item['id']['videoId']
# # #         video_url = f"https://www.youtube.com/watch?v={video_id}"
# # #         songs.append({"title": title, "video_id": video_id})
    
# # #     return songs

# # # # Initialize state variables
# # # if "process_completed" not in st.session_state:
# # #     st.session_state["process_completed"] = False

# # # st.header("Emotion Detection and Music Recommendation")

# # # # Step 1: Image Input and Language Selection
# # # upload_choice = st.radio(
# # #     "Select an option to upload an image:",
# # #     ("Use Camera", "Upload Photo")
# # # )

# # # placeholder = st.empty()
# # # if not st.session_state["process_completed"]:
# # #     uploaded_image = None

# # #     if upload_choice == "Use Camera":
# # #         uploaded_image = placeholder.camera_input("Capture an image for emotion detection")
# # #     elif upload_choice == "Upload Photo":
# # #         uploaded_image = placeholder.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# # #     languages_input = st.text_input(
# # #         "Enter preferred languages (comma-separated):",
# # #         placeholder="e.g., English, Hindi, Spanish"
# # #     )
# # #     languages = [lang.strip() for lang in languages_input.split(",") if lang.strip()]

# # #     if uploaded_image and languages:
# # #         try:
# # #             # Convert the captured/uploaded image to a format that can be processed
# # #             image = np.array(Image.open(uploaded_image))

# # #             # Preprocess and predict the emotion from the image
# # #             img_arr = preprocess_image(image)
# # #             prediction = model.predict(img_arr)
# # #             emotions = ["angry", "contempt", "disgust", "fear", "happiness", "neutrality", "sadness", "surprise"]
# # #             detected_emotion = emotions[np.argmax(prediction)]

# # #             st.success(f"Detected Emotion: {detected_emotion}")
# # #             st.session_state["emotion_detected"] = detected_emotion
# # #             st.session_state["languages"] = languages
# # #             st.session_state["process_completed"] = True
# # #         except Exception as e:
# # #             st.error(f"Error processing the image: {e}")

# # # # Step 2: Recommend Songs
# # # if st.session_state.get("emotion_detected"):
# # #     st.subheader(f"Emotion Detected: {st.session_state['emotion_detected']}")
# # #     st.write(f"Preferred Languages: {', '.join(st.session_state['languages'])}")

# # #     if "songs" not in st.session_state:
# # #         songs = fetch_songs_from_youtube(
# # #             st.session_state["emotion_detected"],
# # #             st.session_state["languages"]
# # #         )
# # #         st.session_state["songs"] = songs

# # #     st.subheader("Recommended Songs:")
# # #     selected_song = None
# # #     for i, song in enumerate(st.session_state["songs"]):
# # #         if st.button(f"Play: {song['title']}", key=f"play_{i}"):
# # #             selected_song = song

# # #     # Display the YouTube video player if a song is selected
# # #     if selected_song:
# # #         st.video(f"https://www.youtube.com/embed/{selected_song['video_id']}")

# # # # Step 3: Retake or Upload a New Image
# # # if st.button("Retake or Upload New Image"):
# # #     st.session_state["process_completed"] = False
# # #     st.session_state.pop("emotion_detected", None)
# # #     st.session_state.pop("languages", None)
# # #     st.session_state.pop("songs", None)
# # #     placeholder.empty()

# import streamlit as st
# import tensorflow as tf
# from PIL import Image
# import numpy as np
# from googleapiclient.discovery import build
# from spellchecker import SpellChecker
# import yt_dlp

# # Load the emotion detection model
# model = tf.keras.models.load_model("emotion_model.h5")

# # Preprocess the image for the emotion model
# def preprocess_image(image):
#     img = Image.fromarray(image)
#     img = img.convert('L')  # Convert to grayscale
#     img = img.resize((64, 64))  # Resize to match model's input size
#     img_rgb = Image.new('RGB', img.size)  # Create an RGB image
#     img_rgb.paste(img)  # Paste grayscale image onto all three channels
#     img_arr = np.array(img_rgb).reshape(1, 64, 64, 3) / 255.0  # Normalize and reshape
#     return img_arr

# # Fetch trending songs dynamically using YouTube API
# def fetch_trending_songs(emotion, languages):
#     api_key = 'AIzaSyD4-X0747wo4mXqJrxHwWb7mo1Yq3JhUhE'  # Replace with your actual API key
#     youtube = build('youtube', 'v3', developerKey=api_key)

#     songs = []
#     for lang in languages:
#         search_query = f"trending {emotion} songs in {lang}"
#         request = youtube.search().list(
#             q=search_query,
#             part="snippet",
#             maxResults=5,
#             type="video"
#         )
#         response = request.execute()
#         for item in response['items']:
#             title = item['snippet']['title']
#             video_id = item['id']['videoId']
#             songs.append({"title": title, "video_id": video_id})

#     return songs

# # Download YouTube audio URL using yt-dlp
# def get_audio_url(video_id):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'quiet': True,
#         'noplaylist': True,
#         'extract_flat': True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
#         for format in info['formats']:
#             if format.get('acodec') and format['acodec'] != 'none':
#                 return format['url']
#     return None

# # Initialize state variables
# if "process_completed" not in st.session_state:
#     st.session_state["process_completed"] = False

# st.header("Emotion-Based Music Player")
# spell = SpellChecker()

# # Step 1: Image and Language Input
# upload_choice = st.radio("Select an option to upload an image:", ("Use Camera", "Upload Photo"))

# placeholder = st.empty()
# uploaded_image = None
# if upload_choice == "Use Camera":
#     uploaded_image = placeholder.camera_input("Capture an image for emotion detection")
# elif upload_choice == "Upload Photo":
#     uploaded_image = placeholder.file_uploader("Upload an image", type=["jpg", "jpeg", "png","webp"])

# # Input for languages with spell-checking
# languages_input = st.text_input("Enter languages (comma-separated):", value="")
# corrected_languages = [spell.correction(lang.strip()) for lang in languages_input.split(",")]

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
#         st.session_state["process_completed"] = True
#     except Exception as e:
#         st.error(f"Error processing the image: {e}")

# # Step 2: Recommend and Play Songs
# if st.session_state.get("emotion_detected"):
#     st.subheader(f"Emotion Detected: {st.session_state['emotion_detected']}")
#     st.write(f"Preferred Languages: {', '.join(st.session_state['languages'])}")

#     if "songs" not in st.session_state:
#         songs = fetch_trending_songs(
#             st.session_state["emotion_detected"],
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
#             st.warning("Audio not available for this song.")

# # Step 3: Retake or Upload New Image
# if st.button("Retake or Upload New Image"):
#     st.session_state["process_completed"] = False
#     st.session_state.pop("emotion_detected", None)
#     st.session_state.pop("languages", None)
#     st.session_state.pop("songs", None)
#     placeholder.empty()

import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from googleapiclient.discovery import build
from spellchecker import SpellChecker
import yt_dlp
import isodate  # For parsing ISO 8601 duration from YouTube API

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

# Emotion-to-Music Mapping
emotion_music_mapping = {
    "angry": ["rock", "metal", "energetic"],
    "disgust": ["calm", "relaxing", "ambient"],
    "fear": ["uplifting", "motivational", "soft"],
    "happiness": ["pop", "dance", "party"],
    "neutrality": ["acoustic", "lofi", "chill"],
    "sadness": ["sad", "melancholic", "slow"],
    "surprise": ["exciting", "upbeat", "electronic"]
}

# Fetch the audio URL using yt_dlp
def get_audio_url(video_id):
    ydl_opts = {
        'format': 'bestaudio/best',  # Fetch best available audio
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            
            # Check video duration
            duration = info.get("duration", 0)
            if duration>100:  # Ensure duration is between 2 and 10 minutes
                for format in info.get('formats', []):
                    if format.get('acodec') and format['acodec'] != 'none':
                        return format['url']
            else:
                return None
        except Exception as e:
            st.error(f"Error fetching audio: {e}")
            return None

# Fetch trending songs dynamically using YouTube API
def fetch_trending_songs(emotion, age, languages):
    api_key = 'AIzaSyD4-X0747wo4mXqJrxHwWb7mo1Yq3JhUhE'  # Replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    genres = emotion_music_mapping.get(emotion, ["popular"])
    songs = []
    
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
                maxResults=5,
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
                if duration>100:  # Filter songs between 2 and 10 minutes
                    title = item['snippet']['title']
                    songs.append({"title": title, "video_id": video_id})

    return songs[:6]

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
        songs = fetch_trending_songs(
            st.session_state["emotion_detected"],
            st.session_state["age"],
            st.session_state["languages"]
        )
        st.session_state["songs"] = songs

    st.subheader("Trending Songs:")
    for song in st.session_state["songs"]:
        st.write(f"**{song['title']}**")
        audio_url = get_audio_url(song['video_id'])
        if audio_url:
            st.audio(audio_url, format="audio/mp4")
        else:
            st.warning("Audio not available or duration is less than 2 minutes.")

if st.button("Fetch others Songs"):
    # Clear session state variables
    st.session_state["process_completed"] = False
    st.session_state.pop("emotion_detected", None)
    st.session_state.pop("languages", None)
    st.session_state.pop("age", )
    st.session_state.pop("songs", None)
    
    # Clear the image placeholder
    placeholder.empty()

    # Refresh the page
    st.experimental_rerun()