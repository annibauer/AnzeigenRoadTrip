import os
import socket

import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

from functions.logger import configure_logger

logger = configure_logger()


def get_available_port(preferred_port: int = 8050, host: str = "0.0.0.0") -> int:
    for port in range(preferred_port, preferred_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((host, port))
                return port
        except OSError:
            continue

    raise OSError(f"No free port found starting from {preferred_port}")


def get_runtime_settings() -> dict:
    host = os.getenv("HOST", "0.0.0.0")
    preferred_port = int(os.getenv("PORT", "8050"))
    debug = os.getenv("DEBUG", "False").lower() in {"1", "true", "yes"}
    port = get_available_port(preferred_port, host)

    return {
        "host": host,
        "port": port,
        "debug": debug,
        "use_reloader": False,
    }


def create_app() -> Dash:
    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )

    app.layout = html.Div([
        dash.page_container,
    ])

    return app


app = create_app()
logger.info("Starting ANZEIGEN app")

if __name__ == "__main__":
    runtime_settings = get_runtime_settings()

    if runtime_settings["port"] != int(os.getenv("PORT", "8050")):
        logger.warning(
            "Port %s is in use; starting the app on %s instead.",
            int(os.getenv("PORT", "8050")),
            runtime_settings["port"],
        )

    app.run(
        debug=runtime_settings["debug"],
        host=runtime_settings["host"],
        port=runtime_settings["port"],
        use_reloader=runtime_settings["use_reloader"],
    )
