package conf

import (
	"fmt"

	"github.com/BurntSushi/toml"
)

type configServer struct {
	BindAddr string `toml:"bind_addr"`
}

type configDatabase struct {
	DbHost string `toml:"db_host"`
	DbName string `toml:"db_name"`
	DbUser string `toml:"db_user"`
	DbPass string `toml:"db_pass"`
}

func (c *configDatabase) DatabaseURL() string {
	return fmt.Sprintf(
		"host=%s dbname=%s user=%s password=%s",
		c.DbHost,
		c.DbName,
		c.DbUser,
		c.DbPass,
	)
}

type configLogging struct {
	Level string
}

type configSecurity struct {
	SecretKey string `toml:"secret_key"`
}

type Config struct {
	Server   configServer   `toml:"server"`
	Database configDatabase `toml:"database"`
	Logging  configLogging  `toml:"logging"`
	Security configSecurity `toml:"security"`
}

func GetFromFile(configPath string) (*Config, error) {
	config := &Config{}
	_, err := toml.DecodeFile(configPath, config)
	if err != nil {
		return nil, err
	}

	return config, nil
}
