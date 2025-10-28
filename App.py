import streamlit as st
import random
import pickle
import os

# Save and load data with pickle
SAVE_FILE = "game_data.pkl"

def save_game(data):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    return None

# Initialize session state
for key, default in {
    "secret_number": None,
    "attempts_left": 0,
    "upper_limit": 0,
    "difficulty_selected": False,
    "message": "",
    "game_over": False,
    "total_games": 0,
    "total_wins": 0,
    "show_goodbye": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Title
st.title("🎯 Advanced Number Guessing Game")
with st.expander("ℹ️ About / How to Play", expanded=True):
    st.markdown("""
    **Welcome to the Advanced Number Guessing Game! 🎯**

    🕹️ **How to Play**
    - Choose a **difficulty level** to start:
        - 🟢 *Easy:* Guess a number between **1–50** with **10 attempts**
        - 🟡 *Medium:* Guess a number between **1–100** with **7 attempts**
        - 🔴 *Hard:* Guess a number between **1–200** with **5 attempts**
    - Enter your guess and click **Guess**.
    - You’ll get hints whether your guess is **too high** or **too low**.
    - Try to guess the secret number before you run out of attempts!

    🧠 **Game Features**
    - Tracks your **wins and total games played**
    - Option to **play again** or **exit** when done
    - Displays your **final stats** when you quit
    - Clean, simple Streamlit interface for smooth gameplay

    💡 *Tip:* The fewer guesses you use, the sharper your guessing skills!
    """)


# Goodbye message section
if st.session_state.show_goodbye:
    st.markdown("### 👋 Thanks for playing! Goodbye!")
    st.markdown(f"""
    **📊 Final Game Stats:**
    - Total Games Played: `{st.session_state.total_games}`
    - Total Wins: `{st.session_state.total_wins}`
    """)
    
    # 🎮 Start new game button
    if st.button("🎮 Start New Game"):
        for key in list(st.session_state.keys()):
            if key not in ["total_games", "total_wins"]:
                del st.session_state[key]
        st.session_state.show_goodbye = False
        st.rerun()
    
    st.stop()

# Difficulty selection
if not st.session_state.difficulty_selected and not st.session_state.game_over:
    st.subheader("Choose Difficulty Level")
    difficulty = st.radio(
        "Select level:",
        ("Easy (1–50, 10 attempts)", "Medium (1–100, 7 attempts)", "Hard (1–200, 5 attempts)")
    )

    if st.button("Start Game"):
        if "Easy" in difficulty:
            st.session_state.upper_limit = 50
            st.session_state.attempts_left = 10
        elif "Medium" in difficulty:
            st.session_state.upper_limit = 100
            st.session_state.attempts_left = 7
        else:
            st.session_state.upper_limit = 200
            st.session_state.attempts_left = 5

        st.session_state.secret_number = random.randint(1, st.session_state.upper_limit)
        st.session_state.difficulty_selected = True
        save_game(st.session_state)
        st.rerun()

# Gameplay section
elif st.session_state.difficulty_selected and not st.session_state.game_over:
    st.write(f"I'm thinking of a number between 1 and {st.session_state.upper_limit}.")
    st.write(f"Attempts left: {st.session_state.attempts_left}")

    guess = st.number_input("Enter your guess:", min_value=1, max_value=st.session_state.upper_limit, step=1)

    if st.button("Guess"):
        if st.session_state.attempts_left > 0:
            st.session_state.attempts_left -= 1

            if guess < st.session_state.secret_number:
                st.session_state.message = f"Too low! 🔽 Attempts left: {st.session_state.attempts_left}"
            elif guess > st.session_state.secret_number:
                st.session_state.message = f"Too high! 🔼 Attempts left: {st.session_state.attempts_left}"
            else:
                st.session_state.message = f"🎉 Correct! The number was {st.session_state.secret_number}."
                st.session_state.total_wins += 1
                st.session_state.game_over = True
                st.session_state.difficulty_selected = False

            if st.session_state.attempts_left == 0 and guess != st.session_state.secret_number:
                st.session_state.message = f"😢 YOU ARE OUT OF ATTEMPTS! The number was {st.session_state.secret_number}."
                st.session_state.game_over = True
                st.session_state.difficulty_selected = False

            save_game(st.session_state)
            st.rerun()

    st.write(st.session_state.message)

# Game over section
if st.session_state.game_over:
    # Increment total games only once
    if "game_counted" not in st.session_state or not st.session_state.game_counted:
        st.session_state.total_games += 1
        st.session_state.game_counted = True

    st.write(st.session_state.message)

    st.write("Would you love to play again?")
    choice = st.radio("", ["Yes", "No"], horizontal=True)

    if choice == "Yes":
        if st.button("Play Again"):
            for key in list(st.session_state.keys()):
                if key not in ["total_games", "total_wins"]:
                    del st.session_state[key]
            st.rerun()

    elif choice == "No":
        if st.button("Exit Game"):
            st.session_state.show_goodbye = True
            st.rerun()
st.write("---")

st.markdown("© 2025 All rights reserved | Developed by PRINCEDEX")
st.write("Contact: [ifeanyistephen003@gmail.com]")
