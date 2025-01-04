import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import t


def calculate_statistics(data):
    """
    Calculate mean, standard deviation, and confidence interval for a dataset.
    """
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)  # Sample standard deviation (ddof=1)
    n = len(data)
    t_value = t.ppf(0.975, n - 1)  # 95% confidence interval
    margin_of_error = t_value * (std_dev / np.sqrt(n))
    return mean, std_dev, margin_of_error


def plot_calibration_curve(concentration, absorbance, slope, intercept):
    """
    Plot the calibration curve with the given data and regression line.
    """
    predicted_absorbance = slope * concentration + intercept

    plt.figure(figsize=(8, 6))
    plt.scatter(concentration, absorbance, label="Observed Data", color="blue")
    plt.plot(concentration, predicted_absorbance, label=f"Fit: y = {slope:.4f}x + {intercept:.4f}", color="red")
    plt.title("Calibration Curve")
    plt.xlabel("Concentration (M)")
    plt.ylabel("Absorbance")
    plt.legend()
    plt.grid(True)
    plt.show()


def calculate_calibration_curve(concentration, absorbance):
    """
    Fit a linear regression model to the calibration data.
    """
    concentration_reshaped = concentration.reshape(-1, 1)
    model = LinearRegression()
    model.fit(concentration_reshaped, absorbance)

    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(concentration_reshaped, absorbance)

    # Plot the calibration curve
    plot_calibration_curve(concentration, absorbance, slope, intercept)

    return slope, intercept, r_squared


def calculate_unknown_concentration(slope, intercept):
    """
    Calculate concentration of an unknown sample based on its absorbance.
    """
    try:
        unknown_absorbance = float(input("\nEnter the absorbance of the unknown sample: "))
        concentration = (unknown_absorbance - intercept) / slope
        return concentration
    except ValueError:
        return "Invalid input. Please enter a numerical value."


def main():
    print("Welcome to the Extended Calibration Curve Tool!")
    try:
        # Input data
        print("Enter known concentrations (comma-separated):")
        concentration = np.array([float(x.strip()) for x in input().split(",")])
        print("Enter corresponding absorbance values (comma-separated):")
        absorbance = np.array([float(x.strip()) for x in input().split(",")])

        # Validate data length
        if len(concentration) != len(absorbance):
            raise ValueError("Concentration and absorbance arrays must have the same length.")

        # Calculate statistics for absorbance
        mean_absorbance, std_dev_absorbance, margin_of_error = calculate_statistics(absorbance)

        # Print statistics
        print(f"\nStatistical Analysis of Absorbance Data:")
        print(f"Mean: {mean_absorbance:.4f}")
        print(f"Standard Deviation: {std_dev_absorbance:.4f}")
        print(f"95% Confidence Interval: ±{margin_of_error:.4f}")

        # Calculate and plot calibration curve
        slope, intercept, r_squared = calculate_calibration_curve(concentration, absorbance)
        print(f"\nCalibration Curve:")
        print(f"Equation: y = {slope:.4f}x + {intercept:.4f}")
        print(f"R² Value: {r_squared:.4f}")

        # Store data for re-plotting
        calibration_data = {"concentration": concentration, "absorbance": absorbance, "slope": slope, "intercept": intercept}

        # Prompt for unknown sample calculation or re-plotting
        while True:
            print("\nOptions:")
            print("1. Calculate an unknown sample concentration")
            print("2. Re-plot the calibration curve")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ").strip()

            if choice == "1":
                unknown_concentration = calculate_unknown_concentration(slope, intercept)
                print(f"Calculated Concentration: {unknown_concentration:.4f} M")
            elif choice == "2":
                plot_calibration_curve(calibration_data["concentration"], calibration_data["absorbance"], calibration_data["slope"], calibration_data["intercept"])
            elif choice == "3":
                print("Exiting the tool. Good luck with your exam!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    except ValueError as e:
        print(f"Error: {e}. Please restart the program and enter valid data.")


if __name__ == "__main__":
    main()