# Selenium Web Scraper

This project is a Python-based web scraping and automation tool using Selenium WebDriver. It focuses on scraping data from a cakes website and includes various utilities for automation tasks.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Features
- Web scraping functionality for cakes website
- Automated mail unsubscribe operations
- Selector management using CSS and XPath
- Basic Selenium automation scripts
- JSON data export capabilities (output file: `cakes.json`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/fredrick-mwaura/selenium.git
   cd selenium
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the web scraper, execute the following command:

```bash
python scraper.py
```

Make sure to adjust the script parameters as needed for your specific scraping tasks.

## Project Structure
```
selenium/
│
├── basic/
│   └── ...
├── scripts/
│   └── scraper.py
├── selectors/
│   └── ...
└── cakes.json
```

- **basic/**: Contains basic utility functions.
- **scripts/**: Contains the main scraping scripts.
- **selectors/**: Contains CSS/XPath selectors for targeting web elements.
- **cakes.json**: The output file containing scraped data.

## License

This project does not have a specified license. Please feel free to use the code for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or suggestions.

## Contact

For any inquiries, please reach out to [your-email@example.com](mailto:your-email@example.com).
