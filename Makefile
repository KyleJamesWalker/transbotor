build_loc ?= $(shell pwd)

build:
	docker build -t tbot $(build_loc)

run:
	docker run -it --rm -v $(build_loc):/code tbot
