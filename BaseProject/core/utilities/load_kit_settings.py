import json
import importlib
from pathlib import Path

VALID_KEYS = {"secrets_backend", "storage_backend", "components"}
VALID_SECRETS_BACKENDS = {"aws", "local"}
VALID_STORAGE_BACKENDS = {"s3", "local"}
COMPONENTS_MODULE_PATH = "BaseProject.core.settings.components"
file_name = "kit.json"


def load_kit_config(path: Path) -> dict:

    if not path.exists():
        raise FileNotFoundError(f"{file_name} not find in: {path}")

    with open(path, "r") as f:
        config = json.load(f)

    missing = VALID_KEYS - config.keys()
    if missing:
        raise KeyError(f"{file_name}: Keys requires: {missing}")

    if config["secrets_backend"] not in VALID_SECRETS_BACKENDS:
        raise ValueError(f"secrets_backend invalid: {config['secrets_backend']}.")

    if config["storage_backend"] not in VALID_STORAGE_BACKENDS:
        raise ValueError(f"storage_backend invalid: {config['storage_backend']}.")

    if not isinstance(config["components"], dict):
        raise TypeError(f"{file_name}: 'components' should be a list")

    return config


def validate_components(components: list) -> None:
    errors = []

    for name, options in components.items():
        module_path = f"{COMPONENTS_MODULE_PATH}.{name}"
        class_name = f"{name.upper()}Config"
        try:
            module = importlib.import_module(module_path)
            if not hasattr(module, class_name):
                errors.append(f"The Class '{class_name}' is not found in {module_path}")
        except ModuleNotFoundError:
            errors.append(f"Module is not found: {module_path}")

    if errors:
        raise ImportError("Components errors:\n" + "\n".join(errors))
