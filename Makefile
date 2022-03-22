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

# all: virtualenvs/landing landing/out front/node_modules front/build landing/out/request
all: virtualenvs/landing landing/out front/build landing/out/request

devserver: all
	. virtualenvs/landing/bin/activate; \
	cd landing; \
	make devserver;

clean:
	rm -rf virtualenvs
	rm -rf landing/out
	rm -rf front/build
#	rm -rf front/node_modules