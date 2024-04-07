# Release Information

This document outlines the step-by-step process for releasing a new version of the application.
It provides detailed instructions on leveraging the provided release workflow to generate executables for various supported operating systems and publish them as release assets.

## Prerequisites
Before initiating the release process, ensure the following prerequisites are met:
- Access to the repository containing the application code.
- Familiarity with Git and GitHub workflows.
- Understanding of how to generate release notes.
- The 'pipeline.yml' for build and test should successfully pass for the pull request associated with the release.

## Release Workflow Overview
The release process is automated through the provided **release.yml** file, which orchestrates the following actions:
- **Trigger**: The release workflow is automatically triggered whenever a new release is published.
- **Build**: Upon triggering, the workflow initiates the build process using **Pyinstaller** to generate executables tailored to each supported operating system.
- **Upload**: Once the builds are successfully generated, the workflow uploads the executables as release assets.
- **Publish**: Finally, the release assets are published, making the new version of the application available to users.