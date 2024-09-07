import streamlit as st
from textblob import TextBlob
import sqlite3
from datetime import datetime
import time
from streamlit_mic_recorder import speech_to_text

# Get sentiment out of the text and classify as Happy, Not Happy or Neutral.
def get_sentiment(text):

  # Create a TextBlob object.
  blob = TextBlob(text)

  # Get the sentiment
  polarity = blob.sentiment.polarity

  # Classify the sentiment.
  if polarity > 0:
    sentiment = 'Happy'
  elif polarity < 0:
    sentiment = 'Not happy'
  else:
    sentiment = 'Neutral'

  return sentiment

# Allow the user to record audio.
def get_audio():
    st.write("Record your voice, and play the recorded audio:")
    
    text = speech_to_text(
    language='en',
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    callback=None,
    args=(),
    kwargs={},
    key=None)

    if text:
        st.write('You said:')
        st.write(text)

    return text 

def record_voicenote():
    text = get_audio()

    if text:
        # Reserve a spot in the UI
        status_text = st.empty()

        # Update the status text to show "Processing..."
        with st.spinner('Processing...'):
            sentiment = get_sentiment(text)
            save_sentiment(sentiment)
            time.sleep(1)
            st.success("Processing completed.")
        
    else:
        st.write("No audio recorded. Please try again.")

# Initialize the database where labels and timestamps will be saved
def initialize_db():
    conn = sqlite3.connect('sentiments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sentiments (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id TEXT NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 sentiment TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def save_sentiment(sentiment):
    conn = sqlite3.connect('sentiments.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO sentiments (user_id, timestamp, sentiment) VALUES (?, ?, ?)', (st.session_state['user_id'], timestamp, sentiment))
    conn.commit()
    conn.close()

def main():
    st.title('_:blue[Mood Tracking]_ Application')
    
    if 'db_initialized' not in st.session_state:
        initialize_db()
        st.session_state.db_initialized = True

    record_voicenote()

if __name__ == "__main__":
    main()
