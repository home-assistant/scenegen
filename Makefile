## Install dependencies and install locally in the checkout

# Option variables, override by invoking like `make VAR=foo target`
URL=http://localhost:8123
EXPORT_SCENE_DIR=..
# This is a very conservative default, taken as a multiple of the 10 seconds
# from the below after testing locally:
# https://developers.home-assistant.io/docs/en/external_api_rest.html#post-api-services-lt-domain-lt-service
EXPORT_SLEEP=20


## Top-level targets

.PHONY: default
default: bin/scenegen


## Real targets that actually produce files

bin/scenegen: bin/pip requirements.txt setup.py
	bin/pip install -r requirements.txt

bin/pip:
	virtualenv -p python3 .


## Optional auto-generating scenes for any existing scenes:
##   Useful for "exporting" scenes from an integration, such as SmartThings,
##   to native Home Assistant themes.

.PHONY: export
export: default
	$(MAKE) EXPORT_ALL_SCENES="$(EXPORT_ALL_SCENES)" \
		$(EXPORT_SCENE_DIR)/.scenes
	$(MAKE) SCENES="$$(cat $(EXPORT_SCENE_DIR)/.scenes)" export-scenes

# Phase 1: maybe get all the scenes
ifdef EXPORT_ALL_SCENES
.PHONY: $(EXPORT_SCENE_DIR)/.scenes
$(EXPORT_SCENE_DIR)/.scenes:
	bin/list-scenes -t "$(TOKEN)" "$(URL)" >"$(@)"
endif

# Phase 2: Export the scenes
ifdef SCENES
SCENE_YAML_FILES = $(SCENES:%=$(EXPORT_SCENE_DIR)/%.yaml)
endif

.PHONY: export-scenes
export-scenes: $(SCENE_YAML_FILES)

$(SCENE_YAML_FILES): default
	curl -f -X POST --oauth2-bearer "$(TOKEN)" \
	       -H "Content-Type: application/json" \
	       -d '{"entity_id": "group.all_lights"}' \
	       "$(URL)/api/services/homeassistant/turn_off"
	curl -f -X POST --oauth2-bearer "$(TOKEN)" \
	       -H "Content-Type: application/json" \
	       -d '{"entity_id": "group.all_switches"}' \
	       "$(URL)/api/services/homeassistant/turn_off"
	sleep $(EXPORT_SLEEP)
	curl -f -X POST --oauth2-bearer "$(TOKEN)" \
	       -H "Content-Type: application/json" \
	       -d '{"entity_id": "scene.$(@:$(EXPORT_SCENE_DIR)/%.yaml=%)"}' \
	       "$(URL)/api/services/scene/turn_on"
	sleep $(EXPORT_SLEEP)
	bin/scenegen -k "$(TOKEN)" -s "$(shell bin/python -c 'print("$(@:$(EXPORT_SCENE_DIR)/%.yaml=%)".replace("_", " ").title())')" "$(URL)" >"$(@)"
