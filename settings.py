import datetime

NOTE_MAP = {
    81: 0,   # A4
    82: 1,   # A#4
    83: 2,   # B4
    84: 3,   # C5
    85: 4,   # C#5
    86: 5,   # D5
    87: 6,   # D#5
    88: 7,   # E5
    89: 8,   # F5
    90: 9,   # F#5
    91: 10,  # G5
    92: 11,  # G#5
}

OUTPUT_FOLDER = '~/steppophone_output'
OUTPUT_FILENAME = f"steppo_{datetime.datetime.now()}"
OUTPUT_HEADER = ""

NOTES_PER_ROW = 8
