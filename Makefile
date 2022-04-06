BASEDIR=$(CURDIR)
APIDIR=$(BASEDIR)/api
FRONTDIR=$(BASEDIR)/front
LANDINGDIR=$(BASEDIR)/landing
PYTHON=python3.8

virtualenvs/landing: landing/requirements.txt
	mkdir -p virtualenvs/landing; \
	virtualenv -p $(PYTHON) virtualenvs/landing; \
	. virtualenvs/landing/bin/activate; \
	pip install -Ur landing/requirements.txt;

landing/out: virtualenvs/landing
	. virtualenvs/landing/bin/activate; \
	cd landing; \
	make clean; \
	make html;

front/node_modules: front/package.json
	cd front; \
	npm install;

front/build: # front/node_modules
	cd front; \
	npm run-script build;

landing/out/request: front/build
	mkdir landing/out/request; \
	cp -r front/build/* landing/out/request; \
	rsync -a landing/out/request/static landing/out;
	rm -rf landing/out/request/static/; \
	mv landing/out/request/asset-manifest.json landing/out; \
	mv landing/out/request/manifest.json landing/out;

all: virtualenvs/landing landing/out front/node_modules front/build landing/out/request

devserver: all
	. virtualenvs/landing/bin/activate; \
	cd landing/out; \
	$(PYTHON) -m http.server 8000;

clean:
	rm -rf virtualenvs
	rm -rf landing/out
	rm -rf front/build
	rm -rf front/public/static/css
	rm -rf front/public/static/fonts
	rm -rf front/public/static/img/*.svg
	rm front/src/LANGUAGES.json
	rm -rf front/node_modules