import os
import json
import logging.config


class Config:
    def __init__(self):
        # Determine the environment, defaulting to 'development' if not set
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.config_folder = os.path.join(os.path.dirname(__file__), 'environment')
        self.config = self.load_config()
        self.setup_logging()

    def load_config(self):
        """
        Load the configuration file based on the current environment.
        """
        config_map = {
            'development': 'development.json',
            'canary': 'canary.json',
            'stable': 'stable.json',
        }
        config_file = config_map.get(self.environment, 'development.json')
        config_path = os.path.join(self.config_folder, config_file)

        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"Configuration file {config_path} not found.")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON file {config_path}.")
            return {}

    def setup_logging(self):
        """
        Setup logging based on the configuration file.
        """
        logging_config = self.config.get('logging', None)
        if logging_config:
            logging.config.dictConfig(logging_config)
        else:
            # Default logging setup if not defined in the config file
            logging.basicConfig(level=logging.INFO)
            logging.warning("No logging configuration found in the config file. Using default logging settings.")


# Initialize the config object
config = Config()
