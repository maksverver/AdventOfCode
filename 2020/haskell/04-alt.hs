import Data.Char
import Data.List
import Data.List.Split
import Data.Maybe

data Passport a = Passport {byr :: a, iyr :: a, eyr :: a, hgt :: a, hcl :: a, ecl :: a, pid :: a} deriving Show

parsePassport :: [String] -> Passport (Maybe String)
parsePassport = foldl' update emptyPassport
    where
        emptyPassport = Passport{byr=Nothing, iyr=Nothing, eyr=Nothing, hgt=Nothing, hcl=Nothing, ecl=Nothing, pid=Nothing}

        update p@Passport{byr=Nothing} ('b':'y':'r':':': s) = p{byr=Just s}
        update p@Passport{iyr=Nothing} ('i':'y':'r':':': s) = p{iyr=Just s}
        update p@Passport{eyr=Nothing} ('e':'y':'r':':': s) = p{eyr=Just s}
        update p@Passport{hgt=Nothing} ('h':'g':'t':':': s) = p{hgt=Just s}
        update p@Passport{hcl=Nothing} ('h':'c':'l':':': s) = p{hcl=Just s}
        update p@Passport{ecl=Nothing} ('e':'c':'l':':': s) = p{ecl=Just s}
        update p@Passport{pid=Nothing} ('p':'i':'d':':': s) = p{pid=Just s}
        update p                       ('c':'i':'d':':': _) = p
        update p                       s                    = error ("Invalid field " ++ show s ++ " for passport " ++ show p)

getComplete :: Passport (Maybe String) -> Maybe (Passport String)
getComplete Passport{byr=Just byr, iyr=Just iyr, eyr=Just eyr, hgt=Just hgt, hcl=Just hcl, ecl=Just ecl, pid=Just pid} =
    Just Passport{byr=byr, iyr=iyr, eyr=eyr, hgt=hgt, hcl=hcl, ecl=ecl, pid=pid}
getComplete _ = Nothing

isValid :: Passport String -> Bool
isValid Passport{byr=byr, iyr=iyr, eyr=eyr, hgt=hgt, hcl=hcl, ecl=ecl, pid=pid} =
    between 1920 2002 (read byr) &&
    between 2010 2020 (read iyr) &&
    between 2020 2030 (read eyr) &&
    validHeight hgt &&
    validHairColor hcl &&
    validEyeColor ecl &&
    validPassportId pid
    where
        between lo hi value = lo <= value && value <= hi

        validHeight s =
            (unit == "cm" && between 150 193 value) ||
            (unit == "in" && between 59 76 value )
            where
                (s', unit) = splitAt (length s - 2) s
                value = read s'
                
        validHairColor ('#':s) = length s == 6 && all isHexDigit s  -- note: accepts uppercase too
        validHairColor _       = False

        validEyeColor s = s `elem` ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

        validPassportId s = length s == 9 && all isDigit s

main = do
    input <- getContents
    let allPassports = map (parsePassport . words) $ splitOn "\n\n" input
    let completePassports = mapMaybe getComplete allPassports
    let validPassports = filter isValid completePassports
    print (length completePassports)
    print (length validPassports)
