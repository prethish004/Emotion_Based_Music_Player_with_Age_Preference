
# Emotion-Based Music Recommendation System 🎵

## Overview
This project is an **Emotion-Based Music Recommendation System** that uses user emotions, age, and preferred languages to recommend trending songs. The system ensures at least one animated movie song is included in the recommendations for enhanced diversity and user experience.
Hosted link="https://emotionbasedmusicplayerfromyoutube.streamlit.app/"
![image](https://github.com/user-attachments/assets/789a69e9-f355-48ba-810f-8d6668469760)


## Features
- 🎭 **Emotion-Based Recommendations**: Suggests songs based on user emotions like happiness, sadness, or excitement.
- 🎞️ **Animated Movie Songs**: Guarantees inclusion of at least one animated movie song in recommendations.
- 🌐 **Language and Age Filters**: Tailors recommendations based on user age group and preferred languages.
- 🎵 **Top Trending Songs**: Fetches trending songs from YouTube using the YouTube Data API.
- 🛠️ **Fallback Mechanism**: Ensures high-quality results even when primary criteria are unmet.

## Requirements
- **Python 3.8 or higher**
- Libraries:
  - `google-api-python-client`
  - `isodate`
  - `tensorflow`
- YouTube Data API Key

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/emotion-based-music-recommendation.git
   cd emotion-based-music-recommendation
   ```
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your YouTube Data API key in an environment variable:
   ```bash
   export YOUTUBE_API_KEY=your_api_key_here
   ```

## Project Structure
```
emotion-based-music-recommendation/
├── app.py      # Handles user input for emotion, age, and languages
├── hello.py        # Fetches songs based on the input and YouTube API
├── README.md             # Project documentation
├── requirements.txt      # Required Python libraries
└── example_output/       # Example outputs (optional)
```

## Usage
1. Run the `app.py` script to input your details:
   ```
    python -m streamlit run app.py

    ```
3. The script will call `fetch_songs.py` to recommend songs based on your input.
4. Results will include up to **6 top songs**, with at least one being an animated movie song.

## Example
### Input:
- Emotion: Happy
- Age: 25
- Preferred Languages: English, Hindi

### Output:
1. Song Title: *Let It Go* - Animated Movie Song
2. Song Title: *Uptown Funk* - Trending in English
3. Song Title: *Chaiyya Chaiyya* - Trending in Hindi

## Troubleshooting
### Common Errors
- **IndexError: pop from empty list**  
  Ensure the `fallback_songs` list contains at least one item before accessing it. This is already handled in the latest version.

- **YouTube Data API Quota Exceeded**  
  Reduce the number of API requests or use a different API key with a higher quota.

- **Model Compilation Warning**  
  Ensure the model is compiled after loading:
  ```python
  model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
  ```

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature or fix bug"
   ```
4. Push to your branch and create a pull request.
