from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FEATURES = ['n','p','k','temperature','humidity','ph','rainfall']
DATASET = Path(__file__).resolve().parent.parent / 'data' / 'crop_recommendation.csv'

class PrecisionFarmingEngine:
    """Random Forest crop ranking plus transparent prototype rules for fertilizer and irrigation."""
    def __init__(self):
        if DATASET.exists():
            df = pd.read_csv(DATASET)
            df.columns = [str(c).strip().lower() for c in df.columns]
            label = 'label' if 'label' in df.columns else 'crop'
            missing = [c for c in FEATURES + [label] if c not in df.columns]
            if missing:
                raise ValueError(f'Dataset missing columns: {missing}')
            X, y = df[FEATURES].astype(float), df[label].astype(str)
            self.demo_mode = False
        else:
            X, y = self._demo_data()
            self.demo_mode = True
        self.model = RandomForestClassifier(n_estimators=250, random_state=42, class_weight='balanced')
        self.model.fit(X[FEATURES], y)

    def _demo_data(self):
        centers = {
            'rice':[90,42,43,25,82,6.0,210], 'maize':[78,48,20,23,65,6.1,90],
            'cotton':[110,40,20,28,65,6.5,85], 'wheat':[75,45,35,20,60,6.5,75],
            'chickpea':[40,65,80,20,45,6.8,65], 'tomato':[100,55,45,24,70,6.2,120],
            'potato':[75,55,50,19,75,5.8,95], 'groundnut':[35,45,25,27,60,6.2,80],
            'banana':[100,75,50,27,80,6.2,160], 'mungbean':[20,45,20,28,60,6.8,55]
        }
        rng = np.random.default_rng(42); rows=[]; labels=[]
        for crop, center in centers.items():
            for _ in range(80):
                rows.append(np.array(center) + rng.normal(0,[12,8,10,2.5,7,.35,20]))
                labels.append(crop)
        return pd.DataFrame(rows, columns=FEATURES), pd.Series(labels)

    def recommend(self, v, soil_type, growth_stage):
        row = pd.DataFrame([{'n':v['N'],'p':v['P'],'k':v['K'],'temperature':v['temperature'],
            'humidity':v['humidity'],'ph':v['ph'],'rainfall':v['rainfall']}], columns=FEATURES)
        probs = self.model.predict_proba(row)[0]
        order = np.argsort(probs)[::-1][:3]
        ranking = [{'crop':str(self.model.classes_[i]).title(),'score':round(float(probs[i])*100,1)} for i in order]
        crop = ranking[0]['crop'].lower()
        # NPK figures are illustrative target values, not a fertilizer prescription.
        targets = {'rice':(100,50,50),'maize':(120,60,40),'cotton':(120,50,50),'wheat':(100,50,40),
                   'chickpea':(40,60,50),'tomato':(110,70,80),'potato':(100,60,100),'groundnut':(40,50,60),
                   'banana':(120,60,100),'mungbean':(25,50,25)}
        target = targets.get(crop,(80,50,50)); deficits=[]
        for name, actual, goal in zip(['Nitrogen (N)','Phosphorus (P)','Potassium (K)'],[v['N'],v['P'],v['K']],target):
            if goal-actual > 10: deficits.append(f'{name} appears below the prototype target by about {goal-actual:.0f} units')
        fertilizer = ('; '.join(deficits) + '. Confirm nutrient levels and application rates with a soil test/local agronomist.' if deficits else
            'No large NPK gap detected by the prototype rules. Use soil-test-guided maintenance fertilization.')
        if v['rainfall'] >= 20:
            irrigation = {'status':'Delay','advice':'Delay watering and reassess soil moisture after rainfall.','reason':'Recent rainfall input is elevated in this prototype rule set.','next_check':'6–12 hours'}
        elif v['soil_moisture'] < 30 and v['temperature'] >= 30:
            irrigation = {'status':'High priority','advice':'Consider irrigation soon, then recheck soil moisture.','reason':'Low moisture combined with high temperature can increase crop water stress.','next_check':'2–4 hours'}
        elif v['soil_moisture'] < 45:
            irrigation = {'status':'Moderate','advice':'Plan irrigation in the next cycle and avoid overwatering.','reason':'Moisture is below the prototype threshold.','next_check':'6–8 hours'}
        else:
            irrigation = {'status':'Low','advice':'No immediate irrigation indicated by this rule. Continue monitoring moisture.','reason':'Current moisture input is above the prototype threshold.','next_check':'12–24 hours'}
        return {'crop':ranking[0]['crop'],'confidence':ranking[0]['score'],'ranking':ranking,
            'fertilizer':fertilizer,'irrigation':irrigation,'soil_type':soil_type,'growth_stage':growth_stage,
            'model_note':'Demo training data is being used. Add the Kaggle CSV for dataset-based recommendations.' if self.demo_mode else 'Model trained using the supplied crop dataset.'}
