package models

type ReadingType string

const (
	Onyomi  ReadingType = "onyomi"
	Kunyomi ReadingType = "kunyomi"
)

type Reading struct {
	Reading string      `json:"reading"`
	Meaning string      `json:"meaning"`
	Kind    ReadingType `json:"kind"`
}

func NewReading(reading, meaning string, kind ReadingType) *Reading {
	return &Reading{
		Reading: reading,
		Meaning: meaning,
		Kind:    kind,
	}
}
