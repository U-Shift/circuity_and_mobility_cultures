# The Relation between Circuity and Mobility Cultures: A Study of 41 European Cities

This repository consist of the source code used for producing the results in the paper:

Costa, M., Valença, G., Adorean, C., Moura, F. (2025). _The Relation between Circuity and Mobility Cultures: A Study of 41 European Cities_. Cities

### Abstract

Street network configuration shapes travel behavior, network performance, and accessibility. Analyzing how physical space relates to transportation becomes vital to assessing transportation systems and planning improvements. Such an assessment can be performed by evaluating the efficiency of the network through different metrics. Within these, circuity measures the ratio between the road network and straight-line distances. This work analyzes and compares circuity for walking, cycling, and driving networks across 41 European cities. Concurrently, we identify cities' mobility cultures (socio-cultural constructs related to mobility) to identify differences between cities' circuities and mobility patterns.

Data-driven methods were employed to cluster cities into six groups according to their mobility culture: _Cycling Champion Cities_, _Sustainable Transportation Advocates_, _Multimodal Metropolises_, _Car Dependent Cities_, _Walking Conducive Cities_, and _Pro Transit Cities_. Both intra- and inter-city differences were discovered for average circuity levels, and statistical differences were found between different clusters’ circuity values. _Car Dependent Cities_ had the worst circuity levels across the three transport modes; _Sustainable Transport Advocates_ had the lowest circuity overall; and _Cycling Champions Cities_ exhibited low levels of circuity for cycling and walking but high for driving.

Results show how circuity varies between European cities and their mobility cultures, drawing attention to how different types of urban street networks are correlated to cities’ mobility constructs. Further, this work poses a benchmark for cities, e.g., cities aspiring to be _Sustainable Transportation Advocates_ can use such an approach to understand how such cities’ networks are constructed and how urban structure is related to network efficiency. 

### Keywords

Circuity, Mobility Culture, Urban Street Networks, Europe


### Code:

Use `01-extract_maps_cities.ipynb` to extract cities bounding boxes from OSM map extracts. 

Use `02-view_cities.ipynb` to plot the cities to a map.

Use `03-sample_points_cities.ipynb` to sample points randomly from each selected city.

Use `04-sample_points_cities-on_streets.ipynb` to sample points randomly from each selected city, but points are located on streets/edges and number of points depend on total kms of roads in each city.

Use `05-simulate_routes.py` to simulate the routes for each city and the sampled points.

Use `06-eda_circuity.ipynb` to perform some EDA on the simulated trips. Create images about circuity values for each mode, trip distance, and city. Generate a final circuity metrics csv file, with different metrics for each city.

Use `07-plot_routes.ipynb` to plot some of the simulated routes.

Use `08-clusters.ipynb` to analyse the mobility culture cultures and their relation with cities' circuities.

### Data

`cities/` Contains data specific for each city, including city limits, OSM map extracts, and mobility culture data.

`city_points-on_streets/` Contains data on points generated for route simulation for all cities.

`simulated_routes-on_streets/` Contains data on the simulated routes for all cities and all transport modes.


### Cite

If you find this useful, consider citing the associated paper:

```
@article{costa2025relation,
  author={Costa, Miguel and Valença, Gabriel and Adorean, Cristian and and Moura, Filipe},
  journal={Cities}, 
  title={The Relation between Circuity and Mobility Cultures: A Study of 41 European Cities}, 
  year={2025},
}
```
