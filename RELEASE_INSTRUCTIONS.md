# How to Create Releases with GitHub Actions

## Triggering an Automated Release

The project is configured with automated release building through GitHub Actions. To create a release with built files, you need to create and push a tag in the format `vX.Y.Z`.

## Steps to Create a Release

### Method 1: Using Git Commands (Recommended)

1. Make sure your code is committed and pushed to the main branch:
   ```bash
   git add .
   git commit -m "Prepare for release vX.Y.Z"
   git push origin main
   ```

2. Create a tag in the format `vX.Y.Z`:
   ```bash
   git tag vX.Y.Z
   ```

3. Push the tag to GitHub to trigger the release workflow:
   ```bash
   git push origin vX.Y.Z
   ```

### Method 2: Using GitHub Web Interface

1. Go to your repository on GitHub
2. Navigate to the "Releases" tab
3. Click "Draft a new release"
4. Enter a tag in the format `vX.Y.Z` (e.g., v1.0.0)
5. Add a title and description for your release
6. Click "Publish release"

## What Happens During the Release Process

When a tag starting with 'v' is pushed or a release is published:

1. GitHub Actions workflow (`release-on-tag.yml`) is triggered
2. Builds are created for Windows, Linux, and macOS
3. Python application is packaged using PyInstaller
4. Electron desktop application is built
5. Source code archive is created
6. All built files are uploaded as release assets to the GitHub release

## Release Assets Included

Each release will include:

- Executable files for Windows (.exe), Linux, and macOS
- Electron desktop application packages
- Source code archive
- All necessary dependencies

## Notes

- The workflow only triggers for tags that start with 'v' (e.g., v1.0.0, v2.1.3)
- Regular pushes to main branch do NOT create releases, only builds for testing
- The release assets will appear under the specific release in the "Assets" section
- Make sure to use semantic versioning (vX.Y.Z format) for proper release tracking