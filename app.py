from flask import Flask, request, send_file, render_template
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/constructor')
def constructor():
    return render_template('constructor.html')

@app.route('/download', methods=['POST'])
def download():
    texts = request.form.getlist('text')
    combined_text = '\n'.join(texts)
    binary_data = combined_text.encode('utf-8')
    return send_file(
        io.BytesIO(binary_data),
        as_attachment=True,
        download_name='text.bin',
        mimetype='application/octet-stream'
    )

if __name__ == '__main__':
    app.run()
