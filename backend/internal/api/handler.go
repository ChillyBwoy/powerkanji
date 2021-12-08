package api

import "github.com/sirupsen/logrus"

type Handler interface {
	Init(logger *logrus.Logger)
}
