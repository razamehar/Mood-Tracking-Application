import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def get_moods():
      
      # Initialize lists for storing timestamps and sentiments
      timestamps, sentiments = [], []
      
      # Connect to the SQLite database
      conn = sqlite3.connect('sentiments.db')
      c = conn.cursor()
      
      # Execute a query to select all rows from the 'sentiments' table
      c.execute('SELECT * FROM sentiments WHERE user_id = ?', (st.session_state['user_id'],))
      
      # Fetch all results
      rows = c.fetchall()
      
      for row in rows:
            timestamps.append(row[2])
            sentiments.append(row[3].lower())
      
      conn.close()
      
      return sentiments, timestamps

def display_pie(sentiments, timestamps, mood_palette, font_size):
    st.header('Overall _:blue[Mood Distribution]_')

    if not sentiments:
        st.write("No mood data available.")
        return
          
    df = pd.DataFrame({'Date-Time': timestamps, 'Mood': sentiments})
    df['Date-Time'] = pd.to_datetime(df['Date-Time'], errors='coerce')
    df['Mood'] = df['Mood'].astype('category')
    mood_distribution = df['Mood'].value_counts()    
      
    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size': font_size})
    plt.pie(mood_distribution, labels=mood_distribution.index, autopct='%1.1f%%', startangle=90,
                colors=[mood_palette[mood] for mood in mood_distribution.index]) 
    plt.axis('equal') 
    st.pyplot(fig)

def display_bar(sentiments, timestamps, mood_palette, font_size):
    st.header('_:blue[Mood Distribution]_ over Time')

    if not sentiments:
        st.write("No mood data available.")
        return
          
    df = pd.DataFrame({'Date-Time': timestamps, 'Mood': sentiments})
    df['Date-Time'] = pd.to_datetime(df['Date-Time'], errors='coerce')
    df['Mood'] = df['Mood'].astype('category')
    df['Date'] = df['Date-Time'].dt.date 
    category_counts = df.groupby(['Date', 'Mood']).size().reset_index(name='Count')
      
    plt.rcParams.update({'font.size': font_size})

    sns.barplot(x='Date', y='Count', hue='Mood', data=category_counts, palette=mood_palette)
    plt.xticks(rotation=45)
    plt.xlabel('Date', fontsize=font_size)
    plt.ylabel('Count', fontsize=font_size)
    plt.legend(title='Mood', fontsize=font_size, title_fontsize=font_size)
    ax = plt.gca()  # Get current axis
    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(plt.gcf())

def main():
      st.header('_:blue[Mood Tracking]_ Application')
      sentiments, timestamps = get_moods()
      mood_palette = {'happy': 'blue', 'not happy': 'red', 'neutral': 'green'}
      font_size = 14
      
      response = st.radio('Choose', options=['Overall Mood Distribution', 'Mood Distribution over Time'], key=12345, horizontal=True)
      
      if response == 'Overall Mood Distribution':
            display_pie(sentiments, timestamps, mood_palette, font_size)
      else:      
            display_bar(sentiments, timestamps, mood_palette, font_size)

# Call the main function
main()
