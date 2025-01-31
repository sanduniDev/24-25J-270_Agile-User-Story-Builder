import os
import tempfile
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechRecognizer, ResultReason
from io import BytesIO
def process_audio_file(audio_file_content: BytesIO, audio_file_name: str):
    azure_speech_key = "9NczgsFdt96EbPY8iqRDOph2sbqEtbrd2DSX0CEYUnoyHLmFmnUnJQQJ99ALACYeBjFXJ3w3AAAYACOGCojk" 
    azure_region = "eastus"  
    azure_endpoint = "https://eastus.api.cognitive.microsoft.com/"  

    speech_config = SpeechConfig(subscription=azure_speech_key, region=azure_region)
    speech_config.endpoint_id = azure_endpoint

    # Create a temporary file to save the in-memory content
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_audio_file.write(audio_file_content.read())  # Write the in-memory file content to the temp file
        temp_audio_file_path = temp_audio_file.name  # Get the path of the temp file
        
        # Close the file explicitly to ensure it's not open when trying to delete
        temp_audio_file.close()

    # Now, use the temporary file for transcription
    audio_config = AudioConfig(filename=temp_audio_file_path)
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print(f"Transcribing {audio_file_name}...")
    result = recognizer.recognize_once()

    # Clean up the temporary file after processing
    # try:
    #     os.remove(temp_audio_file_path)
    # except Exception as e:
    #     print(f"Error removing temporary file: {e}")

    if result.reason == ResultReason.RecognizedSpeech:
        transcription = result.text
        print(f"Transcription completed for {audio_file_name}.")
        return transcription, "Predicted successfully"
    elif result.reason == ResultReason.NoMatch:
        transcription = "No speech could be recognized."
        print(f"No speech could be recognized in {audio_file_name}.")
        return transcription, "No speech detected"
    else:
        raise Exception(f"Error during transcription: {result.reason}")
