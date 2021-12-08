package api

import (
	"net/http"
	"powerkanji/internal/api/handlers"
	"powerkanji/internal/conf"

	"github.com/gorilla/mux"
	"github.com/sirupsen/logrus"
)

type server struct {
	router *mux.Router
	logger *logrus.Logger
}

func NewServer() *server {
	s := &server{
		router: mux.NewRouter(),
		logger: logrus.New(),
	}

	s.router.HandleFunc("/", handlers.HandleKanjiList).Methods("GET")

	return s
}

func (s *server) ServeHTTP(rw http.ResponseWriter, r *http.Request) {
	s.router.ServeHTTP(rw, r)
}

func (s *server) Start(config *conf.Config) error {
	s.logger.Infof("Starting server at %s", config.Server.BindAddr)

	return http.ListenAndServe(config.Server.BindAddr, s)
}
