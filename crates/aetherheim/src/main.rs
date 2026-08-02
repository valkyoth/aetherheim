//! Aetherheim command-line entry point.

#![forbid(unsafe_code)]

use std::env;
use std::process::ExitCode;

fn print_help() {
    println!("Aetherheim {}", aetherheim::version());
    println!("Security-first content operating system foundation");
    println!();
    println!("USAGE:");
    println!("    aetherheim [--version|doctor|help]");
}

fn doctor() {
    println!("version={}", aetherheim::version());
    println!("dependency-policy=minimal-reviewed-exact-pins");
    println!("publishing=disabled");
    println!("status=foundation-only");
}

fn main() -> ExitCode {
    match env::args().nth(1).as_deref() {
        None | Some("help" | "--help" | "-h") => print_help(),
        Some("--version" | "-V") => println!("aetherheim {}", aetherheim::version()),
        Some("doctor") => doctor(),
        Some(command) => {
            eprintln!("unknown command: {command}");
            return ExitCode::from(2);
        }
    }
    ExitCode::SUCCESS
}
