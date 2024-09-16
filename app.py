import streamlit as st
import whisper
import tempfile
import os

st.title("My Transcription App")

# Upload an Audio file with Streamlit
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

model = whisper.load_model("base")
st.text("Whisper Model Loaded")

if st.sidebar.button("Transcribe Audio"):
    if audio_file is not None:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as temp_file:
            temp_file.write(audio_file.read())
            temp_file_path = temp_file.name

        st.sidebar.success("Transcribing Audio")

        # Transcribe audio using the temporary file path
        try:
            transcription = model.transcribe(temp_file_path)
            st.sidebar.success("Transcription Complete")
            
            # Process transcription text to add paragraphs
            # Split the transcription text into paragraphs if needed
            transcription_text = transcription["text"]
            paragraphs = transcription_text.split('\n')  # Assuming paragraphs are separated by newlines

            # Join paragraphs with Markdown double line breaks
            formatted_text = '\n\n'.join(paragraphs)
            
            st.markdown(formatted_text)  # Display formatted text in Markdown
        except Exception as e:
            st.sidebar.error(f"Transcription failed: {str(e)}")
        
        # Clean up temporary file
        os.remove(temp_file_path)
    else:
        st.sidebar.error("Please Upload an audio file")

st.sidebar.header("Play the Original Audio File")
if audio_file is not None:
    st.sidebar.audio(audio_file)
