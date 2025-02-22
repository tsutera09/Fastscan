import time
from rtlsdr import RtlSdr
import numpy as np

def record_sdr(frequency, sample_rate=2.56e6, duration=2, file_name="sdr_data.bin", chunk_size=256*1024):  # Use 2.56 MHz sample rate
    print(f"Initializing RTL-SDR for frequency: {frequency/1e6:.3f} MHz")
    sdr = RtlSdr()

    # Set the frequency and sample rate
    sdr.sample_rate = sample_rate  # 2.56 MHz sample rate to capture wider bandwidth
    sdr.center_freq = frequency    # Hz
    sdr.gain = 'auto'
    sdr.set_direct_sampling(2)     # Optional for increased buffer size

    num_samples = int(sample_rate * duration)
    total_samples_read = 0
    print(f"Saving IQ data to {file_name}")

    with open(file_name, 'ab') as f:  # Append to a single file
        while total_samples_read < num_samples:
            samples = sdr.read_samples(min(chunk_size, num_samples - total_samples_read))
            np.save(f, samples)
            total_samples_read += len(samples)
            print(f"Chunk saved. Total samples read now: {total_samples_read}")
            time.sleep(0.05)  # Reduced delay to speed up the scan

    sdr.close()

# Capture 5 MHz chunks from 100 kHz to 100 MHz
start_freq = 100e3    # 100 kHz
end_freq = 100e6      # 100 MHz
step_size = 5e6       # 5 MHz step size (each chunk captures 2.56 MHz of bandwidth)

# Generate the frequency range in 5 MHz steps
frequencies = np.arange(start_freq, end_freq, step_size)
print(f"Total frequencies to scan: {len(frequencies)}")

# Record all frequency chunks into 1 or 2 files
file_name = "sdr_data_fastscan.bin"  # Single output file
for freq in frequencies:
    print(f"Starting recording for {freq/1e6:.3f} MHz")
    record_sdr(freq, file_name=file_name)  # Append data to the same file
    print(f"Finished recording for {freq/1e6:.3f} MHz")

