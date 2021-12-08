package handlers

import (
	"log"
	"net/http"
)

type KanjiHandler struct{}

func NewKanjiHandler() *KanjiHandler {
	return &KanjiHandler{}
}

func (h *KanjiHandler) Init() {

}

func HandleKanjiList(rw http.ResponseWriter, r *http.Request) {
	log.Println("list of kanji")
}
