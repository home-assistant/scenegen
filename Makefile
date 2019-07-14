## Install dependencies and install locally in the checkout

## Top-level targets

.PHONY: default
default: bin/scenegen


## Real targets that actually produce files

bin/scenegen: bin/pip requirements.txt setup.py
	bin/pip install -r requirements.txt

bin/pip:
	virtualenv -p python3 .
