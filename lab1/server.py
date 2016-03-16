from flask import Flask, render_template, request

from src.identifiers import LanguageIdentifier

identifier = LanguageIdentifier(statistics_dir='statistics')
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home():
    global identifier
    ctx = {}

    if request.method == 'POST':
        statistics = []
        text_to_identify = request.form['text_to_identify']
        for n in range(2, 11):
            distances, language = identifier.identify(text_to_identify, n)
            statistics.append({'language': language, 'distances': distances})
        ctx.update({'statistics': statistics, 'text_to_identify': text_to_identify})

    return render_template('index.html', **ctx)

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=80)
