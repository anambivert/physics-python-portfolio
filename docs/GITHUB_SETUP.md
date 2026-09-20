# Create the GitHub repository

Suggested repository name: **physics-python-portfolio**

Suggested description:

> Python portfolio covering physics labs, spectroscopy, optical beam analysis, image processing, and numerical computing.

Suggested topics: `python`, `physics`, `scientific-computing`, `data-analysis`, `numpy`, `scipy`, `matplotlib`.

## Upload through the website

1. Extract this ZIP on your computer.
2. Open [GitHub's new-repository form](https://github.com/new?name=physics-python-portfolio&description=Python+portfolio+for+physics+labs+and+scientific+computing&visibility=private).
3. Select your account as owner. The link starts with **Private**; choose **Public** when ready to make the portfolio visible to recruiters.
4. Leave GitHub's README, gitignore, and license initialization options unselected; the package already contains a README and Git ignore rules.
5. Create the repository, then choose the link to upload existing files.
6. Upload the **contents** of the extracted `physics-python-portfolio` folder so `README.md` sits at the repository root. Include the supplied dotfiles. Uploading the ZIP itself will not display the portfolio.
7. Review the file list and commit with a message such as `Set up physics Python portfolio`.

For subsequent updates, use **Add file → Upload files** or work locally with Git. See [GitHub's file-upload instructions](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

## Alternative: Git from your computer

After creating an **empty** GitHub repository, open a terminal inside the extracted folder:

```bash
git init -b main
git add .
git status
git commit -m "Set up physics Python portfolio"
git remote add origin https://github.com/YOUR-USERNAME/physics-python-portfolio.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Git must be installed and authenticated; the commit uses your configured Git name and email. Do not run these initial-setup commands inside a different existing repository.

Once uploaded, open the root README and each project link to check the presentation.

References: [Creating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository), [Importing local code](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).
