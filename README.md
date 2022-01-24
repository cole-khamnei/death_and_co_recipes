# Death and Co. Recipe Finder
## How to use:

### Get recipe ideas with a few ingredients:
To find a list of recipes that contain a list of ingredients (in this case `rum` and `amaro`):

```
python death_and_co_recipe_finder.py --recipes-containing --ingredients rum amaro
```

Example output:
```
The Black Prince (Stirred | Coupe | Page 267):
   Amaro | Amaro Averna | 1/2 oz
   Bitters | Orange Bitters | 1 dash
   Rum | Zacapa 23-Year Rum | 2 oz
   Punt E Mes | 3/4 oz

```

### Get possible recipes given a bar:
Given a `bar` (list of ingredients) find all posssible recipes. In this example the bar consists of `mezcal`, `lime`, `tequila`, and `syrup`.

```
python death_and_co_recipe_finder.py --possible-recipes --ingredients mezcal lime tequila syrup
```
Example output:
```
Zihuatanejo Julep (Stirred | Julep Tin | Page 244):
   Mezcal | Del Maguey Chichicapa Mezcal | 1/2 oz
   Syrup | Demerara Syrup | 1 tsp
   Tequila | El Tesoro Reposado Tequila | 2 oz
   Muddle/Egg/Other | 1 Mint Sprig
   Garnish | 1 Cinnamon Stick and 1 Mint Bouquet

```

# Death and Co. Recipe Analysis

[link to Death and Co Recipe Book!](https://www.deathandcompany.com/)


![GitHub Logo](/plots/ingredient_occurences.png)

![GitHub Logo](/plots/glass_occurences.png)