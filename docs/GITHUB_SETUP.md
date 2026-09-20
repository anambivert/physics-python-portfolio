# Use and share the GitHub portfolio

The repository is [anambivert/physics-python-portfolio](https://github.com/anambivert/physics-python-portfolio). Both labs are project folders in this one repository, so its visibility setting applies to both.

## Work locally

```bash
git clone https://github.com/anambivert/physics-python-portfolio.git
cd physics-python-portfolio
```

Follow [environment setup](ENVIRONMENT.md), run a project, and use [the project guide](ADDING_PROJECTS.md) when adding another lab. To upload your changes:

```bash
git add .
git status
git commit -m "Add the next lab project"
git push
```

Review the staged file list before committing. Git must be installed, and pushing requires authentication with your GitHub account. Your configured Git name and email will appear in commits.

## Upload through GitHub

Open the relevant project folder, choose **Add file → Upload files**, select the files, and commit the change. Keep the project README, data inventory and root project index up to date. Upload unpacked files so GitHub can display notebooks and source code.

## Change visibility

Open [repository settings](https://github.com/anambivert/physics-python-portfolio/settings). Under **Danger Zone**, choose **Change visibility → Change to public**, then follow GitHub's confirmation prompts through **Make this repository public**. A public repository allows anyone to view and fork its files and history.

After changing visibility, open the repository in a private/incognito browser window without signing in to verify public access. The root README links to both lab projects.

References: [GitHub visibility instructions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility), [uploading files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
