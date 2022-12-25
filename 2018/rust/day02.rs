use std::collections::HashMap;

fn part1(ids: &Vec<String>) -> i32 {
    let mut samples_with_doubles = 0;
    let mut samples_with_triples = 0;
    for id in &*ids {
        let mut freq = HashMap::new();
        for ch in id.chars() {
            *freq.entry(ch).or_insert(0) += 1;
        }
        let mut have_double = false;
        let mut have_triple = false;
        for &val in freq.values() {
            if val == 2 {
                have_double = true;
            }
            if val == 3 {
                have_triple = true;
            }
        }
        samples_with_doubles += have_double as i32;
        samples_with_triples += have_triple as i32;
    }
    samples_with_doubles * samples_with_triples
}

fn part2(ids: &Vec<String>) -> Result<String, ::common::Error> {
    for s in &*ids {
        // TODO: should not loop over each pair twice!
        for t in &*ids {
            assert!(s.len() == t.len());
            let mut differences = 0;
            for (a, b) in s.chars().zip(t.chars()) {
                if a != b {
                    differences += 1;
                    if differences > 1 {
                        break;
                    }
                }
            }
            if differences == 1 {
                let mut result = String::with_capacity(s.len() - 1);
                for (a, b) in s.chars().zip(t.chars()) {
                    if a == b {
                        result.push(a);
                    }
                }
                return Ok(result);
            }
        }
    }
    Err(::common::Error::NoSolution())
}

pub fn solve(input: Vec<String>) -> Result<(String, String), ::common::Error> {
    Ok((part1(&input).to_string(), part2(&input)?.to_string()))
}
