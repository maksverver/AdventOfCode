use std::vec::Vec;

pub fn solve(input: Vec<String>) -> Result<(String, String), ::common::Error> {
    let numbers: Vec<i32> = ::common::parse_i32s(input)?;

    let answer1: i32 = numbers.iter().sum();

    /*
        let answer2: i32 = {
            let mut seen = std::collections::HashSet::new();
            let mut running_total = 0;
            numbers
                .iter()
                .cycle()
                .find_map(|&number| {
                    running_total += number;
                    if seen.insert(running_total) {
                        None
                    } else {
                        Some(running_total)
                    }
                }).unwrap()
        };
    */
    let answer2: i32 = {
        let mut seen = std::collections::HashSet::new();
        let mut running_total = 0;
        'outer: loop {
            for &number in numbers.iter() {
                running_total += number;
                if !seen.insert(running_total) {
                    break 'outer running_total;
                }
            }
        }
    };

    Ok((answer1.to_string(), answer2.to_string()))
}
