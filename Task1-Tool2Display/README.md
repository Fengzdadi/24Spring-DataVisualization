# Task1 Choose a visualization tool to display information about the position of amino acids in proteins

## Tool examples
The main tools can be divided into these categories: professional software, programming libraries and frameworks, online tools and services and some domain-specific tools.
Specifically, the following example:
### professional software:
+ [Tableau](https://www.tableau.com/)
+ [Microsoft power BI](https://www.microsoft.com/en-us/power-platform/products/power-bi)
### programming libraries and frameworks
+ [Matplotlib](https://matplotlib.org/)
+ [Seaborn](https://seaborn.pydata.org/)
+ [Plotly](https://plotly.com/)
+ [Bokeh](https://bokeh.org/)
+ [D3.js](https://d3js.org/)
### online tools and services
+ [Google Charts](https://developers.google.com/chart)
+ [Datawrapper](https://www.datawrapper.de/)
### domain-specific tools
+ GIS
+ [gephi](https://gephi.org/)

## Data
Protein position information among amino acids, the example as follows:

|      | a    | ……   | b    |
| ---- | ---- | ---- | ---- |
| 1    | 0.33 | ……   | 0.14 |
| ……   | ……   | ……   |      |
| 3    | 0.02 | ……   | 0.81 |


## Works
In this work, don't try low-code platform. Most of the work is done using python. So if you have any good example, happy to hear from you.
Because the performance of matplotlib is relatively poor (seaborn is mutually exclusive), I finally chose to use Plotly.

<img src=".\image\Plotly_result_graph.png" alt="image-20240409150610687" style="zoom:50%;" />

In this effect, it is mainly considered that when medical workers use it, they will most likely only focus on which amino acids exist in which sequences, and express the possible probability through color. The small column on the right is better displayed and has some selective display functions.