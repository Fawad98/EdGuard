import streamlit as st
import pickle
import cohere

# Initialize Cohere Client
API_KEY = st.secrets['API']
co = cohere.Client(API_KEY)  # Replace with your Cohere API key

# Function to generate text using Cohere API
# Function to generate text using Cohere API
def generate_text(prompt, temperature):
    response = co.generate(
        model=st.secrets['ModelID'],  # Replace with your Cohere model ID
        prompt=prompt,
        max_tokens= 2000,
        temperature=temperature,
        stop_sequences=['\n\n'],
    )
    return response

# Function to save chat history
def save_chat_history(chat_history):
    with open("chat_history.pkl", "wb") as file:
        pickle.dump(chat_history, file)

# Function to load chat history
def load_chat_history():
    try:
        with open("chat_history.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# Streamlit app
def main():
    st.markdown(
        """
        <style>
        body {
            background-image: url("https://www.creativefabrica.com/wp-content/uploads/2020/08/09/Set-of-hand-drawn-books-in-doodle-style-Graphics-4900608-1-580x385.jpg"); /* Replace "background.jpg" with your custom image */
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("EdGuard 📚🤓")
    st.write("Welcome to EdGuard your learning partner! 😉😎")
    st.write("Use the example prompt or write your own. ✍🏼")
    
    # Load chat history
    chat_history = load_chat_history()
    
    # Temperature slider
    temperature = st.slider("Creativity", min_value=0.1, max_value=1.0, step=0.1, value=0.5)
    
    # Example prompts
    example_prompts = [
        "What is the acceleration due to gravity on the surface of the Earth (approximately 9.81 m/s²)?",
        "What is the molar mass of carbon dioxide (CO2) to the nearest gram per mole (approximately 44 g/mol)?",
        "Solve for x: 2x + 5 = 11."
    ]
    
    # Prompt selection
    prompt_option = st.selectbox("Choose or enter a query:", ["Select an example query"] + example_prompts + ["Enter your own query"])
    
    # Text area for custom prompt
    if prompt_option == "Enter your own query":
        prompt = st.text_area("Start Writing:")
    elif prompt_option == "Select an example query":
        prompt = ""
    else:
        prompt = prompt_option
    
    # Generate text on button click
    if st.button("Let's start learning!"):
        with st.spinner("Generating..."):
            generated_text = generate_text(prompt, temperature)
        st.success("Yay!🎉 I found something, let's look at it.")
        st.write(generated_text)
        
        # Save chat history
        chat_history.append({"Question": prompt, "Response": generated_text})
        save_chat_history(chat_history)

if __name__ == "__main__":
    main()
