use std::io::BufRead;
use std::io::BufReader;
use std::path::Path;
use std::vec::Vec;

mod common;
mod day01;
mod day02;

const SOLVERS: [(&str, common::SolverFn); 2] = [("01", day01::solve), ("02", day02::solve)];

fn read_lines<P: AsRef<Path>>(filepath: P) -> std::io::Result<Vec<String>> {
    let file = std::fs::File::open(filepath)?;
    let buf_reader = BufReader::new(file);
    let mut lines = Vec::new();
    for line in buf_reader.lines() {
        lines.push(line?);
    }
    Ok(lines)
}

fn concat(s: &str, t: &str) -> String {
    let mut result = s.to_owned();
    result.push_str(t);
    result
}

fn answers_to_lines(answers: &(String, String)) -> String {
    let mut result = String::with_capacity(answers.0.len() + 1 + answers.1.len() + 1);
    result.push_str(&answers.0);
    result.push('\n');
    result.push_str(&answers.1);
    result.push('\n');
    result
}

fn main() {
    let testdata_dir = Path::new("testdata");
    for (name, solver) in &SOLVERS {
        let input_filename = testdata_dir.join(concat(name, ".in"));
        let output_filename = testdata_dir.join(concat(name, ".out"));
        let input = read_lines(input_filename).unwrap();
        let expected_output = std::fs::read_to_string(output_filename).unwrap();
        let answers = solver(input).unwrap();
        let received_output = answers_to_lines(&answers);
        if expected_output != received_output {
            println!(
                "Invalid output for problem {}!\nExpected:\n{}\nReceived:\n{}",
                name, expected_output, received_output
            );
        }
    }
}
