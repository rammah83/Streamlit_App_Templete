# pyspc.py

import numpy as np
import matplotlib.pyplot as plt

# Constants for control charts

# X-bar and R chart constants for n from 2 to 9
A2_table = {
    2: 1.880,
    3: 1.023,
    4: 0.729,
    5: 0.577,
    6: 0.483,
    7: 0.419,
    8: 0.373,
    9: 0.337,
}
D3_table = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184}
D4_table = {
    2: 3.267,
    3: 2.574,
    4: 2.282,
    5: 2.114,
    6: 2.004,
    7: 1.924,
    8: 1.864,
    9: 1.816,
}

# X-bar and S chart constants for n from 10 to 25
A3_table = {
    10: 0.975,
    11: 0.886,
    12: 0.810,
    13: 0.746,
    14: 0.692,
    15: 0.645,
    16: 0.604,
    17: 0.568,
    18: 0.535,
    19: 0.505,
    20: 0.478,
    21: 0.454,
    22: 0.432,
    23: 0.412,
    24: 0.393,
    25: 0.375,
}

B3_table = {
    10: 0.223,
    11: 0.239,
    12: 0.253,
    13: 0.266,
    14: 0.278,
    15: 0.289,
    16: 0.299,
    17: 0.308,
    18: 0.317,
    19: 0.325,
    20: 0.333,
    21: 0.340,
    22: 0.347,
    23: 0.354,
    24: 0.361,
    25: 0.367,
}

B4_table = {
    10: 1.777,
    11: 1.757,
    12: 1.743,
    13: 1.732,
    14: 1.723,
    15: 1.716,
    16: 1.711,
    17: 1.707,
    18: 1.703,
    19: 1.700,
    20: 1.698,
    21: 1.697,
    22: 1.695,
    23: 1.694,
    24: 1.693,
    25: 1.693,
}


def calculate_x_mr_chart(data):
    X = data.values
    X_bar = np.mean(X)
    MR = np.abs(np.diff(X))  # Moving ranges
    MR_bar = np.mean(MR)

    # Constants for n=2 (since moving ranges between two observations)
    E2 = 2.66  # For n=2
    D3 = 0.0  # For n=2
    D4 = 3.267  # For n=2

    # Control limits for X chart
    UCL_X = X_bar + E2 * MR_bar
    LCL_X = X_bar - E2 * MR_bar

    # Control limits for MR chart
    UCL_MR = D4 * MR_bar
    LCL_MR = D3 * MR_bar

    return X, X_bar, MR, MR_bar, UCL_X, LCL_X, UCL_MR, LCL_MR


def plot_x_chart(X, UCL_X, LCL_X, X_bar):
    fig, ax = plt.subplots()
    ax.plot(X, marker="o", linestyle="-")
    ax.axhline(UCL_X, color="red", linestyle="--", label="UCL")
    ax.axhline(X_bar, color="green", linestyle="-", label="Center Line")
    ax.axhline(LCL_X, color="red", linestyle="--", label="LCL")
    ax.set_title("X (Individuals) Control Chart")
    ax.set_xlabel("Observation")
    ax.set_ylabel("Individual Value")
    ax.legend()
    return fig


def plot_mr_chart(MR, UCL_MR, LCL_MR, MR_bar):
    fig, ax = plt.subplots()
    ax.plot(MR, marker="o", linestyle="-")
    ax.axhline(UCL_MR, color="red", linestyle="--", label="UCL")
    ax.axhline(MR_bar, color="green", linestyle="-", label="Center Line")
    ax.set_title("Moving Range Chart")
    ax.set_xlabel("Observation")
    ax.set_ylabel("Moving Range")
    ax.legend()
    return fig


def calculate_xbar_r_chart(data, num_samples):
    n = num_samples
    if n not in A2_table or n not in D3_table or n not in D4_table:
        raise ValueError(
            "Sample size not supported for X-bar and R chart. Please choose a subgroup size between 2 and 9."
        )
    A2 = A2_table[n]
    D3 = D3_table[n]
    D4 = D4_table[n]

    total_samples = len(data) // n * n
    data = data.iloc[:total_samples]
    grouped_data = data.values.reshape((-1, n))

    X_bar = grouped_data.mean(axis=1)
    X_double_bar = np.mean(X_bar)
    R = grouped_data.max(axis=1) - grouped_data.min(axis=1)
    R_bar = np.mean(R)

    # Calculate control limits for X-bar chart
    UCL_X = X_double_bar + A2 * R_bar
    LCL_X = X_double_bar - A2 * R_bar

    # Calculate control limits for R chart
    UCL_R = D4 * R_bar
    LCL_R = D3 * R_bar

    return X_bar, X_double_bar, R, R_bar, UCL_X, LCL_X, UCL_R, LCL_R


def calculate_xbar_s_chart(data, num_samples):
    n = num_samples
    if n not in A3_table or n not in B3_table or n not in B4_table:
        raise ValueError(
            "Sample size not supported for X-bar and S chart. Please choose a subgroup size of 10 or more."
        )
    A3 = A3_table[n]
    B3 = B3_table[n]
    B4 = B4_table[n]

    total_samples = len(data) // n * n
    data = data.iloc[:total_samples]
    grouped_data = data.values.reshape((-1, n))

    X_bar = grouped_data.mean(axis=1)
    X_double_bar = np.mean(X_bar)
    S = grouped_data.std(axis=1, ddof=1)
    S_bar = np.mean(S)

    # Calculate control limits for X-bar chart
    UCL_X = X_double_bar + A3 * S_bar
    LCL_X = X_double_bar - A3 * S_bar

    # Calculate control limits for S chart
    UCL_S = B4 * S_bar
    LCL_S = B3 * S_bar

    return X_bar, X_double_bar, S, S_bar, UCL_X, LCL_X, UCL_S, LCL_S


def plot_xbar_chart(X_bar, UCL_X, LCL_X, X_double_bar):
    fig, ax = plt.subplots()
    ax.plot(X_bar, marker="o", linestyle="-")
    ax.axhline(UCL_X, color="red", linestyle="--", label="UCL")
    ax.axhline(X_double_bar, color="green", linestyle="-", label="Center Line")
    ax.axhline(LCL_X, color="red", linestyle="--", label="LCL")
    ax.set_title("X-bar Control Chart")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Mean Value")
    ax.legend()
    return fig


def plot_r_chart(R, UCL_R, LCL_R, R_bar):
    fig, ax = plt.subplots()
    ax.plot(R, marker="o", linestyle="-")
    ax.axhline(UCL_R, color="red", linestyle="--", label="UCL")
    ax.axhline(R_bar, color="green", linestyle="-", label="Center Line")
    if LCL_R > 0:
        ax.axhline(LCL_R, color="red", linestyle="--", label="LCL")
    ax.set_title("R Control Chart")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Range")
    ax.legend()
    return fig


def plot_s_chart(S, UCL_S, LCL_S, S_bar):
    fig, ax = plt.subplots()
    ax.plot(S, marker="o", linestyle="-")
    ax.axhline(UCL_S, color="red", linestyle="--", label="UCL")
    ax.axhline(S_bar, color="green", linestyle="-", label="Center Line")
    if LCL_S > 0:
        ax.axhline(LCL_S, color="red", linestyle="--", label="LCL")
    ax.set_title("S Control Chart")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Standard Deviation")
    ax.legend()
    return fig


def calculate_process_capability(data, LSL, USL):
    data = np.array(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)

    Cp = (USL - LSL) / (6 * std)
    Cpu = (USL - mean) / (3 * std)
    Cpl = (mean - LSL) / (3 * std)
    Cpk = min(Cpu, Cpl)

    return Cp, Cpk, Cpu, Cpl
