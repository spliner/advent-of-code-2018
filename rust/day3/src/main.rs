use std::{env, process};

use day3::Config;

fn main() {
    let config = Config::new(env::args()).unwrap_or_else(|err| {
        eprintln!("Error parsing arguments: {}", err);

        process::exit(1);
    });

    if let Err(e) = day3::run(config) {
        eprintln!("Application error: {}", e);

        process::exit(1);
    }
}
