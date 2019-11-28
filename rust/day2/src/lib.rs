use std::collections::HashMap;
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
            let result = part1(&contents);
            println!("{}", result);
        }
        Part::Part2 => {
            let result = part2(&contents);
            println!("{:?}", result);
        }
    }

    Ok(())
}

pub fn part1(input: &str) -> i32 {
    let (two_total, three_total) = input.lines().fold((0, 0), |(x, y), l| {
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

        match (has_two, has_three) {
            (true, true) => (x + 1, y + 1),
            (true, false) => (x + 1, y),
            (false, true) => (x, y + 1),
            (false, false) => (x, y),
        }
    });

    two_total * three_total
}

pub fn part2(input: &str) -> Option<String> {
    let lines: Vec<&str> = input.lines().collect();
    for (skip, &line) in lines.iter().enumerate() {
        for &other_line in lines.iter().skip(skip) {
            if line.len() != other_line.len() {
                continue;
            }

            let id = line.chars()
                .zip(other_line.chars())
                .filter_map(|(c, other_char)| {
                    if c == other_char {
                        Some(c)
                    } else {
                        None
                    }
                })
                .collect::<String>();

            if id.len() == line.len() - 1 {
                return Some(id);
            }
        }
    }

    None
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

    #[test]
    fn part2_test() {
        let contents = "\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz";

        assert_eq!(Some(String::from("fgij")), part2(&contents));
    }
}
