import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import uuid
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

load_dotenv()
password = os.getenv('password')
st.write(f"Loaded password: {password}")  # Debug line


# Initialize the cookie manager
cookies = EncryptedCookieManager(
    prefix='mood_tracking_app',
    password=password)

if not cookies.ready():
    st.stop()

# Initialize or get user ID from cookies
def initialize_user():
    if 'user_id' not in cookies:
        user_id = str(uuid.uuid4())
        cookies['user_id'] = user_id
        cookies.save()  # Save the cookie
    else:
        user_id = cookies['user_id']
    st.session_state['user_id'] = user_id

st.title('_:blue[Mood Tracking]_ Application')

initialize_user()

st.write("""
**Record your mood on the go with our app!** Just speak your mind, and this app will turn your voice into text, then use our clever AI to figure out if you’re feeling Happy, Not Happy, or Neutral. Don’t worry, we keep it simple—only the mood and timestamp get saved. Track your vibes over time with a cool dashboard that shows your mood distribution and trends. Record as many notes as you want and watch your mood story unfold!

- **To start recording**, click on **"Record"** in the sidebar.
- **To view your mood trends**, check out the **"Dashboard"** option.
""")

st.image('mood_pic.png')
