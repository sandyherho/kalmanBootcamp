import numpy as np
import matplotlib.pyplot as plt

# Sandy Herho <sandy.herho@email.ucr.edu>
# This script simulates voltage measurements and applies an averaging filter to smooth the data.

class AvgFilter:
    def __init__(self):
        """
        Initialize the averaging filter with persistent variables.
        """
        self.prev_avg = 0  # Previous average value
        self.k = 1  # Sample counter

    def compute(self, x):
        """
        Compute the updated average for a given input.

        Parameters:
        x (float): The new input sample.

        Returns:
        float: The updated average.
        """
        alpha = (self.k - 1) / self.k  # Smoothing factor
        avg = alpha * self.prev_avg + (1 - alpha) * x

        # Update state variables
        self.prev_avg = avg
        self.k += 1

        return avg

def get_volt():
    """
    Simulate a voltage measurement with noise.

    Returns:
    float: A simulated voltage value.
    """
    w = np.random.randn() * 4  # Random noise with standard deviation of 4
    return 14.4 + w  # Base voltage of 14.4V with noise

# Simulation parameters
dt = 0.2  # Time step in seconds
t = np.arange(0, 10 + dt, dt)  # Time vector from 0 to 10 seconds

Nsamples = len(t)  # Number of samples

# Storage for results
avg_saved = np.zeros(Nsamples)  # Array to store filtered averages
xm_saved = np.zeros(Nsamples)  # Array to store raw measurements

# Initialize the averaging filter
filter_instance = AvgFilter()

# Run the simulation
for k in range(Nsamples):
    xm = get_volt()  # Get a new voltage measurement
    avg = filter_instance.compute(xm)  # Apply the averaging filter

    avg_saved[k] = avg  # Save the filtered value
    xm_saved[k] = xm  # Save the raw measurement

# Plot the results
plt.figure()
plt.plot(t, xm_saved, 'r:*', label='Measured Voltage')  # Raw voltage measurements
plt.plot(t, avg_saved, 'o-', label='Filtered Average')  # Filtered averages
plt.xlabel('Time (s)')  # X-axis label
plt.ylabel('Voltage (V)')  # Y-axis label
plt.legend()  # Show legend
plt.title('Voltage Measurement and Filtering')  # Plot title
plt.grid()  # Show grid for better visualization

# Save the plot
plt.savefig("voltage_filtering_results.png")  # Save the figure as a PNG file
plt.show()  # Display the plot

