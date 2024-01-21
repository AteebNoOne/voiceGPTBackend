from flask import Flask, abort, request, jsonify,send_file, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
from pymongo import MongoClient
from flask_cors import CORS
import re
import assemblyai as aai
import os
from datetime import datetime
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv  

app = Flask(__name__)
CORS(app)




# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

aai.settings.api_key = os.getenv("AA_API_KEY")
transcriber = aai.Transcriber()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
atlas_username = os.getenv("ATLAS_USERNAME")
atlas_password = os.getenv("ATLAS_PASSWORD")
atlas_cluster_uri = os.getenv("ATLAS_CLUSTER_URI")
database_name = os.getenv("DATABASE_NAME")
collection_name = os.getenv("COLLECTION_NAME")

atlas_uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster_uri}/{database_name}?retryWrites=true&w=majority"

client = MongoClient(atlas_uri)
db = client['voiceGPT'] 
users_collection = db['users']

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_index(path):
    return send_file('index.html')

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(root_dir, './static'), filename)

# Serve SVG files under the /svg route
@app.route('/svg/<path:filename>')
def serve_svg(filename):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(root_dir, './svg'), filename)

# Serve assets folder
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(root_dir, './assets'), filename)



@app.route('/<path:filename>.js')
def serve_js(filename):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    response = send_from_directory(os.path.join(root_dir, './js/'), f"{filename}.js")
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if users_collection.find_one({'username': {'$regex': f'^{re.escape(username)}$', '$options': 'i'}}):
        return jsonify({'message': 'Username not available'}), 400

    if users_collection.find_one({'email': {'$regex': f'^{re.escape(email)}$', '$options': 'i'}}):
        return jsonify({'message': 'Email already used'}), 400
    
    users_collection.insert_one({
        'username': username,
        'email': email,
        'password': password,
        'refresh_token': create_refresh_token(identity=username)
    })

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if email:
        user = users_collection.find_one({'email': email, 'password': password})
    elif username:
        user = users_collection.find_one({'username': username, 'password': password})
    
    if user:
        refresh_token = create_refresh_token(identity=user['username'])
        users_collection.update_one({'username': user['username']}, {'$set': {'refresh_token': refresh_token}})
        
        access_token = create_access_token(identity=user['username'])
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        print(f"Current User: {current_user}")
        new_token = create_access_token(identity=current_user)
        return jsonify({'access_token': new_token}), 200
    except Exception as e:
        print(f"Error during token refresh: {str(e)}")
        return jsonify({'message': 'Token refresh failed'}), 401
    
@app.route('/audio/<username>/<filename>', methods=['GET'])
def get_audio(username, filename):
    try:
        audio_path = f'./audio/{username}/{filename}'
        return send_file(audio_path, as_attachment=False)
    except FileNotFoundError:
        abort(404, "Audio file not found")
    except Exception as e:
        abort(500, f"An error occurred: {str(e)}")

@app.route('/get_user_audio', methods=['GET'])
@jwt_required()
def get_user_audio():
    current_user = get_jwt_identity()
    base_url = 'http://localhost:5000/audio'

    directory_path = f'./audio/{current_user}'

    try:
        files = os.listdir(directory_path)
    except FileNotFoundError:
        return jsonify({'message': 'Directory not found'}), 404

    audio_list = []

    for file in files:
        if (file.startswith('message_') or file.startswith('response_')) and file.endswith('.wav'):
            file_type = 'message' if file.startswith('message_') else 'response'

            date_str = file.split('_')[1].replace('T', ' ').replace('-', ':').replace('Z', '')[:-4]
            file_date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S:%f')

            audio_path = os.path.join(directory_path, file)

            audio_path = audio_path.replace('\\', '/')

            audio_list.append({'type': file_type, 'audio': audio_path, 'date': file_date})

    sorted_audio_list = sorted(audio_list, key=lambda x: x['date'])

    final_result = [{'type': audio['type'], 'audio': f"{base_url}/{current_user}/{os.path.basename(audio['audio'])}"}
                    for audio in sorted_audio_list]
    
    return jsonify(final_result), 200



@app.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user_data = users_collection.find_one({'username': current_user}, {'_id': 0, 'password': 0, 'refresh_token': 0})
    
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    username = request.form.get('username')

    # Check if the username is not provided
    if not username:
        return jsonify({'error': 'No username provided'}), 400
    
    #Check if the file is not provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Check if the file has a valid name
    if file.filename == '':
        return jsonify({'error': 'Empty file name'}), 400

    # Specify the directory to save the file
    upload_directory = os.path.join('audio', username)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    # Save the file to the specified directory
    file.save(os.path.join(upload_directory, file.filename))

    return jsonify({'message': 'File uploaded successfully' }), 200    

@app.route('/generate_response', methods=['GET'])
@jwt_required()
def generate_response():
    current_user = get_jwt_identity()
    try:
        filename = request.args.get('filename')
        print("filename: ",filename)
        if filename:
            transcript = transcriber.transcribe('./audio/'+current_user+'/'+filename)

        AIResponse = google_response(transcript.text)
        print("Response of GGAI: ",AIResponse)

        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S-%f')[:-3]
        new_filename = f'response_{timestamp}.wav'
        text_to_speech(AIResponse,'en', './audio/'+current_user+'/'+new_filename,'com.pk')
        
        return jsonify(success=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500   
    
def google_response(input_text):
    GOOGLE_API_KEY='AIzaSyD8WVnQjcFifsGhefjcb6qu3y2jLQy8cR0'
    
    # Configure the generative AI model
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Assuming 'gemini-pro' is a valid model name
    model = genai.GenerativeModel('gemini-pro')
    
    # Generate content based on input text
    response = model.generate_content(input_text)
    
    # Combine all chunks into a single string
    full_response = "\n".join(chunk.text for chunk in response)
    
    return full_response

def text_to_speech(text, language, filename,tld):

    tts = gTTS(text=text, lang=language,tld=tld, slow=False)
    
    tts.save(filename)
    
if __name__ == '__main__':
    app.run(debug=True)
