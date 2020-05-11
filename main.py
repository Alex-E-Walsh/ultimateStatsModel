import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from tensorflow.keras.models import load_model

app = Flask(__name__)
lr_model = pickle.load(open('AUDL_linear_model.pkl','rb'))
clf_model = load_model('ANN_classifier_82.h5')

fts = pd.read_csv('AUDL_team_stats.csv')
fts.set_index('team',inplace=True)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    #get user inputs
    features = [str(x) for x in request.form.values()]
    home = features[1]+features[0]
    away = features[3]+features[2]
    model = features[4]
    #fetch respective data from csv
    home_stat = np.array(fts.loc[home])
    away_stat = np.array(fts.loc[away])
    game_stat = np.append(home_stat,away_stat).reshape(1,38)
    matchup = home + ' (H) VS. '+ away + ' (A)'


    if model == "lr":
        pred = float(lr_model.predict(game_stat)[0])
        intScore = int(pred)

        if pred < 0:
            outcome_str = away+' (A) wins by a margin of '+str(abs(intScore)) +' goals'
        if intScore == 0:
            if pred > 0:
                outcome_str = "It's a tie! Slight advantage "+ home
            else:
                outcome_str = "It's a tie! Slight advantage "+ away
        else:
            outcome_str = home+' (H) wins by a margin of '+str(intScore) +' goals'

    elif model == "clf":
        pred = float(clf_model.predict_proba(game_stat).reshape(-1)[0])
        if pred < .5:
            outcome_str = str(100-round(pred*100,3)) + "%  chance "+away+'(A) wins'
        else:
            outcome_str = str(round(pred*100,3)) + "%  chance "+home+'(H) wins'

    return render_template('index.html',prediction_text=(outcome_str),matchup = matchup)

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    # prediction = model.predict([np.array(list(data.values()))])

    return jsonify(data)

#     fts = pd.read_csv('teamStats.csv')
#
#     home_stat = np.array(fts.loc[home])
#     away_stat = np.array(fts.loc[away])
#     game_stat = np.append(home_stat,away_stat).reshape(1,38)
#
#
# def predict_game_score(home,away):
#     #open linear regression model
#     with open('AUDL_linear_model','rb') as f:
#         mdl = pickle.load(f)
#     #fetch team stats
#     home_stat = np.array(fts.loc[home])
#     away_stat = np.array(fts.loc[away])
#     game_stat = np.append(home_stat,away_stat).reshape(1,38)
#
#     pred = int(mdl.predict(game_stat)[0])
#
#     outcome_str = home+' wins by a margin of '+str(pred)
#
#     if pred < 0:
#         outcome_str = away+' wins by a margin of '+str(abs(pred))
#
#     return outcome_str

if __name__ =="__main__":
    app.run(debug=True)
