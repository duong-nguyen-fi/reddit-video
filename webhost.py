import os
from flask import Flask, render_template, request, send_file
import subprocess
import threading
import time
import toml


app = Flask(__name__)

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

def process_docker():
    # Trigger docker process
    command = "docker run --rm -v /home/andy/repo/reddit-video:/app reddit-video:1.3"
    subprocess.run(command, shell=True)

    # Wait for docker process to complete
    time.sleep(1200)  # Assuming 20 minutes processing time

    # Check if results file is created
    if os.path.exists("results/processed_file.txt"):
        return "Processing succeeded!"
    else:
        return "Processing failed!"


def update_config(subreddit, post_id):
    config_path = 'config.toml'
    if not os.path.exists(config_path):
        return "Config file not found."

    with open(config_path, 'r') as f:
        config = toml.load(f)

    reddit_config = config.get('reddit')
    if not reddit_config:
        return "reddit configuration not found in the config file."

    thread_config = reddit_config.get('thread')
    if not thread_config:
        reddit_config['thread'] = {}

    reddit_config['thread']['subreddit'] = subreddit
    reddit_config['thread']['post_id'] = post_id

    with open(config_path, 'w') as f:
        toml.dump(config, f)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subreddit = request.form['subreddit']
        post_id = request.form['post_id']

        # Update config.toml
        update_config(subreddit, post_id)

        # Start docker process in a separate thread
        docker_thread = threading.Thread(target=process_docker)
        docker_thread.start()

        return render_template('index.html', message="Processing started! Please wait.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=8080, debug=False)



