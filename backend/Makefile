.PHONY: build
build:
	go build -o ./build/package -v ./cmd/powerkanji

.PHONY: run
run:
	go run ./cmd/powerkanji/main.go

.PHONY: test
test:
	go test -v -timeout 10s ./..

.DEFAULT_GOAL := build
