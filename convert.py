from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_docx_to_pdf():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400

    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    if file_ext != "docx":
        return {"error": "Only .docx files are supported"}, 400

    file_id = str(uuid.uuid4())
    docx_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
    pdf_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.pdf")

    file.save(docx_path)

    try:
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", OUTPUT_FOLDER], check=True)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        os.remove(docx_path)
        os.remove(pdf_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
