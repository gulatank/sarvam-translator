# Sarvam AI Translation Service

A Python-based translation service that supports both text and voice translation using Sarvam AI's API. This service can translate between multiple Indian languages and includes text-to-speech capabilities.

## Features

- Text translation between multiple Indian languages
- Voice-to-text translation
- Text-to-speech output
- Support for multiple language pairs
- High-quality voice synthesis

## Supported Languages

- English (en-IN)
- Hindi (hi-IN)
- Bengali (bn-IN)
- Gujarati (gu-IN)
- Kannada (kn-IN)
- Malayalam (ml-IN)
- Marathi (mr-IN)
- Odia (od-IN)
- Punjabi (pa-IN)
- Tamil (ta-IN)
- Telugu (te-IN)

## Prerequisites

- Python 3.7+
- ffmpeg (for voice recording and audio processing)
- Sarvam AI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sarvam-translator.git
cd sarvam-translator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Sarvam AI API key:
```
SARVAM_API_KEY=your_api_key_here
```

## Usage

Run the translator:
```bash
python translator.py
```

### Text Translation
1. Choose option 1
2. Enter the text to translate
3. Enter source language code (e.g., 'en' for English)
4. Enter target language code (e.g., 'hi' for Hindi)

### Voice Translation
1. Choose option 2
2. Enter source language code
3. Enter target language code
4. Press Enter to start recording
5. Speak for 5 seconds
6. Wait for translation and audio playback

## Requirements

- python-dotenv==1.0.0
- SpeechRecognition==3.10.0
- gTTS==2.4.0
- pygame==2.5.2
- httpx==0.27.0

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 