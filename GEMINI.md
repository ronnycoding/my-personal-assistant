# GEMINI.md

## Directory Overview

This directory contains a collection of personal AI agents and scripts designed to automate tasks on macOS using AppleScript. The project is built around the concept of "commands," which are defined in TOML files in the `.gemini/commands` directory. These commands orchestrate the execution of AppleScript files located in the `.claude/skills` directory.

The project is well-documented and includes a testing framework for ensuring the reliability of the scripts.

## Key Files

*   `README.md`: The main entry point for understanding the project. It provides a high-level overview, setup instructions, and usage examples.
*   `PROJECT_SUMMARY.md`: A detailed summary of the project's status, completed work, and future roadmap.
*   `.gemini/commands/`: This directory contains the command definitions in TOML format. Each file defines a command, its associated prompt, and the script it executes.
*   `.claude/skills/`: This directory contains the individual AppleScript files, organized by application (e.g., `apple-mail`, `calendar`, `reminders`).
*   `tests/`: This directory contains the testing framework for the AppleScript scripts, including test runners, assertions, and test data generators.
*   `docs/`: This directory contains detailed documentation about the project, including the command API, permissions setup, and development conventions.

## Usage

To use this project, you will need to have a macOS environment with the necessary applications (Mail, Calendar, Reminders) and permissions configured. The `README.md` file provides detailed instructions on how to set up the project and run the agents.

Once the project is set up, you can interact with the agents by providing natural language commands. The agent will then select and execute the appropriate command to fulfill your request.

## Development

This project is under active development. To contribute, you can create new commands, improve existing scripts, or enhance the testing framework. The `docs/SKILLS_API.md` file provides a comprehensive guide to creating and registering new commands.

When developing, it is important to follow the existing conventions and best practices, which are documented in the `docs` and `.claude/skills` directories. All new code should be accompanied by tests to ensure its correctness and reliability.