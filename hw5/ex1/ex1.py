import wave

FILE = "andrea.piccione@epfl.ch.wav"

# open file
wave_obj = wave.open(FILE, mode="r")

# gen number of frames
length = wave_obj.getnframes()

lsb_result = []

# get sample width
sample_width = wave_obj.getsampwidth()

print("Looking at frames...")

# Looking at all the frames
for i in range(0,length):
    frame = wave_obj.readframes(1)
    # Get first sample and extract from it the lsb
    sample_1 = frame[:sample_width]
    lsb_result.append(bin(int.from_bytes(sample_1, byteorder="little"))[-1])
    
    # Get second sample and extract from it the lsb
    sample_2 = frame[sample_width:]
    lsb_result.append(bin(int.from_bytes(sample_2, byteorder="little"))[-1])

# Get string of lsb
bit_string = ''.join(lsb_result)

# Look at the bit string inside the first and last 1, where the message is likely to
start = bit_string.find('1')
end = bit_string.rfind('1')

# Convert bit to string
print("Token: " + int(bit_string[start:end+1], 2).to_bytes(len(bit_string[start:end+1]) + 7 // 8, byteorder='big').decode())
