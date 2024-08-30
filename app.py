from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
import zipfile

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename != '':
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file_path = os.path.join('uploads', 'attendancesystem.zip')
        file.save(file_path)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall('uploads/attendancesystem')
    return redirect(url_for('index'))

# Route to start the attendance system
@app.route('/start')
def start_system():
    # Install all required packages in one command
    subprocess.call("pip install -q ultralytics gradio pandas deepface pillow opencv-python mtcnn matplotlib", shell=True)
    
    # Execute the script that handles cells 3 to 7
    exec(open("scripts/cells_3_to_7.py").read())

    return 'Attendance system started!'

# Route to end the attendance system and process results
@app.route('/end')
def end_system():
    # Execute the script that handles cell 8
    exec(open("scripts/cell_8.py").read())

    return 'Attendance processing complete!'

if __name__ == '__main__':
    app.run(debug=True)
