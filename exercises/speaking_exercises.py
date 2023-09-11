import streamlit as st
from langchain.chat_models import ChatOpenAI
from apikey import api_key
from langchain.prompts.chat import SystemMessage, HumanMessage
import speech_recognition as sr
import pyaudio

# App Framework
st.set_page_config(page_title="LangTutGPT", page_icon="🤖")
st.title("Speaking Exercise")
languages = ["English", "Deutsch", "Türkçe", "日本語","Français","Italiano","Español","한국인"]
languages_shorts = ["en-EN", "de-DE", "tr-TR", "ja-JP", "fr-FR","it-IT","es-ES","ko-KR"]


sec = st.selectbox("Choose a language from options:", languages)
button = st.button("start")
topic = st.text_input("Enter an topic for speaking:")
sec_duration = st.number_input("How many seconds do you want to speak ?", min_value=1, value=30, step=1)


def main():
    if button:
        text = listen_to_audio()
        chat = ChatOpenAI(
            openai_api_key=api_key,
            temperature=0,
            model='gpt-3.5-turbo'
        )
        messages = [SystemMessage(
            content=(
                "You are a language exam judge.You will examine the text given to you by the user,whether the variety "
                "and based on grammatical rules, the variety of words in the text, and whether the content of the text "
                f"matches the {topic},give a score out of 10 and give feedback on areas that need improvement.")),
            HumanMessage(content=f"{text}")]
        response = chat(messages)
        st.write("You said:")
        st.write(text)
        st.write("My review:")
        st.write(response.content)


def listen_to_audio():
    global i, lang
    recognizer = sr.Recognizer()

    # Set the sampling frequency and duration for recording
    fs = 44100
    duration = sec_duration  # Recording duration in minutes

    # Record audio using pyaudio
    audio_data = record_audio(fs, duration)

    # Convert the recorded audio to text using the speech recognition library
    try:
        for i in range(len(languages)):
            if sec == languages[i]:
                lang = languages_shorts[i]
        text = recognizer.recognize_google(audio_data, language=lang)
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try again.")
        return ""
    except sr.RequestError as e:
        st.error(f"Error with the speech recognition service; {e}")
        return ""


def record_audio(fs, duration):
    audio_frames = []
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)

    st.write("Listening...")
    for _ in range(0, int(fs / 1024 * duration)):
        audio_frames.append(stream.read(1024))

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = b''.join(audio_frames)
    return sr.AudioData(audio_data, sample_rate=fs, sample_width=p.get_sample_size(pyaudio.paInt16))


if __name__ == "__main__":
    main()
