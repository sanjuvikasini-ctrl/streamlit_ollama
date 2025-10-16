import streamlit as st
import ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Ollama Query App",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Ollama LLM Query Application")
st.markdown("Query local Ollama models using Streamlit")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Ollama connection settings
    ollama_host = st.text_input(
        "Ollama Host",
        value=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        help="URL of Ollama server"
    )
    
    # Available models (you can customize this)
    available_models = ["llama2", "mistral", "neural-chat", "dolphin-mixtral"]
    selected_model = st.selectbox(
        "Select Model",
        available_models,
        help="Choose which Ollama model to use"
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness: 0=deterministic, 1=random"
    )
    
    # Top-p slider
    top_p = st.slider(
        "Top P (Nucleus Sampling)",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1,
        help="Controls diversity via nucleus sampling"
    )

# Main content area
st.subheader("📝 Query Input")

# Text input for user query
user_query = st.text_area(
    "Enter your prompt:",
    placeholder="Ask me anything...",
    height=150
)

# Columns for buttons
col1, col2 = st.columns([1, 4])

with col1:
    submit_button = st.button("🚀 Submit Query", use_container_width=True)

# Process query
if submit_button and user_query:
    try:
        st.info("⏳ Connecting to Ollama and generating response...")
        
        # Initialize Ollama client
        client = ollama.Client(host=ollama_host)
        
        # Generate response
        with st.spinner("Generating response..."):
            response = client.generate(
                model=selected_model,
                prompt=user_query,
                stream=False,
                options={
                    "temperature": temperature,
                    "top_p": top_p,
                }
            )
        
        # Display response
        st.success("✅ Response generated successfully!")
        
        st.subheader("📤 Response:")
        st.write(response['response'])
        
        # Display metadata
        with st.expander("📊 Response Metadata"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model", selected_model)
            with col2:
                st.metric("Temperature", temperature)
            with col3:
                st.metric("Top P", top_p)
            
            st.json({
                "total_duration": response.get('total_duration'),
                "load_duration": response.get('load_duration'),
                "prompt_eval_count": response.get('prompt_eval_count'),
                "eval_count": response.get('eval_count'),
            })
    
    except ConnectionError:
        st.error(f"❌ Could not connect to Ollama at {ollama_host}")
        st.info("Make sure Ollama is running and accessible at the specified host")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Please check your input and try again")

elif submit_button and not user_query:
    st.warning("⚠️ Please enter a query before submitting")

# Footer
st.divider()
st.markdown("""
---
**How to use this app:**
1. Ensure Ollama is running on your system
2. Select a model from the sidebar
3. Adjust model parameters (temperature, top_p)
4. Enter your query and click Submit
5. Wait for the response

**More info:**
- [Ollama Documentation](https://ollama.ai)
- [Streamlit Documentation](https://streamlit.io)
""")
