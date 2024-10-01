import os
import streamlit as st
import random
import time
import pandas as pd
from io import BytesIO
from gtts import gTTS
import playsound


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
# Function to convert a number to speech
# Function to play the sound for the digit
def play_digit_sound(digit):
    sound_file = digit_sounds.get(digit)
    if sound_file and os.path.exists(sound_file):
        st.audio(sound_file)


# Placeholder URLs for prize images (use actual URLs or local files in a real scenario)
prize_images = {
    "Electric Jug (Yasuda)": "static\images\jug.png",
    "Iron (Yasuda)": "static\images\iron.png",
    "Mixture Grinder (Yasuda)": "static\images\mixture.png",
    "Smart TV (32 inches, Sansui)": "static\images\smarttv.png",
    "Dell Laptop": "static\images\dell.png",
    "Washing Machine": "static\images\washing.png",
    "iPhone 15": "static\images\iphone.png",
    "Bike": "static\images\ike.png",
}

# Define the list of numbers that should be excluded
#excluded_numbers = [10123, 10567, 20000, 23000]  # Replace with actual numbers to exclude

# Define ticket range and prizes
ticket_range = list(range(10000, 25001))

# Exclude the unwanted numbers from the ticket range
#filtered_ticket_range = [ticket for ticket in ticket_range if ticket not in excluded_numbers]

# File path to save the winners list
winners_file_path = "winners.xlsx"

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

# Create a list of prizes
prize_list = []
for prize, quantity in prizes.items():
    prize_list.extend([prize] * quantity)

# Shuffle the ticket numbers and prize list
random.shuffle(ticket_range)

# Shuffle the ticket numbers after filtering
#random.shuffle(filtered_ticket_range)

random.shuffle(prize_list)

# Create a dictionary to store ticket and prize assignments
prize_assignment = dict(zip(ticket_range, prize_list))

# Streamlit App
# Custom CSS to center content
st.markdown(
    """
    <style>
    .single-line-title {
        font-size: 40px;
        text-align: center;
    }
    .centered-subheader {
        text-align: center;
    }
    .centered-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .prize-box {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px;
    }
    .prize-image {
        max-width: 300px;
        height: auto;
        margin-right: 20px;
    }
    .prize-text {
        text-align: center;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
    }
     .logo {
        text-align: center;
        margin-bottom: 20px; /* Add some spacing below the logo */
        margin-left: 100px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Display logo at the top of the page
#st.markdown('<div class="logo"><img src="static/images/logo.png" width="200"/></div>', unsafe_allow_html=True)
#st.image('static/images/logo.png', width=200)
# Apply the CSS class to the title
st.markdown('<h1 class="single-line-title">🎉 कृषि विकास बैंक कर्मचारी संघ उपहार कार्यक्रम २०८१ 🎉</h1>', unsafe_allow_html=True)

# Applying the CSS class to the subheader
st.markdown('<h3 class="centered-subheader">विजेता छान्नुहोस्!</h3>', unsafe_allow_html=True)

# Initialize session state variables
if 'drawn_ticket' not in st.session_state:
    st.session_state.drawn_ticket = None
    st.session_state.prize = None
    st.session_state.show_prize = False
    st.session_state.winner_list = []  # To store previous winners
    st.session_state.show_reveal_button = True  # Track visibility of the reveal button

# Function to draw a ticket
def draw_ticket():
    if not prize_assignment:
        return "No More Prizes Available", None
    ticket, prize = prize_assignment.popitem()  # Remove and return a ticket and its prize
    return ticket, prize

# Function to display the ball with shuffling numbers and reveal the actual digit
def display_ticket_digits_with_ball_animation(ticket_number):
    ticket_str = str(ticket_number)
    displayed_ticket = ""

    ticket_placeholder = st.empty()
    ball_placeholder = st.empty()
    audio_placeholder = st.empty()

    for i, digit in enumerate(ticket_str):
        displayed_ticket += digit

        start_time = time.time()
        while time.time() - start_time < 0.1:
            random_digit = random.randint(0, 9)
            ball_html = f"""
            <div style='text-align: center;'>
                <div style="width: 150px; height: 150px; background-color: green; border-radius: 50%; 
                            display: inline-block; text-align: center; line-height: 150px; color: white; 
                            font-size: 75px; margin: auto;">
                    {random_digit}
                </div>
            </div>
            """
            ball_placeholder.markdown(ball_html, unsafe_allow_html=True)
            time.sleep(0.1)

        ball_html = f"""
        <div style='text-align: center;'>
            <div style="width: 150px; height: 150px; background-color: green; border-radius: 50%; 
                        display: inline-block; text-align: center; line-height: 150px; color: white; 
                        font-size: 75px; margin: auto;">
                {digit}
            </div>
        </div>
        """
        ball_placeholder.markdown(ball_html, unsafe_allow_html=True)

        sound_file_path = f"static/sounds/digit_{digit}.mp3"
        if os.path.exists(sound_file_path):
            audio_placeholder.audio(sound_file_path, autoplay=True)

        ticket_placeholder.markdown(f"<h1 style='text-align: center;'>{displayed_ticket}{'_' * (len(ticket_str) - i - 1)}</h1>", unsafe_allow_html=True)
        time.sleep(0.1)

# Exporting to separate excel file

# Function to load existing winners from the file if it exists
def load_existing_winners():
    if os.path.exists(winners_file_path):
        # Read existing data from the Excel file
        return pd.read_excel(winners_file_path)
    else:
        # Return an empty DataFrame if no file exists
        return pd.DataFrame(columns=["Ticket Number", "Prize"])

# Function to save winners to the Excel file
def save_winners_to_excel(data):
    df = pd.DataFrame(data)

    # Load existing winners
    existing_winners = load_existing_winners()

    # Append new winners to the existing ones
    updated_winners = pd.concat([existing_winners, df], ignore_index=True)

    # Save the updated winners list back to the Excel file
    with pd.ExcelWriter(winners_file_path, engine='xlsxwriter') as writer:
        updated_winners.to_excel(writer, index=False, sheet_name='Winners')


# Button to draw a ticket
if st.button('🎟️🎫 Draw a Ticket'):
    ticket, prize = draw_ticket()

    if prize:
        # Save drawn ticket and prize to session state
        st.session_state.drawn_ticket = ticket
        st.session_state.prize = prize
        st.session_state.show_prize = False
        st.session_state.show_reveal_button = False  # Hide the reveal button

        # Show the ticket number with ball animation
        display_ticket_digits_with_ball_animation(ticket)

        st.subheader("Prize Wheel!")


# Button to reveal the prize
if not st.session_state.show_reveal_button and st.session_state.drawn_ticket and st.button("के पर्यो त?"):
    st.session_state.show_prize = True

if st.session_state.show_prize:
    placeholder_image = st.empty()

    start_time = time.time()
    while time.time() - start_time < 0.1:
        random_prize = random.choice(list(prize_images.values()))
        placeholder_image.image(random_prize, width=300)
        time.sleep(0.1)

    prize_image_path = prize_images.get(st.session_state.prize, None)

    if prize_image_path and os.path.exists(prize_image_path):
        result_text = f"🎫 Ticket {st.session_state.drawn_ticket} wins: {st.session_state.prize} 🎁"
        placeholder_image.empty()
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

# Display the list of all winners in a table
# After a winner is drawn and added to the list
if st.session_state.winner_list:
    # Automatically save the updated winner list to the Excel file
    save_winners_to_excel(st.session_state.winner_list)

    # Display the list of all winners in a table
    st.subheader("All Winners")
    df_winners = pd.DataFrame(st.session_state.winner_list)
    st.dataframe(df_winners)

    # Provide a button for manual download (optional)
    st.download_button(
        label="Download Winners List as Excel",
        data=BytesIO(open(winners_file_path, 'rb').read()),
        file_name='winners_list.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Footer
st.markdown('<div class="footer">© 2024 कृषि विकास बैंक कर्मचारी संघ !!</div>', unsafe_allow_html=True)
