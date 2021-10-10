from typing import List
from mido import MidiFile, MidiTrack
from settings import NOTES_PER_ROW

CMAJ_SCALE = MidiFile('./midi_files/cmaj_scale_C4toC5_60bpm.mid')
ON_OFF = MidiFile('./midi_files/on_off.mid')
TWO_TRACKS = MidiFile('./midi_files/2_tracks.mid')
ONE_BEAT = 7680
JINGLE_TEST = MidiFile('./midi_files/jingle2021v2.mid')


class Message:
    """
    Represents an individual MIDI message.
    """

    def __init__(self, raw: str, filtered_message_types: list = None):
        self.raw = raw
        self.params = self.parse_message_for_params()

        if self.raw.startswith('note_on'):
            self.message_type = 'note_on'
        elif self.raw.startswith('note_off'):
            self.message_type = 'note_off'
        elif 'meta' in self.raw:
            self.message_type = 'meta'
        else:
            self.message_type = 'other'

        if filtered_message_types and self.message_type in filtered_message_types:
            self.filtered = True
        else:
            self.filtered = False

    def parse_message_for_params(self) -> dict:
        """
        Parameters for a given MIDI message are in one long string. Spilt them into something usable.
        """
        params = {}
        split_message = self.raw.split()
        for i in split_message:
            if '=' in i:
                params[i.split('=')[0]] = i.split("=")[1]

        return params

    def __str__(self):
        return f"{self.message_type}"

    def __repr__(self):
        return f"{self.message_type}"


class Output:
    """
    Represents the output that will be written to a file
    """

    def __init__(self):
        self.text: str = ""
        self.track_count: int = 0
        self.total_message_count: int = 0

    def update_text(self, stepmap):
        """
        Takes a stepmap and renders it as a string, adding it to the output text.
        """
        self.track_count += 1
        if self.track_count > 1:
            self.text += f"\nvoice {self.track_count}\n"
        else:
            self.text += f"voice {self.track_count}\n"

        row = ""

        for step, message in stepmap.items():
            if not message.filtered:
                try:
                    next_step_message: Message = stepmap[step + 1]
                    if next_step_message.message_type == 'note_on' and int(
                            next_step_message.params['time']) == ONE_BEAT:
                        row += '0,'
                    elif message.message_type == 'note_on':
                        row += f"{message.params['note']},"
                except KeyError:  # Reached the end
                    # Make sure that final blank notes are correctly shown
                    if len(row.rstrip(',').split(',')) == NOTES_PER_ROW - 1:
                        row += '0,'

                    self.text += row


    def strip_final_comma(self):
        """
        The steppophone output format specifies no final comma
        """
        self.text = self.text.rstrip(',')


def get_tracks(mid: MidiFile) -> list[MidiTrack]:
    """
    Extract the individual tracks from the MIDI file, not including the transport track
    which isn't needed.
    """
    return [track for track in mid.tracks if 'Transport' not in str(track)]


def get_messages(track: MidiTrack) -> List[str]:
    """
    Take a single track and extract the MIDI messages from it.
    """
    messages = []
    for msg in track:
        messages.append(str(msg))

    return messages


def create_stepmap(messages: list) -> dict:
    """
    Create a stepmap that contains only the events we need (no meta events).
    """
    index = 0
    steps = {}

    for msg in messages:
        filtered = ['meta']
        this_message = Message(msg, filtered_message_types=filtered)
        if not this_message.filtered:
            steps[index] = this_message
            index += 1


    return steps


if __name__ == '__main__':
    total_message_count = 0
    track_list = get_tracks(JINGLE_TEST)
    o = Output()
    for track in track_list:
        message_list = get_messages(track)
        stepmap = create_stepmap(message_list)
        o.update_text(stepmap)
    o.strip_final_comma()
    print(o.text)
    with open('/Users/rich/jingle2021.txt', 'w') as fout:
        fout.write(o.text)

