from typing import List
from mido import MidiFile, MidiTrack

CMAJ_SCALE = MidiFile('./midi_files/cmaj_scale_C4toC5_60bpm.mid')
ON_OFF = MidiFile('./midi_files/on_off.mid')
TWO_TRACKS = MidiFile('./midi_files/2_tracks.mid')
ONE_BEAT = 15360


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

def create_output(stepmap: dict) -> str:
    output = ""
    for step, message in stepmap.items():
        if not message.filtered:
            try:
                next_step_message: Message = stepmap[step + 1]
                if next_step_message.message_type == 'note_on' and int(next_step_message.params['time']) == ONE_BEAT:
                    output += '0,'
                elif message.message_type == 'note_on':
                    output += f"{message.params['note']},"
            except KeyError:
                break
    return output

if __name__ == '__main__':
    track_list = get_tracks(TWO_TRACKS)
    print(track_list)
    for track in track_list:
        message_list = get_messages(track)
        stepmap = create_stepmap(message_list)
        #
        # for k, v in stepmap.items():
        #     if not v.filtered:
        #         try:
        #             next_step_message: Message = stepmap[k + 1]
        #
        #             if next_step_message.message_type == 'note_on' and int(next_step_message.params['time']) == ONE_BEAT:
        #                 print('blank')
        #             elif v.message_type == 'note_on':
        #                 print(v.message_type, v.params['note'])
        #         except KeyError:
        #             break

        print(create_output(stepmap))
