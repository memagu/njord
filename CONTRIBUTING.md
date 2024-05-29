# Contributing to Njord

Thank you for your interest in contributing to Njord! Contributions are welcome and appreciated. Here are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs and Suggesting Features

- Use the [GitHub issue tracker](https://github.com/memagu/njord/issues) to report bugs and suggest features.
- Provide a clear and descriptive title.
- Include as many details as possible to help us understand the issue or suggestion.

### Contributing Code

1. **Fork the Repository**: Click the "Fork" button at the top of the repository page to create a copy on your GitHub account.
2. **Clone Your Fork**: Clone the forked repository to your local machine.
    ```sh
    git clone https://github.com/your-username/njord.git
    ```
3. **Create a Branch**: Create a new branch for your changes, including the issue number in the branch name.
    ```sh
    git checkout -b <number>-description
    ```
    Example:
    ```sh
    git checkout -b 42-fix-startup-crash
    ```
4. **Make Your Changes**: Implement your changes, following the current code style of the project.
5. **Commit Your Changes**: Write clear and descriptive commit messages. For bug fixes, include the issue number in the commit message.
    ```sh
    git add .
    git commit -m "Fix #<number>: A clear and descriptive commit message"
    ```
    Example:
    ```sh
    git commit -m "Fix #42: Resolve crash on startup"
    ```
6. **Push to Your Fork**: Push your changes to your forked repository.
    ```sh
    git push origin <number>-description
    ```
    Example:
    ```sh
    git push origin 42-fix-startup-crash
    ```
7. **Submit a Pull Request**: Open a pull request from your branch to the main repository's `main` branch. Include a description of your changes.

## Code Style

- Follow the current code style of the project.
- Ensure your code is clean and well-documented.

## Issue and Commit Message Guidelines

- **Issue Titles**: Be concise and descriptive.
- **Branch Names**: Include the issue number and a brief description. Example:
    ```
    42-fix-startup-crash
    ```
- **Commit Messages**: Use clear and descriptive messages. For bug fixes, include the issue number. Example:
    ```
    Add feature to export reports in PDF format
    Fix #42: Resolve crash on startup
    Improve performance of data processing module
    ```

## For Maintainers: Merging Pull Requests

1. **Review the Pull Request**: Ensure that the code follows the project's code style, is well-documented, and does not introduce any new bugs.
2. **Check for Linked Issues**: Ensure that the pull request references the correct issue numbers in the description and commit messages.
3. **Run Tests**: Make sure all tests pass successfully.
4. **Merge the Pull Request**:
    - Use the "Squash and Merge" option to combine all commits into a single commit.
    - Write a clear and descriptive commit message, referencing the issue number if applicable.
    - Example commit message:
        ```
        Fix #42: Resolve crash on startup
        ```
5. **Close Related Issues**: After merging, close any issues that were resolved by the pull request.
6. **Thank the Contributor**: Leave a comment thanking the contributor for their work.

Thank you for your contributions!
