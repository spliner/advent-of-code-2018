use std::error::Error;
use std::fs;
use regex::Regex;

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

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

impl Point {
    fn new(x: i32, y: i32, z: i32) -> Self {
        Self { x, y, z }
    }

    fn distance(&self, other: &Point) -> i32 {
        (self.x - other.x).abs() + (self.y - other.y).abs() + (self.z - other.z).abs()
    }
}

#[derive(Debug, PartialEq)]
struct Nanobot {
    position: Point,
    signal_radius: i32,
}

impl Nanobot {
    fn new(position: Point, signal_radius: i32) -> Self {
        Self {
            position,
            signal_radius,
        }
    }

    fn is_in_range(&self, other: &Nanobot) -> bool {
        self.position.distance(&other.position) <= self.signal_radius
    }
}

pub fn run(config: &Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(&config.filename)?;
    let bots = parse_nanobots(&contents);

    match config.part {
        Part::Part1 => {
            let result = part1(&bots);
            println!("{}", result);
        }
        Part::Part2 => {
            // TODO: Part 2
        }
    }

    Ok(())
}

fn parse_nanobots(contents: &str) -> Vec<Nanobot> {
    let re = Regex::new(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)").unwrap();

    contents
        .lines()
        .map(|l| l.trim())
        .filter_map(|l| {
            let captures = re.captures(l);
            match captures {
                Some(c) => {
                    let x = c[1].parse::<i32>().unwrap();
                    let y = c[2].parse::<i32>().unwrap();
                    let z = c[3].parse::<i32>().unwrap();
                    let signal_radius = c[4].parse::<i32>().unwrap();
                    let bot = Nanobot::new(Point::new(x, y, z), signal_radius);

                    Some(bot)
                },
                None => None,
            }
        })
        .collect()
}

fn part1(nanobots: &Vec<Nanobot>) -> usize {
    let mut strongest: Option<&Nanobot> = None;
    for b in nanobots {
        if strongest.is_none() || b.signal_radius > strongest.unwrap().signal_radius {
            strongest = Some(b);
        }
    }

    if let None = strongest {
        return 0;
    }

    let strongest = strongest.unwrap();

    nanobots.iter().filter(|b| strongest.is_in_range(b)).count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn distance() {
        let p1 = Point::new(0, 0, 0);
        let p2 = Point::new(1, 0, 0);
        let p3 = Point::new(4, 0, 0);
        let p4 = Point::new(0, 2, 0);
        let p5 = Point::new(0, 5, 0);
        let p6 = Point::new(0, 0, 3);
        let p7 = Point::new(1, 1, 1);
        let p8 = Point::new(1, 1, 2);
        let p9 = Point::new(1, 3, 1);

        assert_eq!(0, p1.distance(&p1));
        assert_eq!(1, p1.distance(&p2));
        assert_eq!(4, p1.distance(&p3));
        assert_eq!(2, p1.distance(&p4));
        assert_eq!(5, p1.distance(&p5));
        assert_eq!(3, p1.distance(&p6));
        assert_eq!(3, p1.distance(&p7));
        assert_eq!(4, p1.distance(&p8));
        assert_eq!(5, p1.distance(&p9));
    }

    #[test]
    fn parse() {
        let contents = "\
pos=<13159152,29544137,118948329>, r=98351255
pos=<55989149,34723518,60253057>, r=77306587
pos=<7464919,27618769,50195292>, r=76432568
pos=<-45662029,18032820,57472487>, r=80889542";

        let nanobots = parse_nanobots(&contents);

        let expected = vec![
            Nanobot::new(Point::new(13159152, 29544137, 118948329), 98351255),
            Nanobot::new(Point::new(55989149, 34723518, 60253057), 77306587),
            Nanobot::new(Point::new(7464919, 27618769, 50195292), 76432568),
            Nanobot::new(Point::new(-45662029, 18032820, 57472487), 80889542),
        ];
        assert_eq!(expected, nanobots);
    }

    #[test]
    fn part1_test() {
        let bots = vec![
            Nanobot::new(Point::new(0, 0, 0), 4),
            Nanobot::new(Point::new(1, 0, 0), 1),
            Nanobot::new(Point::new(4, 0, 0), 3),
            Nanobot::new(Point::new(0, 2, 0), 1),
            Nanobot::new(Point::new(0, 5, 0), 3),
            Nanobot::new(Point::new(0, 0, 3), 1),
            Nanobot::new(Point::new(1, 1, 1), 1),
            Nanobot::new(Point::new(1, 1, 2), 1),
            Nanobot::new(Point::new(1, 3, 1), 1),
        ];

        assert_eq!(7, part1(&bots))
    }
}
