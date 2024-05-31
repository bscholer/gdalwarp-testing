target: build stop run logs

build:
	docker build . --file Dockerfile -t bscholer/gdalwarp-testing

stop:
	- docker stop gdalwarp-testing
	- docker rm gdalwarp-testing

run:
	docker run -it -d -v ./data:/data --name gdalwarp-testing bscholer/gdalwarp-testing

exec:
	docker exec -it gdalwarp-testing /bin/bash

logs:
	docker logs --follow gdalwarp-testing

publish:
	docker push bscholer/gdalwarp-testing
