pyrca-web
---
A web API for the implementation of [pyrca]() library.

### API
#### Base URL:
https://pyrca-web-api.herokuapp.com

#### Usage
```<base-url>/<api-end-point>``` + json data


#### Beam Balanced Flexure Analysis
Endpoint: ```beam-balanced-analysis```

Json parameters:
```json
{
  "main_section": [[0, 0], [0, 500], [250, 500], [250, 0]],
  "fc_prime": 20.7,
  "fy": 276.5,
  "effective_depth": 460,
  "stress_distribution": 1
}
```

#### Definition:
- ```main_section``` - Array of nodes. Each node is defined by an array with 2 elements containing the ```x``` and ```y``` coordinate in millimeter.  
- ```fc_prime``` - Concrete compressive strength in MPa.
- ```fy``` - Steel tensile strength in MPa
- ```effective_depth``` Distance of centroid of tensile reinforcement from extreme compression fiber in millimeter.
- ```stress_distribution``` - 0 for parabolic (exact) and 1 for Whitney's rectangular representation block.
