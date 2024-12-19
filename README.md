# Fibank Branches Scraper

This Python script scrapes information about Fibank branches that operate on Saturdays and Sundays from the Fibank website. The scraped data is saved to an Excel file and sent via email using Gmail SMTP.

## Features

- Scrapes branch information including name, address, telephone, and working hours for Saturday and Sunday.
- Saves the scraped data to an Excel file.
- Sends the Excel file via email using Gmail SMTP.

## Requirements

- Python 3.x
- Selenium
- Pandas
- Openpyxl
- Dotenv

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/fibank-branches-scraper.git
    cd fibank-branches-scraper
    ```

2. **Install the required libraries**:
    ```sh
    pip install selenium pandas openpyxl python-dotenv
    ```

3. **Download ChromeDriver**:
    - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and extract it to a known directory.
    - Update the path to ChromeDriver in the script.

4. **Create a `.env` file**:
    - Create a file named `.env` in the project directory and add your credentials:
      ```env
      FROM_EMAIL=your_email@gmail.com
      TO_EMAIL=recipient_email@example.com
      APP_PASSWORD=your_app_password
      ```

5. **Add `.env` to `.gitignore**:
    - Ensure that your `.env` file is added to `.gitignore` so it is not pushed to GitHub.

## Usage

1. **Run the script**:
    ```sh
    python scrap.py
    ```

2. **Check your email**:
    - The Excel file containing the Fibank branches operating on weekends will be sent to the specified email address.
