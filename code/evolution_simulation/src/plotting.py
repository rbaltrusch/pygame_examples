# -*- coding: utf-8 -*-
"""Module containing code related to plotting"""
import statistics
from collections import deque
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Deque
from typing import List

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


@dataclass
class PlotData:
    """Class for data to be plotted"""

    vision: List[float] = field(default_factory=list)
    size: List[float] = field(default_factory=list)
    speed: List[float] = field(default_factory=list)
    energy_loss: List[float] = field(default_factory=list)
    food_energy: List[float] = field(default_factory=list)
    food_amount: List[float] = field(default_factory=list)
    animal_amount: List[float] = field(default_factory=list)


def plot_data(plotting_data: PlotData, output_filename: str):
    """Plots the specified plot data and saves the plot"""
    if plt is None:
        print("Skipping plots because matplotlib could not be imported.")
        return

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 6))  # type: ignore
    fig.tight_layout(pad=3)
    fig.suptitle("Evolution simulation results")  # type: ignore

    ax1.plot(  # type: ignore
        normalize(plotting_data.food_amount), label="Amount of food", color="#6F7B75"
    )
    ax1.plot(  # type: ignore
        normalize(plotting_data.animal_amount),
        label="Amount of animals",
        color="#da3b56",
    )
    ax1.set_xlabel("Simulation time")  # type: ignore
    ax1.set_ylabel("Amount of food and animals")  # type: ignore
    ax1.set_ylim(ax1.get_ylim()[0], 1.2)
    _add_legend(ax1, columns=2)
    ax1.grid(axis="x", linestyle="--", linewidth=1)  # type: ignore

    ax3.plot(  # type: ignore
        normalize(smooth(plotting_data.food_energy, window=15)),
        label="Food energy",
        color="#6F7B75",
    )
    ax3.plot(  # type: ignore
        normalize(smooth(plotting_data.size, window=3)),
        label="Animal size",
        color="#da3b56",
    )
    ax3.set_xlabel("Simulation time")  # type: ignore
    ax3.set_ylabel("Animal size and energy")  # type: ignore
    ax3.set_ylim(ax3.get_ylim()[0], 1.15)
    _add_legend(ax3, columns=2)
    ax3.grid(axis="x", linestyle="--", linewidth=1)  # type: ignore

    ax2.plot(  # type: ignore
        normalize(plotting_data.vision), label="Animal vision", color="#da3b56"
    )
    ax2.plot(  # type: ignore
        normalize(plotting_data.speed), label="Animal speed", color="#213cc1"
    )
    ax2.set_xlabel("Simulation time")  # type: ignore
    ax2.set_ylabel("Animal stats")  # type: ignore
    ax2.set_ylim(ax2.get_ylim()[0], 1.1)
    _add_legend(
        ax2,
        columns=5,
        columnspacing=0.7,
        handletextpad=0.3,
    )
    ax2.grid(axis="x", linestyle="--", linewidth=1)  # type: ignore

    ax4.plot(plotting_data.energy_loss, color="#da3b56", label="Animal energy loss")  # type: ignore
    ax4.set_xlabel("Simulation time")  # type: ignore
    ax4.set_ylabel("Animal energy loss")  # type: ignore
    ax4.grid(axis="x", linestyle="--", linewidth=1)  # type: ignore
    _add_legend(ax4, columns=1)

    fig.savefig(output_filename)  # type: ignore


def _add_legend(axes, columns: int, **kwargs: Any):  # type: ignore
    axes.legend(  # type: ignore
        fontsize="small",
        loc="upper center",
        labelspacing=0.1,
        handlelength=1,
        ncol=columns,
        bbox_to_anchor=(0.5, 1.05),
        fancybox=True,
        shadow=True,
        **kwargs,
    )


def normalize(data: List[float]) -> List[float]:
    """Returns data with a max value of 1 (not fully normalized between 1 and 0)"""
    max_ = max(data)
    return [x / max_ for x in data]


def smooth(data: List[float], window: int = 5) -> List[float]:
    """Averages data over the specified window (the larger, the smoother)"""
    deque_: Deque[float] = deque(maxlen=window)
    new_data: List[float] = []
    for point in data:
        deque_.append(point)
        new_data.append(statistics.mean(deque_))
    return new_data
