import wave
import struct

source = wave.open("in.wav", mode="rb")
frames_count = source.getnframes()

data = struct.unpack("<" + str(frames_count) + "h",
                     source.readframes(frames_count))

print(data)