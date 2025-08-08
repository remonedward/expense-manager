# Expense Manager by REMO_OX

A simple and intuitive expense tracking application built with Python and Flet. This app allows users to manage their income and expenses, categorize transactions, generate reports, and export data to CSV. It supports both Arabic and English languages, making it accessible to a wider audience.

## Features

- **Add Transactions**: Record income and expenses with details like amount, category, main description, sub-description (for expenses), and notes.
- **Multilingual Support**: Switch between Arabic and English interfaces seamlessly.
- **Transaction Management**: View, edit, and delete transactions with a user-friendly interface.
- **Reporting**: Generate reports for a specified date range, summarizing total income, expenses, and net balance.
- **CSV Export**: Export all transactions to a CSV file for further analysis.
- **Responsive UI**: Built with Flet for a clean, cross-platform interface.

## Prerequisites

To run this project, you need the following installed:
- Python 3.11
- Flet library

## Installation

1. Clone or download the project files from this repository.
2. Create a virtual environment in the project directory to isolate dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install the required dependencies within the virtual environment:
   ```bash
   pip install flet[all]
   ```
4. Ensure you have a directory named `assets/` in the project root (create it if it doesn't exist).

## Usage

1. Activate the virtual environment if not already active:
   ```bash
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
2. Run the application by executing the main script:
   ```bash
   python main.py
   ```
3. The app will open in a window with a form to add transactions, view transactions, and generate reports.
4. Use the language selector in the top-right corner to switch between Arabic and English.
5. To export transactions to CSV, click the export icon in the app bar (saved to `/storage/emulated/0/Download/expenses_report.csv` on Android or equivalent download directory).
6. To generate a report, select a date range in the "Reports Section" and click "Generate Report."

## Building the APK

To deploy the application as an Android APK, follow these steps:

1. Ensure the virtual environment is activated (see Usage step 1).
2. In the terminal, navigate to the project directory and run the following command to build the APK, replacing `"Expense Manager"` with your desired app name:
   ```bash
   flet build apk --project "Expense Manager"
   ```
3. After a successful build, locate the generated APK in the project’s `build/` directory.
4. To enable CSV export functionality, add storage permissions to `AndroidManifest.xml` (typically found in `build/android/app/src/main/`):
   ```xml
   <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
   <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
   ```
   Place these lines below existing permissions within the `<manifest>` tag.
5. Modify the `pubspec.yaml` file (found in the project root or generated in the build directory) to customize the app:
   - Update the app name under `name` (e.g., `name: Expense Manager`).
   - Set the icon path under `flutter/icons` (e.g., `adaptive_icon_foreground: assets/icon.png`). Ensure `icon.png` exists in the `assets/` directory.
6. Save the changes to `AndroidManifest.xml` and `pubspec.yaml`.
7. Delete the previously generated APK from the `build/` directory.
8. Re-run the build command to generate a new APK with the updated configurations:
   ```bash
   flet build apk --project "Expense Manager"
   ```

## Project Structure

```
expense-manager/
│
├── main.py              # Main application script
├── expenses_data.pkl    # Data file for storing transactions (generated automatically)
├── assets/              # Directory for assets (create if missing, add icon.png for APK)
├── pubspec.yaml         # Configuration file for Flet/Flutter (generated during APK build)
└── README.md            # This file
```

## Screenshots

*(Optional: Add screenshots here to showcase the UI. You can upload images to the `assets/` folder and reference them like `![App Screenshot](assets/screenshot1.png)`.)*

## Contributing

Contributions are welcome! If you'd like to contribute:
1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Flet](https://flet.dev/), a framework for creating cross-platform UI in Python.
- Inspired by the need for a simple, multilingual expense tracking solution.