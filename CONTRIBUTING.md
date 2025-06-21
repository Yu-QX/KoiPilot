# Contributing to *KoiPilot* 🛠️

Thank you for your interest in contributing to *KoiPilot* ! We welcome all kinds of contributions — whether it's fixing bugs, adding features, improving documentation, or sharing ideas.

---

## 📝 Code of Conduct

We’re all about a positive, respectful vibe. By joining in, you agree to keep things friendly, inclusive, and professional. No dodgy behavior — treat everyone like a top mate!

---

## 🤔 How to Contribute

### 0. Title Formate 🚂

Please note that all "titles" **must** follow the format: `TYPE(Date): content`. The so called "titles" include but not limited to:
- Committing message: when executing `git commit -m "TYPE(Date): content"` locally
- Pull Requests (PRs) title: when creating a pull request
- Issues title: when creating an issue or discussion

`TYPE` (written in uppercase) can be one of the following:
- `FIX`: for bug fixes
- `FEAT`: for new features
- `DOCS`: for documentation changes or code style changes or translation
- `REFACT`: for refactoring code or changing algorithm
- `OTHERS`: if your commit doesn't fit into any of the above categories

`Date` refers to the local date of the commit in your region, formatted as `YYYYMMDD`. Due to time zone differences, a variation of up to 24 hours is expected and won't affect the overall ordering of commits on the timeline.

`content` should be concise and clearly describe the purpose of the commit.

> e.g. `DOCS(20250610): Write a better README.md`

This helps everyone track what changes have been made across the app.

### 1. Communication 🙋‍♂️

Before diving into development, please search for existing issues — someone may already be working on a similar task. If so, feel free to join the conversation!

If nothing exists yet, open a new issue or start a discussion thread. When creating an issue, we encourage you to include your availability — whether you're ready to work on it with assistance or need help from others.

### 2. Reporting Issues 🪳

If you find a bug or want to request a feature, please open a new issue on GitHub.  

Include the following details:

- A clear description of the problem or request  
- Steps to reproduce (if applicable)  
- Your system details (OS, Python version, etc.)

### 3. Feature Requests 💡

We love fresh ideas! When suggesting a new feature:

- Check existing issues to avoid duplicates  
- Explain the benefit and use case clearly  
- Be open to discussion and feedback

### 4. Refactoring 🪢

Refactoring isn't just about making code look prettier — it's about improving performance, readability, and long-term maintainability. We welcome suggestions such as:

- Replacing inefficient algorithms
- Optimizing overall performance
- Modularizing and restructuring code

Always start a discussion before beginning any refactoring work!

### 5. Improve Documentation & Translations 📚

Documentation improvements are always welcome! You can help by:

- Fixing typos or grammar errors  
- Adding examples to the README or docstrings  
- Writing or updating tutorials or usage guides  

You can also contribute translations for parts of the app such as:

- AI prompt templates  
- User interface elements  

---

## 📝 Code Style

- Use **Python 3.10+** syntax  
- Keep code clean and readable  
- Add comments where needed to explain complex parts
- `CamelCase` for variables and functions to export and `snake_case` for internal use

---

## 🚀 Submitting Pull Requests (PRs)

Before submitting a PR, please make sure you:

* [ ] **At the beginning:**
  * [ ] Start an issue to discuss your proposed changes
  * [ ] Insure good title **throughout** the PR (see `### 0. Title Formate`)
* [ ] **During Coding:**
  * [ ] Keep your changes focused on a single issue or feature
  * [ ] Follow the existing code style and conventions  
  * [ ] Test your changes thoroughly
* [ ] **Creating PR:**
  * [ ] Target your PR at the `dev` branch
  * [ ] Include a clear description of what your PR does  

> Tick all the boxes above to confirm you've done them.

Unless otherwise specified, always create your pull request against the `dev` branch — not `main`.

Thank you for helping make KoiPilot better! 🎉
