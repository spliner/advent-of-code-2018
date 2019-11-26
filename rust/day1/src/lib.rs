use std::num::ParseIntError;
use std::fs;
use std::error::Error;
use std::collections::HashSet;

pub enum Part {
    Part1,
    Part2,
}

impl Part {
    pub fn new(raw_value: String) -> Result<Self, String> {
        match raw_value.to_lowercase().as_str() {
            "part1" => Ok(Part::Part1),
            "part2" => Ok(Part::Part2),
            _ => Err(format!("Invalid part: {}", raw_value)),
        }
    }
}

pub struct Config {
    pub filename: String,
    pub part: Part,
}

impl Config {
    pub fn new(mut args: std::env::Args) -> Result<Config, String> {
        args.next();

        let part = match args.next() {
            Some(raw_part) => {
                match Part::new(raw_part) {
                    Ok(p) => p,
                    Err(e) => return Err(e),
                }
            },
            None => return Err(String::from("Didn't get a part")),
        };

        let filename = match args.next() {
            Some(arg) => arg,
            None => return Err(String::from("Didn't get a file name")),
        };

        Ok(Config { filename, part, })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.filename)?;
    let frequencies = parse_frequencies(&contents)?;

    match config.part {
        Part::Part1 => {
            let final_frequency = calculate_frequency(&frequencies);

            println!("{}", final_frequency);
        },
        Part::Part2 => {
            match calculate_repeating_frequency(&frequencies) {
                Some(f) => println!("{}", f),
                None => println!("Invalid frequency vector"),
            }
        }
    }

    Ok(())
}

pub fn parse_frequencies(contents: &str) -> Result<Vec<i32>, ParseIntError> {
    contents.lines().map(|line| line.trim().parse()).collect()
}

pub fn calculate_frequency(frequencies: &Vec<i32>) -> i32 {
    frequencies.iter().sum()
}

pub fn calculate_repeating_frequency(frequencies: &Vec<i32>) -> Option<i32> {
    if frequencies.len() == 0 {
        return None;
    }

    let frequency_iter = frequencies.iter().cycle();
    let mut current_frequency = 0;

    let mut frequency_set = HashSet::new();
    frequency_set.insert(current_frequency);

    for frequency in frequency_iter {
        current_frequency += *frequency;
        if frequency_set.contains(&current_frequency) {
            break;
        }

        frequency_set.insert(current_frequency);
    }

    Some(current_frequency)
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

    #[test]
    fn calculate_repeating_frequency_empty_vec_should_return_none() {
        let frequencies: Vec<i32> = Vec::new();
        assert_eq!(None, calculate_repeating_frequency(&frequencies));
    }

    #[test]
    fn calculate_repeating_frequency_first_example_should_return_0() {
        let frequencies = vec![1, -1];
        assert_eq!(Some(0), calculate_repeating_frequency(&frequencies));
    }

    #[test]
    fn calculate_repeating_frequency_second_example_should_return_10() {
        let frequencies = vec![3, 3, 4, -2, -4];
        assert_eq!(Some(10), calculate_repeating_frequency(&frequencies));
    }

    #[test]
    fn calculate_repeating_frequency_third_example_should_return_5() {
        let frequencies = vec![-6, 3, 8, 5, -6];
        assert_eq!(Some(5), calculate_repeating_frequency(&frequencies));
    }

    #[test]
    fn calculate_repeating_frequency_fourth_example_should_return_14() {
        let frequencies = vec![7, 7, -2, -7, -4];
        assert_eq!(Some(14), calculate_repeating_frequency(&frequencies));
    }
}
