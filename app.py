from flask import Flask, request, send_file
import io

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form method="post" action="/download">
            <input type="text" name="text">
            <input type="submit" value="Download">
        </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    text = request.form['text']
    binary_data = text.encode('utf-8')
    return send_file(
        io.BytesIO(binary_data),
        as_attachment=True,
        download_name='text.bin',
        mimetype='application/octet-stream'
    )

if __name__ == '__main__':
    app.run()
