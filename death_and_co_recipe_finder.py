""" Module to find certain Death and Co Recipes"""
import argparse

from typing import Any, Dict, List, Optional


import sys
import pandas as pd

#######################################################################################################################
###### Constants
#######################################################################################################################

ORIGINAL_RECIPES = pd.read_csv("death_and_co_categorical_recipes.tsv", sep='\t')
ORIGINAL_RECIPES = ORIGINAL_RECIPES.where(pd.notnull(ORIGINAL_RECIPES), None)

ALL_INGREDIENTS = ORIGINAL_RECIPES.columns.tolist()[7:-2]

GROUPS = [
    "syrup",
    "bitters",
    "mix",
    "lemon",
    "lime",
    "orange",
    "grapefruit",
    "brandy",
    "champagne",
    "vodka",
    "mezcal",
    "tequila",
    "cognac",
    "pisco",
    "gin",
    "aquavit",
    "rum",
    "whiskey",
    "scotch",
    "bourbon",
    "rye",
    "absinthe",
    "rosé",
    "sherry",
    "vermouth",
    "cider",
    "beer",
    "liqueur",
    "amaro",
    "amaretto",
    "campari",
    "cointreau",
    "curacao",
    "chartreuse",
    "aperitif",
    "cordial",
    "gastrique",
    "soda"
]
GROUPS = [group.title() for group in GROUPS]


GROUP_TO_INGREDIENT_DICT = {}
available_ingredients = ALL_INGREDIENTS
GROUPED_INGREDIENTS = []
for group in GROUPS:
    GROUP_TO_INGREDIENT_DICT[group] = [ingredient for ingredient in available_ingredients if group in ingredient]
    available_ingredients = [ingredient for ingredient in available_ingredients if group not in ingredient]
    GROUPED_INGREDIENTS += GROUP_TO_INGREDIENT_DICT[group]
    
UNGROUPED_INGREDIENTS = sorted(set(ALL_INGREDIENTS) - set(GROUPED_INGREDIENTS))

INGREDIENT_TO_GROUP_DICT = {ingredient: group for group, ingredient_list in GROUP_TO_INGREDIENT_DICT.items()
                            for ingredient in ingredient_list}

#######################################################################################################################
###### Functions
#######################################################################################################################


def split_ingredients_into_group_and_specific(ingredients):
    """"""
    group_ingredients = []
    specific_ingredients = []
    
    for ingredient in ingredients:
        if any(ingredient.lower() == group.lower() for group in GROUPS):
            group_ingredients.append(ingredient.lower())
        else:
            specific_ingredients.append(ingredient.lower())

    return group_ingredients, specific_ingredients

class Ingredient:
    def __init__(self, name: str, amount: Optional[str] = None):
        self.name = name
        self.group = INGREDIENT_TO_GROUP_DICT.get(name, None)
        self.amount = amount
    
    def __repr__(self):
        if self.group:
            s = f"{self.group} | {self.name}"
        else:
            s = self.name

        if self.amount:
            s += f" | {self.amount}"
        return s
    
    def __lt__(self, other):
        if other.group == self.group:
            return self.name < other.name
        
        if not other.group:
            return True
        
        if not self.group:
            return False
        
        return self.group < other.group


class Recipe:
    def __init__(self, row):
        self.name = row["Name"]
        self.page = row["Page #"]
        self.glass = row["Glass"]
        self.method = row["Method"]
        self.special = row["Muddle/Egg/Other"]
        self.twist = row["Twist"]
        self.garnish = row["Garnish"]
        
        if self.garnish == '←':
            self.garnish = None
        
        row = row.dropna().to_dict()
        self.ingredients = []
        for item, amount in row.items():
            if item in ["Name", "Page #", "Glass", "Method", "Muddle/Egg/Other", "Twist", "Garnish"]:
                continue
            self.ingredients.append(Ingredient(item, amount=amount))
            
        self.ingredients = sorted(self.ingredients)
        self.ingredient_groups = []
        for ingredient in self.ingredients:
            if ingredient.group not in self.ingredient_groups and ingredient.group:
                self.ingredient_groups.append(ingredient.group)
                
    def has_group_ingredient(self, given_group: str) -> bool:
        """"""
        return any(group.lower() == given_group.lower() for group in self.ingredient_groups)
    
    def has_specific_ingredient(self, given_ingredient: str) -> bool:
        """"""
        return any(ingredient.name.lower() == given_ingredient.lower() for ingredient in self.ingredients)
    
    def all_ingredients_available(self, *ingredients):
        """"""
        group_ingredients, specific_ingredients = split_ingredients_into_group_and_specific(ingredients)
        group_ingredients = [group_ingredient.lower() for group_ingredient in group_ingredients]
        specific_ingredients = [specific_ingredient.lower() for specific_ingredient in specific_ingredients]
        for ingredient in self.ingredients:
            if ingredient.group and ingredient.group.lower() in group_ingredients:
                continue

            if not ingredient.name.lower() in specific_ingredients:
                return False

        return True
            
    def __lt__(self, other):
        return self.name < other.name
    
    def __repr__(self):
        s = f"\n{self.name} ({self.method} | {self.glass} | Page {self.page}):\n"
        for ingredient in self.ingredients:
            s += f"   {ingredient}\n"
            
        if self.special:
            s += f"   Muddle/Egg/Other | {self.special}\n"
        
        if self.twist:
            s += f"   Twist | {self.twist}\n"
        
        if self.garnish:
            s += f"   Garnish | {self.garnish}\n"
            
        return s + "\n"


RECIPES = [Recipe(row) for i, row in ORIGINAL_RECIPES.iterrows()]

#######################################################################################################################
###### Functions
#######################################################################################################################


def search_for_recipe(*ingredients):
    """"""
    group_ingredients, specific_ingredients = split_ingredients_into_group_and_specific(ingredients)

    found_recipes = []
    for recipe in RECIPES:        
        if not all(recipe.has_group_ingredient(group_ingredient) for group_ingredient in group_ingredients):
            continue

        if not all(recipe.has_specific_ingredient(specific_ingredient) for specific_ingredient in specific_ingredients):
            continue
        
        found_recipes.append(recipe)
    return found_recipes


def find_possible_recipes(*ingredients):
    """"""
    return [recipe for recipe in RECIPES if recipe.all_ingredients_available(*ingredients)]


#######################################################################################################################
###### Functions
#######################################################################################################################


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--possible-recipes', dest='possible_recipes', action='store_true',
                        help="Show all possible recipes given a list of bar ingredients")
    parser.add_argument('--recipes-containing', dest='recipes_containing', action='store_true',
                        help="Show recipes containing these ingredients.")
    parser.add_argument('-i', "--ingredients", nargs='+', default=[],
                    help='Ingredients to find recipes with.')


    args = parser.parse_args()


    assert len(args.ingredients) > 0, "No ingredients provided.  Please give ingredients with --ingredients"

    if args.possible_recipes and args.recipes_containing:
        raise ValueError("Both modes selected (--possible-recipes and --recipes-containing) , choose one.")

    elif not args.possible_recipes and not args.recipes_containing:
        raise ValueError("Must select a mode: --possible-recipes or --recipes-containing.")

    elif args.possible_recipes:
        possible_recipes = find_possible_recipes(*args.ingredients)
        if len(possible_recipes) == 0:
            print(f"No valid recipes were found for these ingredients: {args.ingredients}")
        else:
            for recipe in possible_recipes:
                print(recipe)

    else:
        recipes_containing = search_for_recipe(*args.ingredients)
        if len(recipes_containing) == 0:
            print(f"No valid recipes were found for these ingredients: {args.ingredients}")
        else:
            for recipe in recipes_containing:
                print(recipe)






if __name__ == '__main__':
    main()