import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import tensorflow as tf
from tensorflow import keras


app = Flask(__name__)

clf_model = tf.keras.models.load_model('models/h5_models(AUDL)/ANN_classifier_82.h5')
rfe_model =  tf.keras.models.load_model('models/h5_models(AUDL)/audl_rfe.h5')
# lr_model = pickle.load(open('models/h5_models(AUDL)/AUDL_linear_model.pkl','rb'))

fts = pd.read_csv('models/AUDL_team_stats.csv')
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

    #make home + away stats compatible
    rhome = pd.Series(fts.loc[home]).array

    raway = pd.Series(fts.loc[away]).array

    if model == "lr":
        pred = float(lr_model.predict(game_stat)[0])
        intScore = int(pred)

        if pred < 0:
            outcome_str = features[3]+' \''+featues[2] +' (A) wins by a margin of '+str(abs(intScore)) +' goals'
        else:
            outcome_str = features[1]+' \''+features[0]+' (H) wins by a margin of '+str(intScore) +' goals'
        if intScore == 0:
            if pred > 0:
                outcome_str = "It's a tie! Slight advantage "+ features[1]+' \''+features[0]
            else:
                outcome_str = "It's a tie! Slight advantage "+features[3]+' \''+features[2]


    elif model=="rfe":
        home_cols = ['W', 'L', 'PPG', 'PAPG', 'PM', 'BPG', 'CMP', 'CPG','TPG']
        h_stat = fts.loc[home].loc[home_cols]
        away_cols = ['G', 'W', 'L', 'PPG', 'PAPG', 'OEFF', 'DEFF','PMPG', 'BLK', 'BPG', 'CMP', 'CPG', 'CMPR', 'TO','TPG']
        a_stat = fts.loc[away].loc[away_cols]

        f_inp = np.array(h_stat.append(a_stat)).reshape(-1,24)

        pred = float(rfe_model.predict_proba(f_inp).reshape(-1)[0])

        if pred < .5:
            outcome_str = str(100-round(pred*100,3)) + "% chance "+features[3]+' \''+features[2] +' wins'
        else:
            outcome_str = str(round(pred*100,4)) + " % chance "+features[1]+' \''+features[0]+' wins'


    elif model == "clf":
        pred = float(clf_model.predict_proba(game_stat).reshape(-1)[0])
        if pred < .5:
            outcome_str = str(100-round(pred*100,3)) + "%  chance "+features[3]+' \''+features[2] +'(A) wins'
        else:
            outcome_str = str(round(pred*100,3)) + "%  chance "+features[1]+' \''+features[0]+'(H) wins'

    return render_template('index.html',prediction_text=(outcome_str),matchup = matchup, home_stat=rhome,away_stat=raway)

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)

    return jsonify(data)


if __name__ =="__main__":
    app.run(debug=True)
