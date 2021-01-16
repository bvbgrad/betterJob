"""
    Entry point for the betterJob application
"""

import app.main.main as app
import app.utils6L.utils6L as utils

from app.model import db


if __name__ == '__main__':
    utils.setup_logging()
    app.menu()
