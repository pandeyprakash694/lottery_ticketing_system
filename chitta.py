import os
import streamlit as st
import random
import time
import pandas as pd
from io import BytesIO

# Placeholder URLs for prize images (use actual URLs or local files in a real scenario)
prize_images = {
    "Electric Jug (Yasuda)": "static\images\jug.jpg",
    "Iron (Yasuda)": "static\images\iron.png",
    "Mixture Grinder (Yasuda)": "static\images\mixture.png",
    "Smart TV (32 inches, Sansui)": "static\images\smarttv.png",
    "Dell Laptop": "static\images\jug.jpg",
    "Washing Machine": "static\images\jug.jpg",
    "iPhone 15": "static\images\jug.jpg",
    "Bike": "static\images\jug.jpg"
}

# Define ticket range and prizes
ticket_range = list(range(10000, 25001))

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
    </style>
    """, 
    unsafe_allow_html=True
)

# Apply the CSS class to the title
st.markdown('<h1 class="single-line-title">🎉 कृषि विकास बैंक कर्मचारी संघ उपहार कार्यक्रम २०८० 🎉</h1>', unsafe_allow_html=True)

# Applying the CSS class to the subheader
st.markdown('<h2 class="centered-subheader">विजेता छान्नुहोस्!</h2>', unsafe_allow_html=True)

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
        return "No more prizes available", None
    ticket, prize = prize_assignment.popitem()  # Remove and return a ticket and its prize
    return ticket, prize

# Function to display the ball with shuffling numbers and reveal the actual digit
def display_ticket_digits_with_ball_animation(ticket_number):
    ticket_str = str(ticket_number)  # Convert ticket number to string
    displayed_ticket = ""  # Start with an empty string

    # Create placeholders for displaying the ticket and the "rolling" ball
    ticket_placeholder = st.empty()
    ball_placeholder = st.empty()
    
    for i, digit in enumerate(ticket_str):
        displayed_ticket += digit  # Add the next digit to the displayed ticket
        
        # Shuffle numbers within the ball for 2 seconds
        start_time = time.time()
        while time.time() - start_time < 4:
            random_digit = random.randint(0, 9)
            ball_html = f"""
            <div style='text-align: center;'>
                <div style="width: 150px; height: 150px; background-color: red; border-radius: 50%; 
                            display: inline-block; text-align: center; line-height: 150px; color: white; 
                            font-size: 75px; margin: auto;">
                    {random_digit}
                </div>
            </div>
            """
            ball_placeholder.markdown(ball_html, unsafe_allow_html=True)
            time.sleep(0.1)  # Short delay to simulate fast number shuffling
        
        # After 2 seconds, display the actual digit
        ball_html = f"""
        <div style='text-align: center;'>
            <div style="width: 150px; height: 150px; background-color: red; border-radius: 50%; 
                        display: inline-block; text-align: center; line-height: 150px; color: white; 
                        font-size: 75px; margin: auto;">
                {digit}
            </div>
        </div>
        """
        ball_placeholder.markdown(ball_html, unsafe_allow_html=True)
        
        # Update the full ticket display
        ticket_placeholder.markdown(f"<h1 style='text-align: center;'>{displayed_ticket}{'_' * (len(ticket_str) - i - 1)}</h1>", unsafe_allow_html=True)
        time.sleep(5)  # Short delay before the next digit

# Button to draw a ticket
if st.button('🎟️ Draw a Ticket'):
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
    # Rotate images for 3 seconds before showing the actual prize
    placeholder_image = st.empty()  # Placeholder for prize image

    start_time = time.time()
    while time.time() - start_time < 3:
        # Display a random prize image every 0.5 seconds
        random_prize = random.choice(list(prize_images.values()))
        placeholder_image.image(random_prize, width=300)
        time.sleep(0.5)

    # Display the actual prize image and result text in the same row using flexbox
    # Display the actual prize image and result text in the same row using flexbox
    prize_image_path = prize_images.get(st.session_state.prize, None)  # Get the path for the current prize

    if prize_image_path and os.path.exists(prize_image_path):
        result_text = f"🎫 Ticket {st.session_state.drawn_ticket} wins: {st.session_state.prize} 🎁"

        # Clear the placeholder and show the final prize image and result text
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
if st.session_state.winner_list:
    st.subheader("All Winners")
    df_winners = pd.DataFrame(st.session_state.winner_list)
    st.dataframe(df_winners)

    # Export winners data to Excel
    def export_to_excel(data):
        df = pd.DataFrame(data)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Winners')
        buffer.seek(0)
        return buffer

    st.download_button(
        label="Download Winners List as Excel",
        data=export_to_excel(st.session_state.winner_list),
        file_name='winners_list.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Footer
st.markdown('<div class="footer">© 2024 कृषि विकास बैंक कर्मचारी संघ</div>', unsafe_allow_html=True)
