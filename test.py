from gtts import gTTS
from googletrans import Translator
import os
from pydub import AudioSegment

def text_to_speech(message, language='en'):
    # Translate the message if needed
    if language != 'en':
        translator = Translator(service_urls=['translate.google.com'])
        translated_message = translator.translate(message, src='en', dest=language).text
    else:
        translated_message = message

    # Load your voice recording using pydub
    voice_recording = AudioSegment.from_file('narendra modi speech.mp3', format='mp3')

    # Convert the voice recording to raw audio data
    audio_data = voice_recording.raw_data

    # Generate the speech using your voice recording
    def custom_voice(text, lang):
        return audio_data

    tts = gTTS(text=translated_message, lang=language, slow=False, tld='com', pre_processor_funcs=[custom_voice])
    tts.save('output.mp3')

    # Play the speech
    os.system('start output.mp3')

# Example usage
text_to_speech('Hello, how are you doing today?', language='en')
