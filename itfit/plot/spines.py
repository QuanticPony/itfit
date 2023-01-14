# Copyright 2023 Unai Lería Fortea & Pablo Vizcaíno García

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .builder import PlotBuilder
    
class SpineBuilder:
    def __init__(self, plot_builder: PlotBuilder):
        """Spine builder. Used to modify plot spines.

        Args:
            plot_builder (itfit.plot.PlotBuilder): PlotBuilder instance.
        """
        self._plot_builder_ = plot_builder
        self._dict_: dict[str, object] = {}
    
    def start_left_spine(self):
        """Starts a left spine builder.

        Returns:
            (itift.plot.spines.leftSpineBuilder): left spine builder.
        """
        return leftSpineBuilder(self._plot_builder_, self)
        
    def start_right_spine(self):
        """Starts a right spine builder.

        Returns:
            (itift.plot.spines.rightSpineBuilder): right spine builder.
        """
        return rightSpineBuilder(self._plot_builder_, self)
        
    def start_top_spine(self):
        """Starts a top spine builder.

        Returns:
            (itift.plot.spines.topSpineBuilder): top spine builder.
        """
        return topSpineBuilder(self._plot_builder_, self)
        
    def start_bottom_spine(self):
        """Starts a bottom spine builder.

        Returns:
            (itift.plot.spines.bottomSpineBuilder): bottom spine builder.
        """
        return bottomSpineBuilder(self._plot_builder_, self)
        
    def end_spines(self):
        """Ends spine builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        return self._plot_builder_

class GenericSpineBuilder:
    def __init__(self, plot_builder: PlotBuilder, spine_builder: SpineBuilder):
        """Spine builder. Used to modify plot spines.

        Args:
            plot_builder (itfit.plot.spines.GenericSpineBuilder): GenericSpineBuilder instance.
        """
        self._plot_builder_ = plot_builder
        self._spine_builder_ = spine_builder
        self._dict_: dict[str, object] = {}
        
    def alpha(self, alpha: float):
        """Sets spines alpha.

        Args:
            alpha (float): alpha value

        Returns:
            (itfit.plot.spines.GenericSpineBuilder): Returns itself.
        """
        self._dict_.update({'alpha':alpha})
        return self

    def visible(self):
        """Sets spine visible.

        Returns:
            (itfit.plot.spines.GenericSpineBuilder): Returns itself.
        """
        self._dict_.update({'visible':True})
        return self
    
    def invisible(self):
        """Sets spine invisible.

        Returns:
            (itfit.plot.spines.GenericSpineBuilder): Returns itself.
        """
        self._dict_.update({'visible':False})
        return self

    def color(self, color):
        """Sets the color of the spine.

        Args:
            color (str|tuple[float]): Color for the spine.

        Returns:
            (itfit.plot.spines.GenericSpineBuilder): Returns itself.
        """
        self._dict_.update({'color': color})
        return self

    def linestyle(self, linestyle):
        """Changes spine linestyle.

        Args:
            linestyle (str): Spine linestyle.

        Returns:
            (itfit.plot.spines.GenericSpineBuilder): Returns itself.
        """
        self._dict_.update({'linestyle': linestyle})
        return self

    def linewidth(self, linewidth):
        """Changes spine linewidth.

        Args:
            linewidth (float): Spine linewidth.

        Returns:
            (itfit.plot.spines.GenericSpineBuilder): Returns itself.
        """
        self._dict_.update({'linewidth': linewidth})
        return self
    
    def _end_spine_builder(self, spine):
        self._plot_builder_.ax.spines[spine].set(**self._dict_)
        return self._spine_builder_


class leftSpineBuilder(GenericSpineBuilder):
    def __init__(self, plot_builder, spine_builder):
        super().__init__(plot_builder, spine_builder)
        self._spine = "left"
        
    def end_left_spine(self):
        """Ends left spine builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        return self._end_spine_builder(self._spine)
        
        
class rightSpineBuilder(GenericSpineBuilder):
    def __init__(self, plot_builder, spine_builder):
        super().__init__(plot_builder, spine_builder)
        self._spine = "right"
        
    def end_right_spine(self):
        """Ends right spine builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        return self._end_spine_builder(self._spine)
        
        
class topSpineBuilder(GenericSpineBuilder):
    def __init__(self, plot_builder, spine_builder):
        super().__init__(plot_builder, spine_builder)
        self._spine = "top"
        
    def end_top_spine(self):
        """Ends top spne builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        return self._end_spine_builder(self._spine)
        

class bottomSpineBuilder(GenericSpineBuilder):
    def __init__(self, plot_builder, spine_builder):
        super().__init__(plot_builder, spine_builder)
        self._spine = "bottom"
        
    def end_bottom_spine(self):
        """Ends bottom spine builder.

        Returns:
            (itfit.plot.PlotBuilder): Returns the PlotBuilder.
        """
        return self._end_spine_builder(self._spine)
        