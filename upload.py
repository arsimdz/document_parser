from flask import Flask, request, render_template, flash, redirect, url_for, send_file,send_from_directory
import os
from werkzeug.utils import secure_filename
from doc_parse import doc_parser, documents_to_markdown
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        save_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_location)
        flash('File successfully uploaded')
        if os.listdir(app.config['UPLOAD_FOLDER'])!=[]:
            output = doc_parser(app.config['UPLOAD_FOLDER'])
            output_file = documents_to_markdown(output)
            output_file = os.path.join('output',output_file)
            file.save(output_file)
            return redirect(url_for('download'))
            

        return redirect(url_for('upload_file'))
    return render_template('upload.html')

@app.route('/download')
def download():
   return render_template('download.html', files=os.listdir('output'))

@app.route('/download/<filename>')
def download_file(filename):
   return send_from_directory('output',path='output.md')


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)