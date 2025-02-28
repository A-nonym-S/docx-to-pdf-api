from flask import Flask, request, send_file, jsonify
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "DOCX to PDF API is running!"})

@app.route('/convert', methods=['POST'])
def convert_docx_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    if file_ext != "docx":
        return jsonify({"error": "Only .docx files are supported"}), 400

    file_id = str(uuid.uuid4())
    docx_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
    pdf_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.pdf")

    file.save(docx_path)

    try:
        result = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", OUTPUT_FOLDER],
            check=True, capture_output=True, text=True
        )
        print("LibreOffice Output:", result.stdout)

        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF conversion failed"}), 500

        return send_file(pdf_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        print("LibreOffice Error:", e.stderr)
        return jsonify({"error": "Conversion process failed"}), 500

    finally:
        os.remove(docx_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

