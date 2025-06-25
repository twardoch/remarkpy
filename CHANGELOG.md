# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure based on existing files.
- `PLAN.md`: Detailed plan for MVP 1.0 development.
- `TODO.md`: Task checklist for MVP 1.0 development.
- `CHANGELOG.md`: This changelog file.
- `remarkpy/core.py`: Core Python module with `RemarkpyParser` class for Markdown processing.
- `remarkpy/__init__.py`: Makes `remarkpy` a package and exposes public API.
- Custom exceptions `RemarkpyError` and `JavaScriptError` in `remarkpy/core.py`.

### Changed
- Renamed `remarkpy/test.py` to `remarkpy/core.py`.
- Refactored `remarkpy/core.py` to include `RemarkpyParser` class, error handling, and loading of `remarkpy.js`.
- Updated `__version__` in `remarkpy/core.py` and `remarkpy/__init__.py` to `0.1.0`.

### Removed
- Old script content from `remarkpy/core.py` (formerly `test.py`) replaced by `RemarkpyParser` class.

### Fixed
- Ensured `remarkpy.js` path is correctly determined within `remarkpy/core.py`.
