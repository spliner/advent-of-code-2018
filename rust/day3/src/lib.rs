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
    position: Point,
    width: i32,
    height: i32,
}

impl Rectangle {
    pub fn new(position: Point, width: i32, height: i32) -> Self {
        Self { position, width, height, }
    }

    pub fn all_points(&self) -> Vec<Point> {
        let mut points = Vec::new();

        for y in self.position.y..self.position.y + self.height {
            for x in self.position.x..self.position.x + self.width {
                points.push(Point::new(x, y));
            }
        }

        points
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
                let width = *&c[4].parse::<i32>().unwrap();
                let height = *&c[5].parse::<i32>().unwrap();
                let position = Point::new(x, y);
                let rectangle = Rectangle::new(position, width, height);
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
            // TODO: Part 1
        }
        Part::Part2 => {
            // TODO: Part 2
        }
    }

    Ok(())
}

pub fn part1(claims: &Vec<Claim>) -> i32 {
    let mut count = 0;
    let mut points: HashSet<Point> = HashSet::new();

    claims.iter()
        .flat_map(|c| c.rectangle.all_points())
        .for_each(|p| {
            if points.contains(&p) {
                println!("{:?}", &p);
            }
            if !points.insert(p) {
                count += 1;
            }
        });

    count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_claim() {
        let raw_claim = "#1 @ 1,3: 4x4";
        let expected = Claim {
            id: String::from("1"),
            rectangle: Rectangle::new(Point::new(1, 3), 4, 4),
        };

        assert_eq!(Some(expected), Claim::from_str(raw_claim));
    }

    #[test]
    fn parse_valid_large_claim() {
        let raw_claim = "#123 @ 123,323: 423x423";
        let expected = Claim {
            id: String::from("123"),
            rectangle: Rectangle::new(Point::new(123, 323), 423, 423),
        };

        assert_eq!(Some(expected), Claim::from_str(raw_claim));
    }

    #[test]
    fn rectangle_get_all_points() {
        let position = Point::new(3, 1);
        let rectangle = Rectangle::new(position, 4, 4);

        let expected = vec![
            Point::new(3, 1),
            Point::new(4, 1),
            Point::new(5, 1),
            Point::new(6, 1),
            Point::new(3, 2),
            Point::new(4, 2),
            Point::new(5, 2),
            Point::new(6, 2),
            Point::new(3, 3),
            Point::new(4, 3),
            Point::new(5, 3),
            Point::new(6, 3),
            Point::new(3, 4),
            Point::new(4, 4),
            Point::new(5, 4),
            Point::new(6, 4),
        ];

        assert_eq!(expected, rectangle.all_points())
    }

    #[test]
    fn part1_test() {
        let claims = vec![
            Claim::from_str("#1 @ 1,3: 4x4").unwrap(),
            Claim::from_str("#2 @ 3,1: 4x4").unwrap(),
            Claim::from_str("#3 @ 5,5: 2x2").unwrap(),
        ];

        assert_eq!(4, part1(&claims));
    }
}
