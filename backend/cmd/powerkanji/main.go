package main

import (
	"flag"
	"log"
	"powerkanji/internal/api"
	"powerkanji/internal/conf"
)

var (
	configPath string
)

func init() {
	flag.StringVar(&configPath, "c", "configs/base.toml", "path to config file")
}

func main() {
	flag.Parse()

	config, err := conf.GetFromFile(configPath)
	if err != nil {
		log.Fatal(err)
	}

	srv := api.NewServer()

	if err := srv.Start(config); err != nil {
		log.Fatal(err)
	}
}
