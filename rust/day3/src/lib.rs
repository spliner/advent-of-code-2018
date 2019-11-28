use std::error::Error;
use std::fs;

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
            // TODO: Part 1
        }
        Part::Part2 => {
            // TODO: Part 2
        }
    }

    Ok(())
}
