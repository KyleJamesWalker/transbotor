build_loc ?= $(shell pwd)

build:
	docker build -t tbot $(build_loc)

run:
	docker run -it --rm -v $(build_loc):/code tbot

create:
	docker create --name transbotor --restart=on-failure:5 -v $(build_loc):/code tbot

start:
	docker start transbotor
