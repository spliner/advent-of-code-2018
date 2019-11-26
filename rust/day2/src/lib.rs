use std::error::Error;
use std::fs;
use std::collections::HashMap;

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
            Some(raw_part) => match Part::new(raw_part) {
                Ok(p) => p,
                Err(e) => return Err(e),
            },
            None => return Err(String::from("Didn't get a part")),
        };

        let filename = match args.next() {
            Some(arg) => arg,
            None => return Err(String::from("Didn't get a file name")),
        };

        Ok(Config { filename, part })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.filename)?;

    match config.part {
        Part::Part1 => {
            let result = part1(&contents);
            println!("{}", result);
        }
        Part::Part2 => {
            // TODO: Part 2
        }
    }

    Ok(())
}

pub fn part1(input: &str) -> i32 {
    let (two_total, three_total) = input.lines()
        .map(|l| {
            let mut map = HashMap::new();
            for c in l.chars() {
                let count = map.entry(c).or_insert(0);
                *count += 1;
            }

            let mut has_two = false;
            let mut has_three = false;
            for (_, v) in map {
                has_two = has_two || v == 2;
                has_three = has_three || v == 3;
            }

            (if has_two { 1 } else { 0 }, if has_three { 1 } else { 0 })
        })
        .fold((0, 0), |(two_count, three_count), (x, y)| {
            (two_count + x, three_count + y)
        });

    two_total * three_total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1_test() {
        let contents = "\
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab";

        assert_eq!(12, part1(contents));
    }
}
