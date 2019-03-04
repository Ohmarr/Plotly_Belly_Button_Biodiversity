# Use Plotly.js to build interactive charts for your dashboard.

# * Create a PIE chart that uses data from your samples route (`/samples/<sample>`) to display the top 10 samples.
#   * Use `sample_values` as the values for the PIE chart
#   * Use `otu_ids` as the labels for the pie chart
#   * Use `otu_labels` as the hovertext for the chart

# * Create a Bubble Chart that uses data from your samples route (`/samples/<sample>`) to display each sample.
#   * Use `otu_ids` for the x values
#   * Use `sample_values` for the y values
#   * Use `sample_values` for the marker size
#   * Use `otu_ids` for the marker colors
#   * Use `otu_labels` for the text values

# * Display the sample metadata from the route `/metadata/<sample>`

#   * Display each key/value pair from the metadata JSON object somewhere on the page

# * Update all of the plots any time that a new sample is selected.

# * You are welcome to create any layout that you would like for your dashboard. An example dashboard page might look something like the following.

import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import (
    Flask, 
    jsonify, 
    render_template)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

Base = automap_base() # reflect an existing database into a new model
Base.prepare(db.engine, reflect=True) # reflect the tables

Samples_Metadata = Base.classes.sample_metadata # Save references to each table
Samples = Base.classes.samples

# –––––––––––––––– **NOTE** –––––––––––––––––––––
# DATABASE: bellybutton
# 2 TABLES: Samples_Metadata & samples_df_filtered
#################################################
# Routes
#################################################

@app.route("/")		          # Homepage ⟶ Render
def index():
	print('success loading homepage')
	return render_template("index.html")

@app.route("/names")              # default route ⟶ Visit route; query `samples_data`
def names():		          # Return ⟶ list(JSON): sample
	query = db.\
		session.\
		query(Samples).\
		statement     # Use Pandas to perform the sql query
	print('query succesful')
	df = pd.read_sql_query(query, db.session.bind)
	print(jsonify(list(df.columns)[2:]) )
	return jsonify(list(df.columns)[2:])   

@app.route("/metadata/<sample>")  # Parameter=sample ⟶ Visit route; query `Samples_Metadata`
def sample_metadata(sample):      # Return ⟶ Metadata(JSON): sample,ETHNICITY,GENDER,AGE,LOCATION,BBTYPE,WFREQ

	sel = [ # List of deisred metadata columns
		Samples_Metadata.sample,
		Samples_Metadata.ETHNICITY,
		Samples_Metadata.GENDER,
		Samples_Metadata.AGE,
		Samples_Metadata.LOCATION,
		Samples_Metadata.BBTYPE,
		Samples_Metadata.WFREQ,
		]
	query = db.\
		session.\
		query(*sel).\
		filter(Samples_Metadata.sample == sample).\
		all() 

	sample_metadata = {}     # Dictionary to hold Json of queried data compiled in next for loop 
	for result in query:
		sample_metadata["sample"] = result[0]
		sample_metadata["ETHNICITY"] = result[1]
		sample_metadata["GENDER"] = result[2]
		sample_metadata["AGE"] = result[3]
		sample_metadata["LOCATION"] = result[4]
		sample_metadata["BBTYPE"] = result[5]
		sample_metadata["WFREQ"] = result[6]
	print(sample_metadata)
	return jsonify(sample_metadata) 

@app.route("/samples/<sample>")   # Parameter=sample ⟶ Visit route; query `sample_data`
def samples(sample):              # Return ⟶ (Json of queried data) `otu_ids`, `otu_labels`& `sample_values`

	query = db.session.query(Samples).statement
	samples_df = pd.read_sql_query(query, db.session.bind)
	# Filter samples w/ values > 1
	samples_df_filtered = samples_df.loc[samples_df[sample] > 1, ["otu_id", "otu_label", sample]]
	
	sample_data = { # (Json of queried data) `otu_ids`, `otu_labels`& `sample_values`
		"otu_ids": samples_df_filtered.otu_id.values.tolist(),
		"sample_values": samples_df_filtered[sample].values.tolist(),
		"otu_labels": samples_df_filtered.otu_label.tolist(),
		}
	return jsonify(sample_data)

if __name__ == "__main__":
    app.run()
