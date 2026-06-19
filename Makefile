.PHONY: reproduce test sweep thresholds decoherence anesthesia

reproduce:
	python3 examples/quick_reproduce.py

test:
	PYTHONPATH=src python3 -m unittest discover -s tests

sweep:
	PYTHONPATH=src python3 -m orch_or sweep --output examples/output/collapse_time_table.csv

thresholds:
	PYTHONPATH=src python3 -m orch_or thresholds --output examples/output/dp_threshold_table.csv

decoherence:
	PYTHONPATH=src python3 -m orch_or decoherence --output examples/output/decoherence_estimate_table.csv

anesthesia:
	PYTHONPATH=src python3 -m orch_or anesthesia --output examples/output/anesthesia_prediction_table.csv
