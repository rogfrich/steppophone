import mido
from steppo import get_messages, Message, create_stepmap, get_tracks

def test_get_tracks():
    test_file = './midi_files/2_tracks.mid'
    mf = mido.MidiFile(test_file)
    tracks = get_tracks(mf)
    assert len(tracks) == 2
    for track in tracks:
        assert isinstance(track, mido.MidiTrack)


def test_get_messages():
    test_file = './midi_files/on_off.mid'
    mf = mido.MidiFile(test_file)
    tracks = get_tracks(mf)
    messages = get_messages(tracks[0])
    assert isinstance(messages, list)
    assert len(messages) == 12


def test_basic_Message_filtering():
    note_on = Message('note_on channel=0 note=72 velocity=100 time=15360', filtered_message_types=['note_on'])
    assert note_on.filtered == True

    note_on = Message('note_on channel=0 note=72 velocity=100 time=15360')
    assert note_on.filtered == False


def test_multiple_types_message_filtering():
    tracks = get_tracks(mido.MidiFile('./midi_files/on_off.mid'))
    messages = get_messages(tracks[0])
    filtered_messages = []
    filtered_message_types = ['note_off', 'meta', 'other']
    for m in messages:
        this_message = Message(m, filtered_message_types)
        if not this_message.filtered:
            filtered_messages.append(this_message)

    for fm in filtered_messages:
        assert fm.message_type == 'note_on'


def test_Message_returns_correct_name():
    note_on = Message('note_on channel=0 note=72 velocity=100 time=15360')
    assert note_on.__str__() == 'note_on'

    note_off = Message('note_off channel=0 note=72 velocity=100 time=15360')
    assert note_off.__str__() == 'note_off'

    meta = Message('<meta channel=0 note=72 velocity=100 time=15360')
    assert meta.__str__() == 'meta'


def test_Message_type_correctly_derived():
    note_on = Message('note_on channel=0 note=72 velocity=100 time=15360')
    assert note_on.message_type == 'note_on'

    note_off = Message('note_off channel=0 note=72 velocity=100 time=15360')
    assert note_off.message_type == 'note_off'

    meta = Message('<meta channel=0 note=72 velocity=100 time=15360')
    assert meta.message_type == 'meta'

    other = Message('Some unknown message type')
    assert other.message_type == 'other'


def test_Message_paramater_parsing():
    note_on = Message('note_on channel=0 note=72 velocity=100 time=15360')
    valid_params = {
        'channel': '0',
        'note': '72',
        'velocity': '100',
        'time': '15360',
    }
    assert valid_params == note_on.params


def test_create_stepmap():
    messages = get_messages(mido.MidiFile('./midi_files/on_off.mid'))
    stepmap = create_stepmap(messages)
    assert isinstance(stepmap, dict)
    assert len(stepmap) == 8
    assert stepmap[0].message_type == 'note_on'
    assert stepmap[7].message_type == 'note_off'



