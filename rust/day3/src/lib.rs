use std::error::Error;
use std::fs;
use regex::Regex;
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

#[derive(Debug, Hash, Eq, PartialEq)]
pub struct Point {
    x: i32,
    y: i32,
}

impl Point {
    pub fn new(x: i32, y: i32) -> Self {
        Self { x, y, }
    }
}

#[derive(Debug, PartialEq)]
pub struct Rectangle {
    top_left: Point,
    bottom_right: Point,
}

impl Rectangle {
    pub fn new(top_left: Point, bottom_right: Point) -> Self {
        Self { top_left, bottom_right, }
    }

    pub fn area(&self) -> i32 {
        let width = self.bottom_right.x - self.top_left.x;
        let height = self.bottom_right.y - self.top_left.y;
        width * height
    }
}

#[derive(Debug, PartialEq)]
pub struct Claim {
    id: String,
    rectangle: Rectangle,
}

impl Claim {
    pub fn from_str(raw_value: &str) -> Option<Self> {
        let re = Regex::new(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$").unwrap();
        let captures = re.captures(raw_value);
        match captures {
            Some(c) => {
                let id = String::from(&c[1]);
                let x = *&c[2].parse::<i32>().unwrap();
                let y = *&c[3].parse::<i32>().unwrap();
                let top_left = Point::new(x, y);

                let width = *&c[4].parse::<i32>().unwrap();
                let height = *&c[5].parse::<i32>().unwrap();
                let bottom_right = Point::new(x + width, y + height);

                let rectangle = Rectangle::new(top_left, bottom_right);
                let claim = Self { id, rectangle };

                Some(claim)
            },
            None => None,
        }
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.filename)?;

    match config.part {
        Part::Part1 => {
            let claims = parse_claims(&contents).unwrap();
            let result = part1(&claims);
            println!("{}", result);
        }
        Part::Part2 => {
            // TODO: Part 2
        }
    }

    Ok(())
}

fn parse_claims(contents: &str) -> Option<Vec<Claim>> {
    contents
        .lines()
        .map(|l| Claim::from_str(l.trim()))
        .collect()
}

fn part1(claims: &Vec<Claim>) -> i32 {
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_claim() {
        let raw_claim = "#1 @ 1,3: 4x4";
        let expected = Claim {
            id: String::from("1"),
            rectangle: Rectangle::new(Point::new(1, 3), Point::new(5, 7)),
        };

        assert_eq!(Some(expected), Claim::from_str(raw_claim));
    }

    #[test]
    fn parse_valid_large_claim() {
        let raw_claim = "#123 @ 10,100: 50x5";
        let expected = Claim {
            id: String::from("123"),
            rectangle: Rectangle::new(Point::new(10, 100), Point::new(60, 105)),
        };

        assert_eq!(Some(expected), Claim::from_str(raw_claim));
    }

    #[test]
    fn rectangle_area() {
        let top_left = Point::new(10, 10);
        let bottom_right = Point::new(15, 15);
        let rectangle = Rectangle::new(top_left, bottom_right);

        assert_eq!(25, rectangle.area());
    }

    #[test]
    fn part1_test() {
        let claims = vec![
            Claim::from_str("#1 @ 1,3: 4x4").unwrap(),
            Claim::from_str("#2 @ 3,1: 4x4").unwrap(),
            Claim::from_str("#3 @ 5,5: 2x2").unwrap(),
        ];

        assert_eq!(1, part1(&claims));
    }
}
