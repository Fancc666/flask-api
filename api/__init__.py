# api/__init__.py
from pathlib import Path
from flask import Blueprint, Flask
import importlib
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    """确保中文不转义"""
    ensure_ascii = False

def register_all(app: Flask):
    app.json = CustomJSONProvider(app)
    for file in Path(__file__).parent.glob('*.py'):
        if file.stem.startswith('_'):
            continue
        module = importlib.import_module(f'api.{file.stem}')
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)
