from json import load
with open("settings.json", "r") as f:
    _SETTINGS = load(f)


SCREEN_WIDTH = _SETTINGS["screen-width"]
SCREEN_HEIGHT = _SETTINGS["screen-height"]
RES = (SCREEN_WIDTH, SCREEN_HEIGHT)
BG_COLOR = _SETTINGS["bg-color"]

P_SPEED = _SETTINGS["player-speed"]
P_SIZE = _SETTINGS["player-size"]

O_SPEED = _SETTINGS["opponent-speed"]
O_SIZE = _SETTINGS["opponent-size"]

PADDLE_SPACING = _SETTINGS["paddle-space-from-screen"]

BALL_SIZE = _SETTINGS["ball-size"]
BALL_SPEED = _SETTINGS["ball-speed"]
