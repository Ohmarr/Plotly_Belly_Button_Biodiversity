function init() { 			// Visit '/names' ⟶ default route (app.py)

	var selector = d3.select("#selDataset"); // dropdown selector
	var default_url = '/names';

	d3.json(default_url).then( // Parameter=JSON list of names
		(sampleNames) => {
			sampleNames.forEach(
				(sample) => {
					selector
						.append("option") // append options for dropdown selection
						.text(sample)     // add text
						.property("value", sample);
				});
			const firstSample = sampleNames[0]; // 1st Sample
			getSampleData(firstSample)
			console.log(firstSample)
		});	   // Return ⟶ Function Calls buildCharts(firstSample) & buildMetadata(firstSample);

};			// Operations ⟶ Adds sample options to # & Returns 1 ⟶ Calls buildCharts(1) & buildMetadata(1);

function buildMetadata(newSample) { 	// display key/value pair from @ metadata route  
	// @TODO: Complete the following function that builds the metadata panel
	var selector = d3.select("#metadata_table");
	var newSample = sample;
	newSample.forEach((sample) => {
		var tableRow = selector.append("tr");
		Object.entries(stuff)
			.forEach(([key, value]) => {
				var cell = selector.append("td");
				cell.text(value);
			});
	});





	// Use `d3.json` to fetch the metadata for a sample
	// Use d3 to select the panel with id of `#sample-metadata`
	var selector = d3.select("#sample-metadata");
	// Use `.html("") to clear any existing metadata

	// Use `Object.entries` to add each key and value pair to the panel
	// Hint: Inside the loop, you will need to use d3 to append new
	// tags for each key-value in the metadata.

	// BONUS: Build the Gauge Chart
	// buildGauge(data.WFREQ);
	var default_url = `/metadata/${sample}`;

};

function buildCharts(sample) { 		// build bubble chart & pie chart for sample data

	var trace_pie = {
		values: sample.sample_values,
		labels: sample.otu_ids,
		type: 'pie'
	};
	var data_pie = [trace_pie]; //data must be an array; so converted here; 
	var layout_pie = {
		title: "'Pie' Chart - Samples",
		height: 400,
		width: 500
	};
	Plotly.newPlot('pie', data_pie, layout_pie); // pie chart
};
// @TODO: Use `d3.json` to fetch the sample data for the plots

// @TODO: Build a Bubble Chart using the sample data

// @TODO: Build a Pie Chart
// HINT: You will need to use slice() to grab the top 10 sample_values,
// otu_ids, and labels (10 each).


function getSampleData(newSample) {	//  Dropdown Change ⟶ New Sample Selected
	d3.json(`/metadata/${newSample}`)
		.then(
			(newMetadata) => {
				buildMetadata(newMetadata)
				console.log(`calling buildMetadata() on ${newMetadata}`)
			})

	d3.json(`/samples/${newSample}`)
		.then(
			(new_sampledata) => {
				buildCharts(new_sampledata)
				console.log(`calling buildCharts(${new_sampledata})`)
			})
}; 	// Return ⟶ function calls ⟶ buildCharts(newSample) & buildMetadata(newSample);

init();					// Return ⟶ Function Call init()
