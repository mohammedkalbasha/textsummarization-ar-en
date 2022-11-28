import pickle
import json
from flask import Flask, jsonify, request
from functions import fetch_data, summarize_category

app = Flask(__name__)
text_summary = 'Text'
text_category = 'category'

@app.route('/')
def index():
    return "mohammed albasha & abdalrahman Shahror"

#scraping websites and analyze text
@app.route("/analyze_url", methods=['GET', 'POST'])
def analyze_url():
    jsonData = '{"text_summary_URL_json": "Text_URL","text_category_URL_json": "Category_URL"}'
    data = json.loads(jsonData)
    data = dict()
    if request.method == 'POST':
        input_language = request.form['url_language']
        input_url = request.form['url_input_text']
        input_text = fetch_data(input_url)
        classifier_model_name = request.form['url_classifier']
        sentences_number = request.form['url_sentences_number']
        global text_summary , text_category

        if input_language == 'english':
            classifier_model = pickle.load(open('Model/en_model/en_' + classifier_model_name + '.pkl', 'rb'))
            text_summary, text_category = summarize_category(input_text, sentences_number, classifier_model, False)
        else:
            classifier_model = pickle.load(open('Model/ar_model/ar_' + classifier_model_name + '.pkl', 'rb'))
            text_summary, text_category = summarize_category(input_text, sentences_number, classifier_model, True)
            
    data['text_summary_URL_json'] = text_summary
    data['text_category_URL_json'] = text_category
    return jsonify(data)


#analyze text
@app.route("/analyze_text", methods=['GET', 'POST'])
def analyze_text():
    jsonData = '{"text_summary_json": "Text","text_category_json": "Category"}'
    data = json.loads(jsonData)
    data = dict()

    if request.method == 'POST':
        input_text = request.form['text_input_text']
        sentences_number = request.form['text_sentences_number']
        classifier_model_name = request.form['text_classifier']
        input_language = request.form['text_language']
        global text_summary , text_category

        if input_language == 'english':
            classifier_model = pickle.load(open('Model/en_model/en_' + classifier_model_name + '.pkl', 'rb'))
            text_summary, text_category = summarize_category(input_text, sentences_number, classifier_model, False)
        else:
            classifier_model = pickle.load(open('Model/ar_model/ar_' + classifier_model_name + '.pkl', 'rb'))
            text_summary, text_category = summarize_category(input_text, sentences_number, classifier_model, True)
            
    data['text_summary_json'] = text_summary
    data['text_category_json'] = text_category
    return jsonify(data)

    
if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0')