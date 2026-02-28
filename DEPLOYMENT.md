# Deployment Guide

ProjectFlow is designed to be a completely static site (HTML, CSS, JS), making it incredibly easy to deploy almost anywhere.

## Official Live Deployment

ProjectFlow is currently deployed via GitHub Pages at:
**[https://seanito14.github.io/projectflow-website/](https://seanito14.github.io/projectflow-website/)**

---

## How to Deploy to GitHub Pages (Your Own Fork)

If you've forked or cloned this repo and want to host your own version on GitHub Pages, follow these steps:

1. **Push your code to GitHub**
   Make sure all your files (`index.html`, `style.css`, `app.js`) are in the root of your repository or in a specific branch (like `main`).

2. **Enable GitHub Pages**
   - Go to your repository on GitHub.
   - Click on the **Settings** tab.
   - On the left sidebar, click on **Pages**.
   - Under "Build and deployment", select **Deploy from a branch**.
   - Under "Branch", select your main branch (e.g., `main`) and the `/root` folder.
   - Click **Save**.

3. **Wait for Deployment**
   GitHub will trigger a GitHub Actions workflow to build and deploy your site. This usually takes 1-2 minutes.

4. **Access Your Site**
   Once deployed, the URL will be available at the top of the Pages settings screen (typically `https://<your-username>.github.io/<your-repo-name>/`).

## How to Deploy Locally

To run the application locally for development or private use:

1. Navigate to the project directory in your terminal:

   ```bash
   cd project-manager
   ```

2. Make the serve script executable (first time only):

   ```bash
   chmod +x serve.sh
   ```

3. Run the script:

   ```bash
   ./serve.sh
   ```

4. Access the site at `http://localhost:8000`.
