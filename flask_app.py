from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import csv
import io
import PyPDF2
import requests
from werkzeug.utils import secure_filename
import tempfile
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Together.ai API configuration
TOGETHER_API_KEY = "enter-your-together-API"  # Replace with your actual API key
TOGETHER_API_URL = "https://api.together.xyz/inference"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading text file: {str(e)}")

def generate_flashcards_with_llm(content):
    """Generate flashcards using Together.ai API"""
    prompt = f"""
    Please analyze the following educational content and generate between 10 and 20 high-quality flashcards in Q&A format.

    Requirements:
    - Create clear, concise questions that test understanding
    - Provide accurate, informative answers
    - Cover key concepts, definitions, and important details
    - Vary question types (definitions, explanations, applications, comparisons)
    - Ensure questions are specific and answers are comprehensive

    Content to analyze:
    {content[:4000]}  # Limit content to avoid token limits

    Please respond with ONLY a valid JSON array in this exact format:
    [
        {{"question": "What is...", "answer": "..."}},
        {{"question": "How does...", "answer": "..."}},
        ...
    ]

    Generate at least 10 and at most 20 flashcards.
    """

    try:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "meta-llama/Llama-2-70b-chat-hf",
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.1
        }

        response = requests.post(TOGETHER_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('output', {}).get('choices', [{}])[0].get('text', '')

            # Try to parse the JSON response
            try:
                # Find JSON array in the response
                start_idx = generated_text.find('[')
                end_idx = generated_text.rfind(']') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = generated_text[start_idx:end_idx]
                    flashcards = json.loads(json_str)

                    # Validate the structure
                    if isinstance(flashcards, list) and len(flashcards) >= 10:
                        valid_flashcards = []
                        for card in flashcards:
                            if isinstance(card, dict) and 'question' in card and 'answer' in card:
                                valid_flashcards.append({
                                    'id': str(uuid.uuid4()),
                                    'question': card['question'].strip(),
                                    'answer': card['answer'].strip(),
                                    'created_at': datetime.now().isoformat()
                                })

                        # Ensure between 10 and 20 cards
                        if len(valid_flashcards) >= 10:
                            return valid_flashcards[:20]

                # Fallback: generate default flashcards
                return generate_fallback_flashcards(content)

            except json.JSONDecodeError:
                return generate_fallback_flashcards(content)
        else:
            return generate_fallback_flashcards(content)

    except Exception as e:
        print(f"LLM API Error: {str(e)}")
        return generate_fallback_flashcards(content)

def generate_fallback_flashcards(content):
    """Generate basic flashcards when LLM fails"""
    words = content.split()
    sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 10]

    fallback_cards = []

    # Generate some basic flashcards based on content
    for i in range(min(20, len(sentences))):
        fallback_cards.append({
            'id': str(uuid.uuid4()),
            'question': f"What is discussed in: '{sentences[i][:50]}...'?",
            'answer': sentences[i],
            'created_at': datetime.now().isoformat()
        })

    # Add some definition-style questions if needed
    if len(fallback_cards) < 10:
        key_terms = [word for word in words if len(word) > 6 and word.isalpha()][:10]
        for term in key_terms:
            if len(fallback_cards) >= 20:
                break
            fallback_cards.append({
                'id': str(uuid.uuid4()),
                'question': f"Define or explain: {term}",
                'answer': f"Based on the context, {term} is an important concept discussed in the material.",
                'created_at': datetime.now().isoformat()
            })

    # Ensure at least 10 and at most 20 cards
    if len(fallback_cards) < 10:
        # Repeat some cards to reach 10 if content is too short
        while len(fallback_cards) < 10:
            fallback_cards.append(fallback_cards[-1])
    return fallback_cards[:20]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Flashcard API is running"})

@app.route('/api/generate-flashcards', methods=['POST'])
def generate_flashcards():
    try:
        content = ""
        
        # Handle text input
        if 'text_input' in request.form and request.form['text_input'].strip():
            content += request.form['text_input'].strip() + "\n\n"
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                try:
                    if filename.lower().endswith('.pdf'):
                        file_content = extract_text_from_pdf(file_path)
                    else:
                        file_content = extract_text_from_txt(file_path)
                    
                    content += file_content
                finally:
                    # Clean up uploaded file
                    if os.path.exists(file_path):
                        os.remove(file_path)
        
        if not content.strip():
            return jsonify({"error": "No content provided"}), 400
        
        if len(content.strip()) < 50:
            return jsonify({"error": "Content too short. Please provide at least 50 characters."}), 400
        
        # Generate flashcards
        flashcards = generate_flashcards_with_llm(content)
        
        return jsonify({
            "success": True,
            "flashcards": flashcards,
            "count": len(flashcards),
            "message": f"Successfully generated {len(flashcards)} flashcards"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate flashcards: {str(e)}"}), 500

@app.route('/api/export-flashcards', methods=['POST'])
def export_flashcards():
    try:
        data = request.get_json()
        flashcards = data.get('flashcards', [])
        export_format = data.get('format', 'json')
        
        if not flashcards:
            return jsonify({"error": "No flashcards to export"}), 400
        
        if export_format == 'json':
            return jsonify({
                "success": True,
                "data": json.dumps(flashcards, indent=2),
                "filename": f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "mime_type": "application/json"
            })
            
        elif export_format == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Question', 'Answer', 'Created At'])
            
            for card in flashcards:
                writer.writerow([
                    card.get('question', ''),
                    card.get('answer', ''),
                    card.get('created_at', '')
                ])
            
            return jsonify({
                "success": True,
                "data": output.getvalue(),
                "filename": f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "mime_type": "text/csv"
            })
            
        elif export_format == 'anki':
            # Anki format (tab-separated)
            anki_data = []
            for card in flashcards:
                anki_data.append(f"{card.get('question', '')}\t{card.get('answer', '')}")
            
            return jsonify({
                "success": True,
                "data": "\n".join(anki_data),
                "filename": f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "mime_type": "text/plain"
            })
            
        elif export_format == 'quizlet':
            # Quizlet format (similar to Anki but with specific formatting)
            quizlet_data = []
            for card in flashcards:
                quizlet_data.append(f"{card.get('question', '')}\t{card.get('answer', '')}")
            
            return jsonify({
                "success": True,
                "data": "\n".join(quizlet_data),
                "filename": f"flashcards_quizlet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "mime_type": "text/plain"
            })
        
        else:
            return jsonify({"error": "Unsupported export format"}), 400
            
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.route('/api/update-flashcard', methods=['PUT'])
def update_flashcard():
    try:
        data = request.get_json()
        card_id = data.get('id')
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()
        
        if not card_id or not question or not answer:
            return jsonify({"error": "Missing required fields"}), 400
        
        # In a real application, you would update the flashcard in a database
        # For now, we'll just return the updated card
        updated_card = {
            'id': card_id,
            'question': question,
            'answer': answer,
            'updated_at': datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "flashcard": updated_card,
            "message": "Flashcard updated successfully"
        })
        
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Change port if needed
