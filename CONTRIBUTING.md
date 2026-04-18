# Contributing to PainMatrix

First off, thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](../../issues)
2. If not, create a new issue using the **Bug Report** template
3. Include: OS version, Python version, steps to reproduce, expected vs actual behavior

### Suggesting Features

1. Check existing [Issues](../../issues) and [Discussions](../../discussions)
2. Create a new issue using the **Feature Request** template
3. Describe the use case and expected behavior clearly

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `python -m pytest tests/ -v`
6. Commit with clear message: `git commit -m "Add: feature description"`
7. Push: `git push origin feature/my-feature`
8. Create a Pull Request using the PR template

### Code Style

- Python: Follow PEP 8, use type hints
- Max line length: 120 characters
- Use meaningful variable names
- Add docstrings to all public functions

### Development Setup

```bash
git clone https://github.com/openclaw/PainMatrix.git
cd PainMatrix
pip install -r requirements.txt
python -m pytest tests/ -v
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
