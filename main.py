import sys
import json
from pathlib import Path
import os
# from configurator import Container
from configurator_my import Container


if __name__ == '__main__':

    # settings = None
    json_path = "configurations.json"
    json_path = Path.cwd().joinpath(Path(json_path)).resolve()
    with open(json_path, "r") as jsonfile:
        settings = json.load(jsonfile)
    container = Container(settings)

    app = container.app
    # container.window().show()
    container.window.showMaximized()
    # container.window().showFullScreen()
    sys.exit(app.exec())
