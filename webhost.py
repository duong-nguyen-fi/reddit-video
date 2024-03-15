import os
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    root_dir = os.getcwd()  # Current working directory
    return render_template('index.html', root=root_dir)

@app.route('/browse')
def browse():
    directory = request.args.get('dir', '')
    files = []
    directories = []
    if os.path.isdir(directory):
        for item in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, item)):
                files.append(item)
            else:
                directories.append(item)
    return render_template('browse.html', directory=directory, files=files, directories=directories)

@app.route('/download')
def download_file():
    filepath = request.args.get('filepath', '')
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=8080, debug=False)