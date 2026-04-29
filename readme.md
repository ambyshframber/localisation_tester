This program is designed for performing localisation tests using an N-speaker circular array. The static values inside the `Config` class can be edited to change the number and positon of speakers, the number of sounds under test, and the note corresponding to sound 0. It sends MIDI messages to N instances of a sampler, each listening to a unique channel corresponding to its index within the array. As it uses MIDI channels to determine output, this program cannot support N > 16, however, modifying it to do so would be a Simple Matter Of Programming.

## Dependencies

This program depends on mido and Tkinter. run.sh is provided to easily run the program using a virtual environment installed into `[project root]/py_venv`.
