# Firebreaks
Investigating Australia's recent brushfire season. 

## Inspiration

For anyone who has been following the recent season of Australian brushfires I found this article really illuminating: https://www.bbc.co.uk/news/amp/world-australia-50951043. It takes a look at how the fires have spread recently, some of the reasons why this season has been worse than usual, and what the cost of these brushfires have looked like over time. I’m interested in getting a sense for what past seasons looked like compared to today so I made the following visualization using GeoPandas.
## Result
![Recent Brushfire Distribution](https://github.com/danjizquierdo/Firebreaks/blob/master/images/aus_fires.gif?raw=true)
The background is a Kernel Density Estimation (KDE) to get a feel for what the probability distribution of the location of fires might look like. The color of each point is the temperature in Celsius of fires detected by satellites with over 90% confidence. For more information on how these fires were detected please visit https://firms.modaps.eosdis.nasa.gov/
## Further Questions
* Are the fires in recent years likely to have come from the same distribution as fires from past years?
* Have the intensity of fires changed over time?
* Can we see correlations with changes in time compared to exogenous variables like: mean temperature, average rainfall, global CO2 emission, etc?
