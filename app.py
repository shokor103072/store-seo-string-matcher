import pandas as pd
from flask import Flask, request, app, jsonify, url_for, render_template
import pickle
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)
Data_description = pd.read_pickle(r'Data_description.pkl')


@app.route('/')
def home():
    return str('Thank you')


@app.route('/predict', methods=['GET'])
def predict():
    text = request.args.get('text')
    specific_sent = re.sub('[^A-Za-z0-9]+', '',
                           re.sub('\s\s+|\n|\n+', '', re.sub('<[^>]*>', '', text)))
    if len(specific_sent) == 0:
        result = 0
    else:
        try:
            Data_description['search'] = Data_description['description'].str.contains(specific_sent, case=False)
            search_data = Data_description[Data_description['search'] == True]
            result = process.extractOne(specific_sent, search_data['description'], scorer=fuzz.ratio)[1]
        except:
            result = 0
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
