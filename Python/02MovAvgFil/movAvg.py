import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# Sandy Herho <sandy.herho@email.ucr.edu>
# This script simulates sonar measurements and applies a moving average filter to smooth the data.

class MovAvgFilter:
    def __init__(self, n=100):
        """
        Initialize the moving average filter with a specified buffer size.

        Parameters:
        n (int): The number of samples to use in the moving average.
        """
        self.n = n  # Buffer size
        self.first_run = True

    def compute(self, x):
        """
        Compute the moving average for a given input.

        Parameters:
        x (float): The new input sample.

        Returns:
        float: The moving average of the input.
        """
        if self.first_run:
            self.xbuf = np.ones(self.n) * x  # Initialize buffer with the first value
            self.first_run = False

        # Shift the buffer and add the new value
        self.xbuf[:-1] = self.xbuf[1:]
        self.xbuf[-1] = x

        # Compute and return the average
        return np.sum(self.xbuf) / self.n

def get_sonar():
    """
    Simulate a sonar reading using data from the loaded SonarAlt.mat file.

    Returns:
    float: The simulated sonar altitude.
    """
    if not hasattr(get_sonar, "initialized"):
        # Emulate MATLAB's persistent variable with function attributes
        get_sonar.initialized = True
        get_sonar.k = 0
        # Load sonar altitude data from the MATLAB file
        mat_data = loadmat("SonarAlt.mat")
        get_sonar.sonarAlt = mat_data["sonarAlt"].flatten()

    # Get the current reading and increment the counter
    h = get_sonar.sonarAlt[get_sonar.k % len(get_sonar.sonarAlt)]
    get_sonar.k += 1
    return h

def main():
    # User-configurable parameters
    Nsamples = 1500  # Number of samples
    dt = 0.02  # Time step in seconds
    n = 100  # Moving average buffer size

    t = np.arange(0, Nsamples * dt, dt)  # Time vector

    # Storage for results
    xsaved = np.zeros(Nsamples)  # Array to store filtered values
    xmsaved = np.zeros(Nsamples)  # Array to store raw measurements

    # Initialize the moving average filter
    filter_instance = MovAvgFilter(n=n)

    # Run the simulation
    for k in range(Nsamples):
        xm = get_sonar()  # Get a new sonar measurement
        x = filter_instance.compute(xm)  # Apply the moving average filter

        xsaved[k] = x  # Save the filtered value
        xmsaved[k] = xm  # Save the raw measurement

    # Plot the results
    plt.figure()
    plt.plot(t, xmsaved, 'r.', label='Measured')  # Raw sonar measurements
    plt.plot(t, xsaved, 'k', linewidth=3, label='Moving Average')  # Filtered measurements
    plt.xlabel('Time (s)')  # X-axis label
    plt.ylabel('Sonar Altitude')  # Y-axis label
    plt.legend(loc='upper left')  # Show legend
    plt.title('Sonar Measurement and Moving Average Filter')  # Plot title
    plt.grid()  # Show grid for better visualization

    # Save the plot
    plt.savefig("sonar_moving_average_results.png")  # Save the figure as a PNG file
    plt.show()  # Display the plot

if __name__ == "__main__":
    main()

