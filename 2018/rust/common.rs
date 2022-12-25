use std::str::FromStr;
use std::vec::Vec;

pub type SolverFn = fn(Vec<String>) -> Result<(String, String), ::common::Error>;

fn parse_strings<T>(strings: Vec<String>) -> Result<Vec<T>, <T as FromStr>::Err>
where
    T: FromStr,
{
    let mut results: Vec<T> = Vec::new();
    for string in strings {
        results.push(string.parse()?);
    }
    Ok(results)
}

pub fn parse_i32s(strings: Vec<String>) -> Result<Vec<i32>, Error> {
    parse_strings(strings).or_else(|e| Err(Error::ParseIntError(e)))
}

#[derive(Debug)]
pub enum Error {
    ParseIntError(std::num::ParseIntError),
    NoSolution(),
}
