.PHONY: sample database serve check

sample:
	python3 download_data.py --sample
	python3 clean_data.py --sample
	python3 merge_datasets.py --sample

database: sample
	python3 build_database.py

serve:
	python3 -m http.server 8000 --directory web

check:
	python3 -m compileall -q src *.py

