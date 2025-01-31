from flask import Blueprint, jsonify, request
from api.audio import process_audio_file
from api.inference import RequirementClassifier
from io import BytesIO

def create_blueprint():
    api_blueprint = Blueprint("api", __name__)

    @api_blueprint.route("/", methods=["GET"])
    def home():
        """
        Health check endpoint.
        """
        return jsonify({"message": "Requirement Classifier API is running!"}), 200

    @api_blueprint.route("/predict", methods=["POST"])
    def handle_predict_request():
        """
        Handle prediction requests via HTTP with a wave audio file.
        Broadcast prediction status via WebSocket.
        """
        try:
            if 'audio' not in request.files:
                raise ValueError("Invalid input, 'audio' file is required")

            audio_file = request.files['audio']
            if not audio_file.filename.endswith('.wav'):
                raise ValueError("Invalid file format, only '.wav' files are supported")

            audio_file_content = BytesIO(audio_file.read())

            print(f"Audio Processing")
            transcription, message = process_audio_file(audio_file_content, audio_file.filename)
            # transcription="""Visitors to the platform are welcomed by an onboarding process featuring a captivating hero image that showcases the Mystery Machine, the Mystery Team, and silhouetted characters representing new additions to the gang. Prominent call to action buttons encourage users to build your character or build dog character and engage with the platform score features. As users scroll through the landing page, they encounter visually appealing product highlights dynamic parallax effects."""
            # message="speech detected"

            if message=="No speech detected":
                raise ValueError("No Speech detected on the .wav file")
            
            classifier= RequirementClassifier()
            sentences =classifier.split_paragraph_into_sentences(transcription)
            results=[]
            for sentence in sentences:
                result=classifier.classify_requirements(sentence)
                results.append(result)

            print(jsonify({"results": results}))
            return jsonify({"results": results}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
  
    return api_blueprint
