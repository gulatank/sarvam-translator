import os
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import httpx

# Load environment variables
load_dotenv()

# Supported language codes
SUPPORTED_LANGUAGES = {
    'en': 'en-IN',  # English
    'hi': 'hi-IN',  # Hindi
    'bn': 'bn-IN',  # Bengali
    'gu': 'gu-IN',  # Gujarati
    'kn': 'kn-IN',  # Kannada
    'ml': 'ml-IN',  # Malayalam
    'mr': 'mr-IN',  # Marathi
    'od': 'od-IN',  # Odia
    'pa': 'pa-IN',  # Punjabi
    'ta': 'ta-IN',  # Tamil
    'te': 'te-IN',  # Telugu
    'auto': 'auto'  # Auto-detect
}

class Translator:
    def __init__(self):
        # Initialize API key and base URL
        self.api_key = os.getenv('SARVAM_API_KEY')
        self.base_url = "https://api.sarvam.ai"
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
    def get_language_code(self, lang):
        """
        Convert short language code to full language code
        """
        return SUPPORTED_LANGUAGES.get(lang.lower(), lang)
        
    def text_translate(self, text, source_lang, target_lang):
        """
        Translate text from source language to target language using Sarvam AI
        """
        try:
            # Convert language codes to full format
            source_lang = self.get_language_code(source_lang)
            target_lang = self.get_language_code(target_lang)
            
            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "input": text,
                "source_language_code": source_lang,
                "target_language_code": target_lang,
                "mode": "formal"  # Using formal mode as default
            }
            
            response = httpx.post(
                f"{self.base_url}/translate",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('translated_text')
            else:
                print(f"Translation error: {response.text}")
                return None
                
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None

    def voice_to_text(self):
        """
        Convert voice input to text using Sarvam AI Speech-to-Text
        """
        try:
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
            
            # Ask for confirmation before recording
            print("\nReady to record. You will have 5 seconds to speak.")
            input("Press Enter to start recording...")
            
            # Record audio using system command with better feedback
            print("\nRecording... (5 seconds)")
            os.system(f"ffmpeg -f avfoundation -i ':0' -t 5 -y {temp_audio_path}")
            print("Recording complete!")
            
            # Use Sarvam AI Speech-to-Text API
            headers = {
                "api-subscription-key": self.api_key
            }
            
            files = {
                'file': ('audio.wav', open(temp_audio_path, 'rb'), 'audio/wav')
            }
            
            print("Converting speech to text...")
            response = httpx.post(
                f"{self.base_url}/speech-to-text",
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                transcript = result.get('transcript')
                if transcript:
                    print(f"Recognized text: {transcript}")
                    return transcript
                else:
                    print("No speech was detected in the recording.")
                    return None
            else:
                print(f"Speech recognition error: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in voice recognition: {str(e)}")
            return None
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

    def text_to_voice(self, text, lang='en-IN'):
        """
        Convert text to voice output using Sarvam AI's text-to-speech API
        """
        try:
            # Ensure language code is in correct format
            lang = self.get_language_code(lang)
            
            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "target_language_code": lang,
                "speaker": "meera",  # Using lowercase speaker name
                "pitch": 0,          # Default pitch
                "pace": 1,           # Default pace
                "loudness": 1,       # Default loudness
                "speech_sample_rate": 22050,  # Default sample rate
                "enable_preprocessing": True,  # Enable preprocessing for better handling of mixed-language text
                "model": "bulbul:v1"  # Using the latest model
            }
            
            print("Converting text to speech...")
            response = httpx.post(
                f"{self.base_url}/text-to-speech",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                audio_base64 = result.get('audios', [None])[0]
                
                if audio_base64:
                    # Convert base64 to audio file
                    import base64
                    audio_data = base64.b64decode(audio_base64)
                    
                    # Save to temporary file
                    temp_file = "temp_speech.wav"
                    with open(temp_file, "wb") as f:
                        f.write(audio_data)
                    
                    # Convert to afplay-compatible format
                    temp_file_afplay = "temp_speech_afplay.wav"
                    os.system(f"ffmpeg -y -i {temp_file} -acodec pcm_s16le -ar 44100 {temp_file_afplay}")
                    try:
                        # Play the audio using system's afplay command
                        print("Playing audio...")
                        os.system(f"afplay {temp_file_afplay}")
                        print("Audio playback complete!")
                    except Exception as e:
                        print(f"Error playing audio: {str(e)}")
                    finally:
                        # Clean up
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                        if os.path.exists(temp_file_afplay):
                            os.remove(temp_file_afplay)
                else:
                    print("No audio data received from the API")
            else:
                print(f"Text-to-speech error: {response.text}")
                
        except Exception as e:
            print(f"Text-to-speech error: {str(e)}")

    def voice_translate(self, source_lang, target_lang):
        """
        Complete voice-to-voice translation
        """
        # Get voice input
        input_text = self.voice_to_text()
        if not input_text:
            print("Could not recognize speech. Please try again.")
            return
        
        # Translate the text
        print(f"\nTranslating from {source_lang} to {target_lang}...")
        translated_text = self.text_translate(input_text, source_lang, target_lang)
        if not translated_text:
            print("Translation failed. Please try again.")
            return
        
        # Convert translated text to voice
        print(f"Translated text: {translated_text}")
        print("Playing translated audio...")
        self.text_to_voice(translated_text, lang=target_lang)

def main():
    translator = Translator()
    
    # Print supported languages
    print("\nSupported Languages:")
    for code, full_code in SUPPORTED_LANGUAGES.items():
        if code != 'auto':
            print(f"- {code}: {full_code}")
    
    while True:
        print("\nTranslation Service")
        print("1. Text Translation")
        print("2. Voice Translation")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            text = input("Enter text to translate: ")
            source_lang = input("Enter source language code (e.g., 'en' for English): ")
            target_lang = input("Enter target language code (e.g., 'hi' for Hindi): ")
            
            translated = translator.text_translate(text, source_lang, target_lang)
            if translated:
                print(f"Translated text: {translated}")
                
        elif choice == "2":
            source_lang = input("Enter source language code (e.g., 'en' for English): ")
            target_lang = input("Enter target language code (e.g., 'hi' for Hindi): ")
            translator.voice_translate(source_lang, target_lang)
            
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 