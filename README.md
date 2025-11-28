# Satellite_Images

## Introduction
This project allows users to **interactively click on a map** to capture geographic coordinates (latitude & longitude).  
Once a point is selected, the system automatically triggers a workflow that generates a **satellite image** based on those coordinates.

This tool is ideal for:
- Collecting satellite imagery for research or analysis  
- Quickly extracting imagery for specific geographic points  
- Learning about map interaction, APIs, and GitHub Actions workflows

---

## How It Works
1. User clicks on the map rendered in the browser.  
2. The coordinates of the clicked location are recorded.  
3. A GitHub Actions workflow generates a satellite image for those coordinates.  
4. The user downloads the resulting satellite image from the **GitHub Actions → satellite_image** workflow.

---

## Getting Started

###  Clone the Repository
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

## Running the Map Interface (Using Live Server)

### Requirements
- VS Code
- Live Server extension (by Ritwick Dey)

### Steps
1. Open the repository in VS Code.
2. Locate the main HTML file (for example, `index.html`).
3. Right-click the file and select **"Open with Live Server"**.
4. The map will open in your browser.
5. Click anywhere on the map to generate coordinates.

A notification or console output will confirm that coordinates were captured.



## Downloading the Generated Satellite Image

1. Go to your GitHub repository.
2. Click the **Actions** tab.
3. Select the workflow named `satellite_image`.
4. Open the most recent workflow run (triggered automatically after clicking on the map).
5. Scroll to the **Artifacts** section.
6. Download the satellite image artifact.
7. Extract the downloaded file to view your satellite image.
