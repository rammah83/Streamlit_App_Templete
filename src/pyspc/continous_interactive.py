# spc_plotly.py

import numpy as np
import plotly.graph_objects as go

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
    """
    Calculate statistics and control limits for X-MR (Individuals and Moving Range) Chart.

    Parameters:
        data (pd.Series): Data series for analysis.

    Returns:
        Tuple containing:
            - X: Individual observations.
            - X_bar: Mean of X.
            - MR: Moving ranges.
            - MR_bar: Mean of MR.
            - UCL_X: Upper Control Limit for X chart.
            - LCL_X: Lower Control Limit for X chart.
            - UCL_MR: Upper Control Limit for MR chart.
            - LCL_MR: Lower Control Limit for MR chart.
    """
    X = data.values
    X_bar = np.mean(X)
    MR = np.abs(np.diff(X))  # Moving ranges
    MR_bar = np.mean(MR)

    # Constants for n=2 (since moving ranges between two observations)
    E2 = 2.66  # For individuals chart based on MR
    D3 = 0.0  # For n=2
    D4 = 3.267  # For n=2

    # Control limits for X chart
    UCL_X = X_bar + E2 * MR_bar
    LCL_X = X_bar - E2 * MR_bar

    # Control limits for MR chart
    UCL_MR = D4 * MR_bar
    LCL_MR = D3 * MR_bar

    return X, X_bar, MR, MR_bar, UCL_X, LCL_X, UCL_MR, LCL_MR


def calculate_xbar_r_chart(data, num_samples):
    """
    Calculate statistics and control limits for X-bar and R Chart.

    Parameters:
        data (pd.Series): Data series for analysis.
        num_samples (int): Number of measurements per sample (subgroup size).

    Returns:
        Tuple containing:
            - X_bar: Means of subgroups.
            - X_double_bar: Overall mean of X_bar.
            - R: Ranges of subgroups.
            - R_bar: Mean of R.
            - UCL_X: Upper Control Limit for X-bar chart.
            - LCL_X: Lower Control Limit for X-bar chart.
            - UCL_R: Upper Control Limit for R chart.
            - LCL_R: Lower Control Limit for R chart.
    """
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

    # Control limits for X-bar chart
    UCL_X = X_double_bar + A2 * R_bar
    LCL_X = X_double_bar - A2 * R_bar

    # Control limits for R chart
    UCL_R = D4 * R_bar
    LCL_R = D3 * R_bar

    return X_bar, X_double_bar, R, R_bar, UCL_X, LCL_X, UCL_R, LCL_R


def calculate_xbar_s_chart(data, num_samples):
    """
    Calculate statistics and control limits for X-bar and S Chart.

    Parameters:
        data (pd.Series): Data series for analysis.
        num_samples (int): Number of measurements per sample (subgroup size).

    Returns:
        Tuple containing:
            - X_bar: Means of subgroups.
            - X_double_bar: Overall mean of X_bar.
            - S: Standard deviations of subgroups.
            - S_bar: Mean of S.
            - UCL_X: Upper Control Limit for X-bar chart.
            - LCL_X: Lower Control Limit for X-bar chart.
            - UCL_S: Upper Control Limit for S chart.
            - LCL_S: Lower Control Limit for S chart.
    """
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

    # Control limits for X-bar chart
    UCL_X = X_double_bar + A3 * S_bar
    LCL_X = X_double_bar - A3 * S_bar

    # Control limits for S chart
    UCL_S = B4 * S_bar
    LCL_S = B3 * S_bar

    return X_bar, X_double_bar, S, S_bar, UCL_X, LCL_X, UCL_S, LCL_S


def plot_x_chart(
    X, UCL_X, LCL_X, X_bar, LSL=None, USL=None, title="X (Individuals) Control Chart"
):
    """
    Plot the Individuals (X) Control Chart using Plotly.

    Parameters:
        X (np.ndarray): Individual observations.
        UCL_X (float): Upper Control Limit.
        LCL_X (float): Lower Control Limit.
        X_bar (float): Center Line (Mean).
        LSL (float, optional): Lower Specification Limit.
        USL (float, optional): Upper Specification Limit.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The generated X chart.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=X,
            mode="markers+lines",
            name="Individual Values",
            marker=dict(color="blue"),
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[UCL_X] * len(X),
            mode="lines",
            name="UCL",
            line=dict(color="red", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[X_bar] * len(X),
            mode="lines",
            name="Center Line",
            line=dict(color="green", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[LCL_X] * len(X),
            mode="lines",
            name="LCL",
            line=dict(color="red", dash="dash"),
        )
    )

    # Add Specification Limits if provided
    if LSL is not None:
        fig.add_trace(
            go.Scatter(
                y=[LSL] * len(X),
                mode="lines",
                name="LSL",
                line=dict(color="purple", dash="dot"),
            )
        )

    if USL is not None:
        fig.add_trace(
            go.Scatter(
                y=[USL] * len(X),
                mode="lines",
                name="USL",
                line=dict(color="purple", dash="dot"),
            )
        )

    fig.update_layout(
        title=title,
        # xaxis_title="Observation",
        # yaxis_title="Individual Value",
        legend=dict(x=0, y=1.1, orientation="h"),
    )

    return fig


def plot_mr_chart(
    MR, UCL_MR, LCL_MR, MR_bar, LSL=None, USL=None, title="Moving Range Chart"
):
    """
    Plot the Moving Range (MR) Control Chart using Plotly.

    Parameters:
        MR (np.ndarray): Moving ranges.
        UCL_MR (float): Upper Control Limit for MR chart.
        LCL_MR (float): Lower Control Limit for MR chart (often 0).
        MR_bar (float): Center Line (Mean of MR).
        LSL (float, optional): Lower Specification Limit.
        USL (float, optional): Upper Specification Limit.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The generated MR chart.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=MR,
            mode="markers+lines",
            name="Moving Range",
            marker=dict(color="blue"),
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[UCL_MR] * len(MR),
            mode="lines",
            name="UCL",
            line=dict(color="red", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[MR_bar] * len(MR),
            mode="lines",
            name="Center Line",
            line=dict(color="green", dash="dash"),
        )
    )

    if LCL_MR > 0:
        fig.add_trace(
            go.Scatter(
                y=[LCL_MR] * len(MR),
                mode="lines",
                name="LCL",
                line=dict(color="red", dash="dash"),
            )
        )

    # Add Specification Limits if provided
    if LSL is not None:
        fig.add_trace(
            go.Scatter(
                y=[LSL] * len(MR),
                mode="lines",
                name="LSL",
                line=dict(color="purple", dash="dot"),
            )
        )

    if USL is not None:
        fig.add_trace(
            go.Scatter(
                y=[USL] * len(MR),
                mode="lines",
                name="USL",
                line=dict(color="purple", dash="dot"),
            )
        )

    fig.update_layout(
        title=title,
        # xaxis_title="Observation",
        # yaxis_title="Moving Range",
        legend=dict(x=0, y=1.1, orientation="h"),
    )

    return fig


def plot_xbar_chart(
    X_bar, UCL_X, LCL_X, X_double_bar, LSL=None, USL=None, title="X-bar Control Chart"
):
    """
    Plot the X-bar Control Chart using Plotly.

    Parameters:
        X_bar (np.ndarray): Means of subgroups.
        UCL_X (float): Upper Control Limit for X-bar chart.
        LCL_X (float): Lower Control Limit for X-bar chart.
        X_double_bar (float): Center Line (Overall Mean).
        LSL (float, optional): Lower Specification Limit.
        USL (float, optional): Upper Specification Limit.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The generated X-bar chart.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=X_bar,
            mode="markers+lines",
            name="Subgroup Means",
            marker=dict(color="blue"),
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[UCL_X] * len(X_bar),
            mode="lines",
            name="UCL",
            line=dict(color="red", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[X_double_bar] * len(X_bar),
            mode="lines",
            name="Center Line",
            line=dict(color="green", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[LCL_X] * len(X_bar),
            mode="lines",
            name="LCL",
            line=dict(color="red", dash="dash"),
        )
    )

    # Add Specification Limits if provided
    if LSL is not None:
        fig.add_trace(
            go.Scatter(
                y=[LSL] * len(X_bar),
                mode="lines",
                name="LSL",
                line=dict(color="purple", dash="dot"),
            )
        )

    if USL is not None:
        fig.add_trace(
            go.Scatter(
                y=[USL] * len(X_bar),
                mode="lines",
                name="USL",
                line=dict(color="purple", dash="dot"),
            )
        )

    fig.update_layout(
        title=title,
        # xaxis_title="Sample",
        # yaxis_title="Mean Value",
        legend=dict(x=0, y=1.1, orientation="h"),
    )

    return fig


def plot_r_chart(R, UCL_R, LCL_R, R_bar, LSL=None, USL=None, title="R Control Chart"):
    """
    Plot the R (Range) Control Chart using Plotly.

    Parameters:
        R (np.ndarray): Ranges of subgroups.
        UCL_R (float): Upper Control Limit for R chart.
        LCL_R (float): Lower Control Limit for R chart.
        R_bar (float): Center Line (Mean of R).
        LSL (float, optional): Lower Specification Limit.
        USL (float, optional): Upper Specification Limit.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The generated R chart.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=R,
            mode="markers+lines",
            name="Range",
            marker=dict(color="blue"),
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[UCL_R] * len(R),
            mode="lines",
            name="UCL",
            line=dict(color="red", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[R_bar] * len(R),
            mode="lines",
            name="Center Line",
            line=dict(color="green", dash="dash"),
        )
    )

    if LCL_R > 0:
        fig.add_trace(
            go.Scatter(
                y=[LCL_R] * len(R),
                mode="lines",
                name="LCL",
                line=dict(color="red", dash="dash"),
            )
        )

    # Add Specification Limits if provided
    if LSL is not None:
        fig.add_trace(
            go.Scatter(
                y=[LSL] * len(R),
                mode="lines",
                name="LSL",
                line=dict(color="purple", dash="dot"),
            )
        )

    if USL is not None:
        fig.add_trace(
            go.Scatter(
                y=[USL] * len(R),
                mode="lines",
                name="USL",
                line=dict(color="purple", dash="dot"),
            )
        )

    fig.update_layout(
        title=title,
        # xaxis_title="Sample",
        # yaxis_title="Range",
        legend=dict(x=0, y=1.1, orientation="h"),
    )

    return fig


def plot_s_chart(S, UCL_S, LCL_S, S_bar, LSL=None, USL=None, title="S Control Chart"):
    """
    Plot the S (Standard Deviation) Control Chart using Plotly.

    Parameters:
        S (np.ndarray): Standard deviations of subgroups.
        UCL_S (float): Upper Control Limit for S chart.
        LCL_S (float): Lower Control Limit for S chart.
        S_bar (float): Center Line (Mean of S).
        LSL (float, optional): Lower Specification Limit.
        USL (float, optional): Upper Specification Limit.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The generated S chart.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=S,
            mode="markers+lines",
            name="Standard Deviation",
            marker=dict(color="blue"),
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[UCL_S] * len(S),
            mode="lines",
            name="UCL",
            line=dict(color="red", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=[S_bar] * len(S),
            mode="lines",
            name="Center Line",
            line=dict(color="green", dash="dash"),
        )
    )

    if LCL_S > 0:
        fig.add_trace(
            go.Scatter(
                y=[LCL_S] * len(S),
                mode="lines",
                name="LCL",
                line=dict(color="red", dash="dash"),
            )
        )

    # Add Specification Limits if provided
    if LSL is not None:
        fig.add_trace(
            go.Scatter(
                y=[LSL] * len(S),
                mode="lines",
                name="LSL",
                line=dict(color="purple", dash="dot"),
            )
        )

    if USL is not None:
        fig.add_trace(
            go.Scatter(
                y=[USL] * len(S),
                mode="lines",
                name="USL",
                line=dict(color="purple", dash="dot"),
            )
        )

    fig.update_layout(
        title=title,
        # xaxis_title="Sample",
        # yaxis_title="Standard Deviation",
        legend=dict(x=0, y=1.1, orientation="h"),
    )

    return fig


def calculate_process_capability(data, LSL, USL):
    """
    Calculate process capability indices: Cp, Cpk, Cpu, Cpl.

    Parameters:
        data (pd.Series or np.ndarray): Data series for analysis.
        LSL (float): Lower Specification Limit.
        USL (float): Upper Specification Limit.

    Returns:
        Tuple containing:
            - Cp: Process Capability Index.
            - Cpk: Minimum of Cpu and Cpl.
            - Cpu: Capability Index for upper specification.
            - Cpl: Capability Index for lower specification.
    """
    data = np.array(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)

    Cp = (USL - LSL) / (6 * std)
    Cpu = (USL - mean) / (3 * std)
    Cpl = (mean - LSL) / (3 * std)
    Cpk = min(Cpu, Cpl)

    return Cp, Cpk, Cpu, Cpl
