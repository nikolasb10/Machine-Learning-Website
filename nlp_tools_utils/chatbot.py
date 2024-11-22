import streamlit as st
from general_utils.make_hf_requests import make_hf_requests
import shelve
from transformers import AutoTokenizer

model_name = "facebook/blenderbot-400M-distill"

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
MAX_TOKENS = 128  # Set to the model's maximum token limit

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Load tokenizer for truncating input text to token limit
tokenizer = AutoTokenizer.from_pretrained(model_name)

def get_truncated_history():
    """Concatenate messages and truncate to the model's token limit."""
    conversation_text = "\n".join(
        f"{USER_AVATAR if msg['role'] == 'user' else BOT_AVATAR}: {msg['content']}" 
        for msg in st.session_state.messages[-5:]  # Keep only the last 5 messages for context
    )
    
    # Truncate tokens if conversation exceeds MAX_TOKENS
    tokens = tokenizer(conversation_text, truncation=True, max_length=MAX_TOKENS, return_tensors="pt")
    truncated_text = tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)
    
    return truncated_text

def chatbot():
    # Initialize or load chat history
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()
        _ = make_hf_requests(model_name, {"inputs": ""})

    # Sidebar with a button to delete chat history
    with st.sidebar:
        if st.button("Delete Chat History"):
            st.session_state.messages = []
            save_chat_history([])

    messages = st.container(height=350)
    # Display chat messages in reverse order, so the latest message appears at the top
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        messages.chat_message(message["role"], avatar=avatar).write(message["content"])

    # Main chat input
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        messages.chat_message("user", avatar=USER_AVATAR).write(prompt)

        # Get truncated conversation history
        conversation_text = get_truncated_history()

        # Make request to the model with truncated history
        response = make_hf_requests(model_name, {"inputs": conversation_text})
        print(response)

        # Handle model response
        bot_response = response.get("content") if isinstance(response, dict) else response

        generated_text = bot_response[0]["generated_text"]
        messages.chat_message("assistant", avatar=BOT_AVATAR).write(generated_text)
        st.session_state.messages.append({"role": "assistant", "content": generated_text})

    # Save chat history
    save_chat_history(st.session_state.messages)
