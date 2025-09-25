import streamlit as st
import json
import os
import random

# Use st.cache_data to cache the data loading function.
@st.cache_data
def load_all_data(file_name):
    """
    Loads all flashcard data from a single JSON file.
    """
    if not os.path.exists(file_name):
        st.error(f"File not found: {file_name}. Please make sure 'data.json' exists.")
        return []

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Check if the loaded data is a list as expected
            if isinstance(data, list):
                return data
            else:
                st.error("JSON file is not in the expected list format.")
                return []
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {file_name}. The file may be empty or malformed.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []

st.set_page_config(page_title="Flashcard App", layout="centered")

st.title("English-Chinese Flashcards")
st.markdown("---")

# Use a radio button to select between vocabulary and sentence flashcards.
card_type = st.radio(
    "Select Card Type:",
    ("Vocabulary", "Sentences")
)

# Load all data from the single 'data.json' file
all_data = load_all_data("data.json")

# Filter the data based on the selected card type
if all_data:
    # Determine the expected 'type' value to match in the JSON data.
    # We account for the singular vs. plural inconsistency between the radio button and data.
    expected_type = card_type.lower()
    if expected_type == "sentences":
        expected_type = "sentence"
        
    filtered_data = [card for card in all_data if card.get('type') == expected_type]

    if filtered_data:
        st.success(f"Successfully loaded {len(filtered_data)} {card_type} flashcards!")

        # Use session state to manage the current card index
        if 'card_index' not in st.session_state or 'card_type' not in st.session_state or st.session_state.card_type != card_type:
            st.session_state.card_index = 0
            st.session_state.card_type = card_type
            st.session_state.show_translation = False
        
        # Get the current flashcard from the filtered data
        current_card = filtered_data[st.session_state.card_index]

        # Display the Chinese side of the flashcard first
        st.header(f"Card {st.session_state.card_index + 1}/{len(filtered_data)}")
        st.markdown(f"**Chinese Translation:**")
        st.info(current_card['chinese'])

        # Use columns to place the buttons side-by-side below the Chinese translation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Next Card"):
                st.session_state.card_index = (st.session_state.card_index + 1) % len(filtered_data)
                st.session_state.show_translation = False
                st.rerun()

        with col2:
            if st.button("Shuffle Cards"):
                random.shuffle(filtered_data)
                st.session_state.card_index = 0
                st.session_state.show_translation = False
                st.rerun()

        # Button to toggle the English translation
        if st.button("Show/Hide English"):
            st.session_state.show_translation = not st.session_state.show_translation

        # Display the English side if the toggle is on
        if st.session_state.show_translation:
            st.markdown(f"**English:**")
            st.success(current_card['english'])
    else:
        st.info(f"No {card_type} flashcards found in the data.")
else:
    st.info("No flashcard data to display. Please check your 'data.json' file.")
