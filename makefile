# Makefile
IMAGES = ghcr.io/osgeo/gdal:ubuntu-small-3.9.0 ghcr.io/osgeo/gdal:ubuntu-small-3.8.0

.PHONY: all build stop run logs

all:
	@for image in $(IMAGES); do \
		echo "\n=============================="; \
		echo "Using base image: $$image"; \
		echo "=============================="; \
		$(MAKE) build BASE_IMAGE=$$image; \
		$(MAKE) stop; \
		$(MAKE) run; \
		$(MAKE) logs; \
	done

build:
	@docker build . --file Dockerfile --build-arg BASE_IMAGE=$(BASE_IMAGE) -t bscholer/gdalwarp-testing:$(subst /,_,$(subst :,_,${BASE_IMAGE})) > /dev/null

stop:
	-@docker stop gdalwarp-testing > /dev/null 2>&1
	-@docker rm gdalwarp-testing > /dev/null 2>&1

run:
	@docker run -it -d -v ./data:/data --name gdalwarp-testing bscholer/gdalwarp-testing

exec:
	@docker exec -it gdalwarp-testing /bin/bash

logs:
	@docker logs --follow gdalwarp-testing

publish:
	@docker push bscholer/gdalwarp-testing