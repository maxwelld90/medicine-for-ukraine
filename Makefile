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

virtualenvs/api: api/requirements.txt
	mkdir -p virtualenvs/api; \
	virtualenv -p $(PYTHON) virtualenvs/api; \
	. virtualenvs/api/bin/activate; \
	pip install -Ur api/requirements.txt;

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

.BUILD_SUCCESS:
	./build_final.sh;
	touch .BUILD_SUCCESS;
.PHONY: .BUILD_SUCCESS

all: virtualenvs/landing virtualenvs/api landing/out front/build landing/out/request .BUILD_SUCCESS
#all: virtualenvs/landing virtualenvs/api landing/out front/node_modules front/build landing/out/request .BUILD_SUCCESS

server-api:
	. virtualenvs/api/bin/activate; \
	cd api; \
	$(PYTHON) manage.py runserver 0.0.0.0:8001;
.PHONY: server-api

server-landing:
	cd landing/out; \
	echo "Access http://127.0.0.1:8000/ for the frontend server."; \
	$(PYTHON) -m http.server 8000;
.PHONY: server-landing

devserver: all
	make -j 2 server-api server-landing;
.PHONY: devserver

clean:
	rm -rf virtualenvs
	rm -rf landing/out
	rm -rf front/build
	rm -rf front/public/static/css
	rm -rf front/public/static/fonts
	rm -rf front/public/static/img/*.svg
	rm front/src/LANGUAGES.json
	rm .BUILD_SUCCESS
#rm -rf front/node_modules