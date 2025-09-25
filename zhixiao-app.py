import streamlit as st
import json
import random

def load_data():
    """Load flashcard data from the data.json file."""
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)["flashcards"]
        return data
    except FileNotFoundError:
        st.error("The 'data.json' file was not found. Please make sure it's in the same directory.")
        return []

def initialize_session_state():
    """Initialize or reset the session state variables."""
    if 'flashcards' not in st.session_state:
        st.session_state.flashcards = load_data()
    if 'filtered_cards' not in st.session_state:
        st.session_state.filtered_cards = []
    if 'card_index' not in st.session_state:
        st.session_state.card_index = 0
    if 'show_english' not in st.session_state:
        st.session_state.show_english = False
    if 'card_type' not in st.session_state:
        st.session_state.card_type = 'sentence'

def filter_and_shuffle_cards():
    """Filter cards based on type and shuffle them."""
    st.session_state.filtered_cards = [
        card for card in st.session_state.flashcards
        if card['type'] == st.session_state.card_type
    ]
    random.shuffle(st.session_state.filtered_cards)
    st.session_state.card_index = 0
    st.session_state.show_english = False

def show_next_card():
    """Move to the next flashcard in the deck."""
    if st.session_state.filtered_cards:
        st.session_state.card_index = (st.session_state.card_index + 1) % len(st.session_state.filtered_cards)
        st.session_state.show_english = False
        st.experimental_rerun()

def main():
    """Main function to run the Streamlit application."""
    st.title("Speaking Flashcards for Zhixiao")

    # Initialize session state on first run
    initialize_session_state()

    # Filter and shuffle cards on first load or when card type changes
    if 'card_type_changed' not in st.session_state or st.session_state.card_type_changed:
        filter_and_shuffle_cards()
        st.session_state.card_type_changed = False

    # Radio buttons to select flashcard type
    card_type = st.radio(
        "Select card type:",
        ('sentence', 'vocabulary'),
        horizontal=True,
        key='card_type_selector'
    )

    # Check if the card type has changed and update state
    if card_type != st.session_state.card_type:
        st.session_state.card_type = card_type
        st.session_state.card_type_changed = True
        st.experimental_rerun()

    # Display the current card
    if st.session_state.filtered_cards:
        current_card = st.session_state.filtered_cards[st.session_state.card_index]
        
        # Display Chinese text
        st.markdown(f"**<p style='font-size: 24px; text-align: center;'>{current_card['chinese']}</p>**", unsafe_allow_html=True)
        
        # Display English translation with conditional visibility
        if st.session_state.show_english:
            st.markdown(f"<p style='font-size: 20px; text-align: center; color: #6b7280;'>{current_card['english']}</p>", unsafe_allow_html=True)
        
        # Display card counter
        st.markdown(
            f"<p style='text-align: center; color: #9ca3af;'>{st.session_state.card_index + 1}/{len(st.session_state.filtered_cards)}</p>",
            unsafe_allow_html=True
        )

        # Buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Show/Hide English", on_click=lambda: st.session_state.update(show_english=not st.session_state.show_english), use_container_width=True)
        with col2:
            st.button("Next Card", on_click=show_next_card, use_container_width=True)
        with col3:
            st.button("Shuffle Cards", on_click=filter_and_shuffle_cards, use_container_width=True)

    else:
        st.info("No flashcards found for this category.")

if __name__ == "__main__":
    main()
