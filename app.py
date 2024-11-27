import os
import shutil
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Function to organize files based on extensions
def organize_files(directory):
    # Define file type categories
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Text': ['.txt', '.pdf', '.docx', '.xlsx'],
        'Audio': ['.mp3', '.wav', '.aac'],
        'Videos': ['.mp4', '.avi', '.mkv'],
        'Archives': ['.zip', '.tar', '.gz']
    }
    
    # Ensure the main directory exists
    if not os.path.exists(directory):
        return "Directory does not exist."
    
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            for folder, extensions in file_types.items():
                if file_ext in extensions:
                    folder_path = os.path.join(directory, folder)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    shutil.move(file_path, os.path.join(folder_path, filename))
                    break
    return "Files organized successfully."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        folder_path = request.form['folder_path']
        result = organize_files(folder_path)
        return render_template('index.html', result=result)
    return render_template('index.html', result='')

if __name__ == '__main__':
    app.run(debug=True)