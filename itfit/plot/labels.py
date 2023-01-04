from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .builder import PlotBuilder


class LabelBuilder:
    def __init__(self, plot_builder: PlotBuilder, label: str):
        """Abstract label builder. Use xLabelBuilder, yLabelBuilder or titleLabelBuilder.

        Args:
            plot_builder (itfit.plot.PlotBuilder): PlotBuilder instance.
            label (str): Label string.
        """
        self._plot_builder_ = plot_builder
        self._label_ = label
        self._dict_ = {}

    def fontsize(self, size):
        """Sets label fontsize.

        Args:
            size (float): Size of the label.

        Returns:
            (itfit.plot.labels.LabelBuilder): Returns itself.
        """
        self._dict_.update({'fontsize': size})
        return self

    def fontweight(self, weight):
        """TODO:

        Args:
            weight (_type_): _description_

        Returns:
            (itfit.plot.labels.LabelBuilder): Returns itself.
        """
        self._dict_.update({'fontweight': weight})
        return self

    def color(self, color):
        """Sets the color of the label.

        Args:
            color (str|Tuple[float]): Color for the label.

        Returns:
            (itfit.plot.labels.LabelBuilder): Returns itself.
        """
        self._dict_.update({'color': color})
        return self

    def verticalalignment(self, loc):
        """TODO:

        Args:
            loc (_type_): _description_

        Returns:
            (itfit.plot.labels.LabelBuilder): Returns itself.
        """
        self._dict_.update({'verticalalignment': loc})
        return self

    def horizontalalignment(self, loc):
        """TODO

        Args:
            loc (_type_): _description_

        Returns:
            (itfit.plot.labels.LabelBuilder): Returns itself.
        """
        self._dict_.update({'horizontalalignment': loc})
        return self

class xLabelBuilder(LabelBuilder):
    """Specific implementation of LabelBuilder for x label.
    """
    def __init__(self, plot_builder, label: str):
        super().__init__(plot_builder, label)

    def end_xlabel(self):
        """Ends x label builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        self._plot_builder_.ax.set_xlabel(self._label_, self._dict_)
        return self._plot_builder_

class yLabelBuilder(LabelBuilder):
    """Specific implementation of LabelBuilder for y label.
    """
    def __init__(self, plot_builder, label: str):
        super().__init__(plot_builder, label)

    def end_ylabel(self):
        """Ends y label builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        self._plot_builder_.ax.set_ylabel(self._label_, self._dict_)
        return self._plot_builder_

class titleLabelBuilder(LabelBuilder):
    """Specific implementation of LabelBuilder for the title label.
    """
    def __init__(self, plot_builder, label: str):
        super().__init__(plot_builder, label)

    def end_title(self):
        """Ends title label builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        self._plot_builder_.ax.set_title(self._label_, self._dict_)
        return self._plot_builder_