from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .builder import PlotBuilder

class LabelBuilder:
    def __init__(self, plot_builder: PlotBuilder):
        """Starts a LabelBuilder. Used to modify axis labels.

        Args:
            plot_builder (PlotBuilder): PlotBuilder to return when exit.
        """
        self._plot_builder_ = plot_builder
        
        
    def start_x_label(self, label):
        """Starts a x label builder.

        Args:
            label (str): x axis label.

        Returns:
            (itfit.plot.labels.xLabelBuilder): x label builder.
        """
        return xLabelBuilder(self._plot_builder_, self,  label)
        
    def start_y_label(self, label):
        """Starts a y label builder.

        Args:
            label (str): y axis label.

        Returns:
            (itfit.plot.labels.yLabelBuilder): y label builder.
        """
        return yLabelBuilder(self._plot_builder_, self, label)
        
    def end_labels(self):
        """Exits labels builder.

        Returns:
            (itft.plot.PlotBuilder): Returns the PlotBuilder.
        """
        return self._plot_builder_

class GenericLabelBuilder:
    def __init__(self, plot_builder: PlotBuilder, label: str):
        """Abstract label builder. Use xLabelBuilder, yLabelBuilder or titleLabelBuilder.

        Args:
            plot_builder (itfit.plot.PlotBuilder): PlotBuilder instance.
            label (str): Label string.
        """
        self._plot_builder_ = plot_builder
        self._label_ = label
        self._dict_: dict[str, object] = {}

    def fontsize(self, size):
        """Sets label fontsize.

        Args:
            size (float): Size of the label.

        Returns:
            (itfit.plot.labels.GenericLabelBuilder): Returns itself.
        """
        self._dict_.update({'fontsize': size})
        return self

    def fontweight(self, weight):
        """TODO:

        Args:
            weight (_type_): _description_

        Returns:
            (itfit.plot.labels.GenericLabelBuilder): Returns itself.
        """
        self._dict_.update({'fontweight': weight})
        return self

    def color(self, color):
        """Sets the color of the label.

        Args:
            color (str|tuple[float]): Color for the label.

        Returns:
            (itfit.plot.labels.GenericLabelBuilder): Returns itself.
        """
        self._dict_.update({'color': color})
        return self

    def verticalalignment(self, loc):
        """TODO:

        Args:
            loc (_type_): _description_

        Returns:
            (itfit.plot.labels.GenericLabelBuilder): Returns itself.
        """
        self._dict_.update({'verticalalignment': loc})
        return self

    def horizontalalignment(self, loc):
        """TODO

        Args:
            loc (_type_): _description_

        Returns:
            (itfit.plot.labels.GenericLabelBuilder): Returns itself.
        """
        self._dict_.update({'horizontalalignment': loc})
        return self

class xLabelBuilder(GenericLabelBuilder):
    """Specific implementation of GenericLabelBuilder for x label.
    """
    def __init__(self, plot_builder: PlotBuilder, label_builder: LabelBuilder, label: str):
        super().__init__(plot_builder, label)
        self._label_builder_ = label_builder

    def end_xlabel(self):
        """Ends x label builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        self._plot_builder_.ax.set_xlabel(self._label_, self._dict_)
        return self._label_builder_

class yLabelBuilder(GenericLabelBuilder):
    """Specific implementation of GenericLabelBuilder for y label.
    """
    def __init__(self, plot_builder, label_builder: LabelBuilder, label: str):
        super().__init__(plot_builder, label)
        self._label_builder_ = label_builder

    def end_ylabel(self):
        """Ends y label builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        self._plot_builder_.ax.set_ylabel(self._label_, self._dict_)
        return self._label_builder_

class titleLabelBuilder(GenericLabelBuilder):
    """Specific implementation of GenericLabelBuilder for the title label.
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