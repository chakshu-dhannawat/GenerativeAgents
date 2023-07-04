from gtts import gTTS
import subprocess

# Dictionary to store the voice samples for each agent
agent_voices = {
    'Agent1': 'English Speeches - Amitabh Bachchan.mp3'
}

def generate_voiceover(agent, text):
    voice_sample = agent_voices.get(agent)
    if voice_sample is None:
        print("Voice sample not found for the agent.")
        return

    # Call gTTS to generate voiceover in Japanese
    tts = gTTS(text, lang='ja')
    tts.save('English_voiceover.mp3')

    # Convert the voiceover to the desired voice sample
    subprocess.call(['ffmpeg', '-i', 'voiceover.mp3', '-af', f'apad=pad_dur=2,atrim=0:7,volume=10', voice_sample])

    # Cleanup temporary files
    subprocess.call(['rm', 'voiceover.mp3'])
