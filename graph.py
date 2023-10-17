import matplotlib.pyplot as plt
import time
import controller


def plot(queue):
    def plot_real_time_angle(angle):
        plt.ion()  # Turn on interactive mode

        x_data = []
        y_data = []

        fig, ax = plt.subplots()
        line, = ax.plot(x_data, y_data)

        ax.set_xlabel('Time')
        ax.set_ylabel('Angle (degrees)')
        ax.set_title('Real-Time Angle Graph')

        while True:
            x_data.append(time.time())  # Use current time as x-axis value
            y_data.append(queue.get())

            line.set_xdata(x_data)
            line.set_ydata(y_data)

            ax.relim()  # Update data limits
            ax.autoscale_view()  # Auto-scale the view

            plt.draw()
            plt.pause(0.1)  # Pause to allow the graph to update

        plt.ioff()  # Turn off interactive mode after loop
        plt.show()  # Display the final graph

    # Call the function with the angle function
    plot_real_time_angle(controller.getAngle())
