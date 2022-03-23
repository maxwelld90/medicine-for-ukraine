node_modules/: package.json
	npm install

build/: node_modules/
	npm run-script build

start: node_modules/
	npm start

clean:
	rm -rf build
	rm -rf public/static/css
	rm -rf public/static/fonts
	rm -rf public/static/img/*.svg

clean_node:
	rm -rf node_modules