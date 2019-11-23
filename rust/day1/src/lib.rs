use std::num::ParseIntError;
use std::fs;
use std::error::Error;

pub struct Config {
    pub filename: String,
}

impl Config {
    pub fn new(mut args: std::env::Args) -> Result<Config, &'static str> {
        args.next();

        let filename = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a file name"),
        };

        Ok(Config { filename, })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.filename)?;
    let frequencies = parse_frequencies(&contents)?;

    let final_frequency = calculate_frequency(&frequencies);

    println!("{}", final_frequency);

    Ok(())
}

pub fn parse_frequencies(contents: &str) -> Result<Vec<i32>, ParseIntError> {
    contents.lines().map(|line| line.trim().parse()).collect()
}

pub fn calculate_frequency(frequencies: &Vec<i32>) -> i32 {
    frequencies.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_frequencies_valid_input_should_be_successful() {
        let contents = "\
+1
-2
+3";
        assert_eq!(Ok(vec![1, -2, 3]), parse_frequencies(contents))
    }

    #[test]
    fn parse_frequencies_invalid_input_should_return_error() {
        let contents = "\
+1
-2
+3
invalid";

        let result = parse_frequencies(contents);
        assert_eq!(true, result.is_err());
    }

    #[test]
    fn calculate_frequencies_first_example_should_return_3() {
        let frequencies = vec![1, 1, 1];
        assert_eq!(3, calculate_frequency(&frequencies));
    }

    #[test]
    fn calculate_frequencies_second_example_should_return_0() {
        let frequencies = vec![1, 1, -2];
        assert_eq!(0, calculate_frequency(&frequencies));
    }

    #[test]
    fn calculate_frequencies_third_example_should_return_minus_6() {
        let frequencies = vec![-1, -2, -3];
        assert_eq!(-6, calculate_frequency(&frequencies));
    }
}
