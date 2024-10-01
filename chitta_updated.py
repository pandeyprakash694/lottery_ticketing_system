import os
import streamlit as st
import random
import time
import pandas as pd
from io import BytesIO
from gtts import gTTS
import playsound

from chitta import display_ticket_digits_with_ball_animation, prize_images,play_digit_sound

# Map digits to sound file paths
digit_sounds = {
    '0': 'static/sounds/digit_0.mp3',
    '1': 'static/sounds/digit_1.mp3',
    '2': 'static/sounds/digit_2.mp3',
    '3': 'static/sounds/digit_3.mp3',
    '4': 'static/sounds/digit_4.mp3',
    '5': 'static/sounds/digit_5.mp3',
    '6': 'static/sounds/digit_6.mp3',
    '7': 'static/sounds/digit_7.mp3',
    '8': 'static/sounds/digit_8.mp3',
    '9': 'static/sounds/digit_9.mp3'
}

# File path to save the winners list
winners_file_path = "winners.xlsx"

# Define ticket range
ticket_range = list(range(10000, 25001))

# Function to load existing winners from the file if it exists
def load_existing_winners():
    if os.path.exists(winners_file_path):
        return pd.read_excel(winners_file_path)
    else:
        return pd.DataFrame(columns=["Ticket Number", "Prize"])

# Load existing winners
existing_winners = load_existing_winners()

# Filter out tickets that have already been drawn
drawn_tickets = existing_winners['Ticket Number'].tolist()
filtered_ticket_range = [ticket for ticket in ticket_range if ticket not in drawn_tickets]

# Define the number of prizes for each category
prizes = {
    "Electric Jug (Yasuda)": 50,
    "Iron (Yasuda)": 25,
    "Mixture Grinder (Yasuda)": 15,
    "Smart TV (32 inches, Sansui)": 2,
    "Dell Laptop": 1,
    "Washing Machine": 1,
    "iPhone 15": 1,
    "Bike": 1
}


# Adjust remaining prizes based on existing winners
remaining_prizes = prizes.copy()
for prize in existing_winners["Prize"]:
    if prize in remaining_prizes and remaining_prizes[prize] > 0:
        remaining_prizes[prize] -= 1

# Create a shuffled list of remaining prizes
prize_list = []
for prize, quantity in remaining_prizes.items():
    prize_list.extend([prize] * quantity)
random.shuffle(prize_list)  # Shuffle the prize list

# Shuffle the ticket numbers
random.shuffle(filtered_ticket_range)

# Function to draw a ticket
def draw_ticket():
    if not prize_list or not filtered_ticket_range:
        return "No More Prizes Available", None

    # Draw a random ticket and assign a prize
    ticket = filtered_ticket_range.pop(0)
    prize = prize_list.pop(0)  # Get a prize from the shuffled prize list
    return ticket, prize

def save_winners_to_excel(data):
    df = pd.DataFrame(data)

    # Load existing winners
    existing_winners = load_existing_winners()

    # Append new winners to the existing ones, ensuring no duplicates
    updated_winners = pd.concat([existing_winners, df]).drop_duplicates(subset=["Ticket Number"], keep="first")

    # Save the updated winners list back to the Excel file
    with pd.ExcelWriter(winners_file_path, engine='xlsxwriter') as writer:
        updated_winners.to_excel(writer, index=False, sheet_name='Winners')

# Streamlit App
st.markdown('<h1 class="single-line-title">🎉 कृषि विकास बैंक कर्मचारी संघ नेपाल उपहार कार्यक्रम २०८१ 🎉</h1>', unsafe_allow_html=True)
# Applying the CSS class to the subheader
st.markdown('<h3 class="centered-subheader">विजेता छान्नुहोस्!</h3>', unsafe_allow_html=True)

# Initialize session state variables
if 'drawn_ticket' not in st.session_state:
    st.session_state.drawn_ticket = None
    st.session_state.prize = None
    st.session_state.show_prize = False
    st.session_state.winner_list = []  # To store previous winners
    st.session_state.show_reveal_button = True  # Track visibility of the reveal button

# Display the remaining prize inventory
st.sidebar.subheader("Remaining Prizes Inventory")
for prize, count in remaining_prizes.items():
    st.sidebar.write(f"{prize}: {count} remaining")

# Button to draw a ticket with a unique key
if st.button('🎟️🎫 Draw a Ticket', key='draw_ticket_button'):
    ticket, prize = draw_ticket()

    if prize == "No More Prizes Available":
        st.error("No More Prizes Available")  # Show an error message
    elif prize:
        # Prevent duplicate tickets
        if ticket not in drawn_tickets:
            st.session_state.drawn_ticket = ticket
            st.session_state.prize = prize
            st.session_state.show_prize = False
            st.session_state.show_reveal_button = False  # Hide the reveal button

            # Show the ticket number with ball animation
            display_ticket_digits_with_ball_animation(ticket)

            st.subheader("Prize Wheel!")

# Button to reveal the prize with a unique key
if not st.session_state.show_reveal_button and st.session_state.drawn_ticket and st.button("के पर्यो त?", key='reveal_prize_button'):
    st.session_state.show_prize = True

if st.session_state.show_prize:
    prize_image_path = prize_images.get(st.session_state.prize, None)

    if prize_image_path and os.path.exists(prize_image_path):
        result_text = f"🎫 Ticket {st.session_state.drawn_ticket} wins: {st.session_state.prize} 🎁"
        st.markdown(f"<h2 style='text-align:center;'>{result_text}</h2>", unsafe_allow_html=True)
        st.image(prize_image_path, caption=st.session_state.prize, width=300)
    else:
        st.error("Prize image not found.")

    # Append the winner to the winner list (Ticket and Prize)
    st.session_state.winner_list.append({
        "Ticket Number": st.session_state.drawn_ticket,
        "Prize": st.session_state.prize
    })

    # Show the reveal button again for the next draw
    st.session_state.show_reveal_button = True

# Automatically save the updated winner list to the Excel file
if st.session_state.winner_list:
    # Save the winners to the Excel file
    df_winners = pd.DataFrame(st.session_state.winner_list)
    save_winners_to_excel(df_winners)

    # Display the list of all winners in a table
    st.subheader("All Winners")
    st.dataframe(df_winners)

    # Provide a button for manual download
    st.download_button(
        label="Download Winners List as Excel",
        data=BytesIO(open(winners_file_path, 'rb').read()),
        file_name='winners_list.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Footer
st.markdown('<div class="footer">© 2024 कृषि विकास बैंक कर्मचारी संघ !!</div>', unsafe_allow_html=True)
