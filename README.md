Steppo takes a standard MIDI file and converts it into a text file suitable for feeding a steppophone. 

Constraints:
- All notes should be the same length (they're effectively "pulses" rather musical notes).
- Midi note length is set to a constant of 15360 ticks which is an eighth note at a tempo of 60BPM. Tempo is arbitary - it's set by the steppophone itself - so this app might as well use an easy-to-work-with value.
- This utility works with Standard Midi Files exported by Propellerhead Reason. No other midi files have been tested.
- If a track ends on a rest (a "blank" in terms of the steppophone output), that final blank is not represented in the output. This doesn't affect operation but is annoying and is on the fix list.
- Since the steppophone is inherently monophonic, so is this utility. Steppo does not support polyphonic tracks (but does support multiple monophonic tracks playing at once).