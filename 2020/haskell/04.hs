import Data.Char
import Data.Default
import Data.List
import Data.List.Split
import Data.Maybe

data F = Absent | Present | Valid deriving (Eq, Show);
data Passport = Passport {byr :: F, iyr :: F, eyr :: F, hgt :: F, hcl :: F, ecl :: F, pid :: F} deriving Show

instance Default Passport where
    def = Passport{byr=Absent, iyr=Absent, eyr=Absent, hgt=Absent, hcl=Absent, ecl=Absent, pid=Absent}

parsePassport :: [String] -> Passport
parsePassport = foldl' update def
    where
        update p@Passport{byr = Absent} ('b':'y':'r':':': s) = p{byr = classify $ isValidByr s}
        update p@Passport{iyr = Absent} ('i':'y':'r':':': s) = p{iyr = classify $ isValidIyr s}
        update p@Passport{eyr = Absent} ('e':'y':'r':':': s) = p{eyr = classify $ isValidEyr s}
        update p@Passport{hgt = Absent} ('h':'g':'t':':': s) = p{hgt = classify $ isValidHgt s}
        update p@Passport{hcl = Absent} ('h':'c':'l':':': s) = p{hcl = classify $ isValidHcl s}
        update p@Passport{ecl = Absent} ('e':'c':'l':':': s) = p{ecl = classify $ isValidEcl s}
        update p@Passport{pid = Absent} ('p':'i':'d':':': s) = p{pid = classify $ isValidPid s}
        update p                         ('c':'i':'d':':': _) = p
        update p                         s                    = error ("Invalid field " ++ show s ++ " for passport " ++ show p)

        classify False = Present
        classify True  = Valid

        isValidByr byr = between 1920 2002 (read byr)

        isValidIyr iyr = between 2010 2020 (read iyr)
       
        isValidEyr eyr = between 2020 2030 (read eyr)
       
        isValidHgt hgt = 
            (unit == "cm" && between 150 193 value) ||
            (unit == "in" && between 59 76 value )
            where
                (s', unit) = splitAt (length hgt - 2) hgt
                value = read s'

        isValidHcl ('#':s) = length s == 6 && all isHexDigit s  -- note: accepts uppercase too
        isValidHcl _       = False

        isValidEcl s = s `elem` ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

        isValidPid s = length s == 9 && all isDigit s

        between lo hi value = lo <= value && value <= hi


fields Passport{byr=byr, iyr=iyr, eyr=eyr, hgt=hgt, hcl=hcl, ecl=ecl, pid=pid} =
    [byr, iyr, eyr, hgt, hcl, ecl, pid]

main = do
    input <- getContents
    let passports = map (parsePassport . words) $ splitOn "\n\n" input
    print $ countIf noFieldsAbsent passports
    print $ countIf allFieldsValid passports
    where 
        countIf pred = length . filter pred
        noFieldsAbsent = notElem Absent . fields
        allFieldsValid = all (== Valid) . fields
