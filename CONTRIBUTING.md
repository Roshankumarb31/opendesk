# Contributing to OpenDesk

Thanks for your interest in contributing! We welcome issues, ideas, and pull requests.

## Ways to Contribute
- Report bugs and propose features via Issues
- Improve UI/UX or add supported app types
- Enhance build tooling, packaging, or CI
- Improve docs: README, build guide, usage tips

## Development Setup
- OS: Windows 10/11
- Python: 3.7+
- Install dependencies:
  - pip install flet psutil

Run the app:
- python main.py

## Workflow
1. Fork the repo
2. Create a feature branch:
   - git checkout -b feature/your-feature
3. Make your changes with clear commit messages
4. Ensure it runs locally and doesn’t break existing features
5. Open a Pull Request:
   - Describe what changed and why
   - Include screenshots/GIFs for UI changes

## Code Style
- Follow PEP8 (readable, consistent)
- Keep functions small and focused
- Avoid hard-coding machine-specific paths
- Update docs and type hints where helpful

## Testing Your Changes
- Launch selected, close all, add/delete items
- Website open (normal/incognito) for multiple browsers
- Startup toggle behavior
- Config saved to ~/Documents/launcher_config.json

## Attribution
OpenDesk is an open-collaboration project. Please retain credit to original authors and contributors in documentation and source headers where applicable.

Thanks for helping build OpenDesk!