# Manual trigger instead of scheduled automation

The app is named "daily report generator," which might suggest it runs automatically. We decided the first version only runs when the user manually opens the app, picks the Excel file themselves via a file-picker dialog, and clicks a button — no scheduled runs, no folder-watching. This keeps the first version simple to build and test, and automatic scheduling can be layered on top later without changing the core Excel → PowerPoint → PDF conversion logic underneath it.
