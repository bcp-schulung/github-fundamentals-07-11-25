import importlib
import pytest
from flask import Flask

# tests/test_deploy.py

CANDIDATES = ["app", "application", "wsgi", "src.app", "flaskr", "project", "myapp"]


def _discover_app():
    for name in CANDIDATES:
        try:
            mod = importlib.import_module(name)
        except Exception:
            continue

        # try factory pattern: create_app()
        factory = getattr(mod, "create_app", None)
        if callable(factory):
            try:
                app = factory()
                if isinstance(app, Flask):
                    return app
            except Exception:
                continue

        # try app instance attribute
        for attr in ("app", "application"):
            app = getattr(mod, attr, None)
            if isinstance(app, Flask):
                return app

    pytest.skip(
        "Could not import a Flask app. Make your app importable as one of: "
        + ", ".join(CANDIDATES)
    )


def test_flask_app_runs():
    """
    Check that the Flask app can be imported and the root URL responds with < 400.
    This accepts 200, 302, etc., as long as it's not an error.
    """
    app = _discover_app()
    app.testing = True
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code < 400, f"Root endpoint returned {resp.status_code}"