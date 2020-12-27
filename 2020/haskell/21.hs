import Data.Char
import Data.List
import Data.List.Split
import Data.Ord
import PairWiseAssociation
import SortedList

data Product = Product{allergens::[Allergen], ingredients::[Ingredient]} deriving Show

newtype Allergen = Allergen String deriving (Eq, Ord, Show)
newtype Ingredient = Ingredient String deriving (Eq, Ord, Show)

-- Note: assumes a product contains no duplicate ingredients or allergens!
parseProduct :: String -> Product
parseProduct line | last line == ')' = Product{ingredients=ingredients, allergens=allergens}
    where
        [a, b] = splitOn " (contains " (init line)
        ingredients = map Ingredient $ sort $ words a
        allergens = map Allergen $ sort $ splitOn ", " b

main = do
    input <- getContents
    let products = map parseProduct (lines input) :: [Product]
    let allIngredients = distinct $ concatMap ingredients products :: [Ingredient]
    let allAllergens = distinct $ concatMap allergens products :: [Allergen]

    let possibleIngredientsAndAllergens = [
            (intersectionAll [ingredients p | p <- products, a `elem` allergens p], a) |
            a <- allAllergens] :: [([Ingredient], Allergen)]

    -- Part 1
    let riskyIngredients = distinct $ concatMap fst possibleIngredientsAndAllergens :: [Ingredient]
    print $ length $ concatMap ((`difference` riskyIngredients) . ingredients) products

    -- Part 2
    let ingredientAllergens = solvePairs possibleIngredientsAndAllergens :: [(Ingredient, Allergen)]
    putStrLn $ intercalate "," [s | (Ingredient s, _) <- sortBy (comparing snd) ingredientAllergens]
