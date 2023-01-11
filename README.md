[![PyPI Downloads](https://img.shields.io/pypi/dm/itfit.svg?label=downloads)](https://pypi.org/project/itfit/)
[![PyPI Version](https://img.shields.io/pypi/v/itfit?)](https://pypi.org/project/itfit/)

![Commit activity](https://img.shields.io/github/commit-activity/m/QuanticPony/itfit)
[![License](https://img.shields.io/pypi/l/itfit)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/QuanticPony/itfit/ci-master.yml)](https://github.com/QuanticPony/itfit/actions)

[![Python Version](https://img.shields.io/pypi/pyversions/itfit)](https://pypi.org/project/itfit/)
[![Wheel](https://img.shields.io/pypi/wheel/itfit)](https://pypi.org/project/itfit/)

<br></br>
<h1 align="center">
Itfit
</h1>
<h2 align="center">
Interactive Fitter
</h2><br></br>
<h3 align="center">
Simple, intuitive and interactive application to help fitting common functions to your data.
</h3><br></br>



<div align="center">

<a href="https://quanticpony.github.io/itfit/">
<center><img src=https://img.shields.io/github/deployments/QuanticPony/itfit/github-pages?label=documentation></center>
</a>
<br></br>

</div>
<br></br>


```py
import matplotlib.pyplot as plt
import itfit

fitter = itfit.Fitter(xdata, ydata)
fitter()
plt.show()
```
<h3 align="center">
<img src="https://raw.githubusercontent.com/QuanticPony/itfit/master/docs/images/sample.gif" width="400" height="320" />
</h3>

```py

plot = fitter_app.default_plot_last_fit("x value", r"$\phi$ [s$^{-1}$]", "Itfit default plot")
plot.save_fig("figure.png")

```


<h3 align="center">
<img src="https://raw.githubusercontent.com/QuanticPony/itfit/master/docs/images/readme_figure.png" width="400" height="320" />
</h3>

# Instalation
Itfit releases are available as wheel packages on [PyPI](https://pypi.org/project/itfit/). You can install the last version using `pip`:
```
pip install itfit
```


# Documentation
Documentations is automatically generated from code on master push and hosted in github-pages [here](https://quanticpony.github.io/itfit/).

# Help
Just open an issue with the `question` tag ([or clic here](https://github.com/QuanticPony/itfit/issues/new?assignees=QuanticPony&labels=question&template=question.md&title=)) and we would love to help!

# Contributing
You can contribute with:
* Examples
* Documentation
* [Bug report/fix](https://github.com/QuanticPony/itfit/issues/new?assignees=QuanticPony&labels=bug&template=bug_report.md&title=)
* New fit functions
* [Features](https://github.com/QuanticPony/itfit/issues/new?assignees=QuanticPony&labels=new-feature&template=feature_request.md&title=)
* Code

Even only feedback is greatly apreciated. 

Just create an issue and let us know you want to help! 


# Licensing
**Itfit** is released under the **Apache License Version 2.0**.