from flask import Flask, render_template, request

from lab1.src.identifiers import LanguageIdentifier
from lab2.src.engine import CorrectionEngine

identifier = LanguageIdentifier(statistics_dir='lab1/statistics')
correction_engine = CorrectionEngine(forms_file='lab2/forms/formy.txt')
app = Flask(__name__)

# TODO: change to websockets

@app.route("/lab1", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def lab1():
    global identifier
    ctx = {}

    if request.method == 'POST':
        statistics = []
        text_to_identify = request.form['text_to_identify']
        for n in range(2, 11):
            distances, language = identifier.identify(text_to_identify, n)
            statistics.append({'language': language, 'distances': distances})
        ctx.update({'statistics': statistics, 'text_to_identify': text_to_identify})

    return render_template('lab1.html', **ctx)


@app.route("/lab2", methods=['POST', 'GET'])
def lab2():
    global correction_engine
    ctx = {}

    if request.method == 'POST':
        text_to_correct = request.form['text_to_correct']
        corrected_text = correction_engine.correct_text(text_to_correct)
        ctx.update({'corrected_text': corrected_text, 'text_to_correct': text_to_correct})

    return render_template('lab2.html', **ctx)


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=80)
