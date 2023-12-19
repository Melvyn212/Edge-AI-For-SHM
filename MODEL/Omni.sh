#! bin/bash

git clone https://github.com/smallcowbaby/OmniAnomaly && cd OmniAnomaly

wget https://s3-us-west-2.amazonaws.com/telemanom/data.zip && unzip data.zip && rm data.zip

cd data && wget https://raw.githubusercontent.com/khundman/telemanom/master/labeled_anomalies.csv

pip install -r requirements.txt

python data_preprocess.py <dataset>

## where <dataset> is one of SMAP, MSL or SMD.

python main.py
