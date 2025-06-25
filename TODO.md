# Remarkpy MVP 1.0 TODO List

## Phase 1: Project Setup & Core Documentation

-   [x] **1. Understand Project Structure and Goals**
    -   [x] Analyze `llms.txt`
    -   [x] Define MVP 1.0 scope
-   [x] **2. Create Core Documentation Files**
    -   [x] `PLAN.md`
    -   [x] `TODO.md`
    -   [x] `CHANGELOG.md`

## Phase 2: Python API Development

-   [ ] **3. Refine Python Interface**
    -   [x] Rename `remarkpy/test.py` to `remarkpy/core.py`
    -   [x] Develop Python API (`RemarkpyParser` class in `remarkpy/core.py`)
        -   [x] Define main parsing method (`parse`)
        -   [x] Implement `quickjs` interaction for loading `remarkpy/remarkpy.js`
        -   [x] Add error handling (`RemarkpyError`, `JavaScriptError`)
    -   [x] Add basic usage example (in `remarkpy/core.py` under `if __name__ == '__main__':`)
    -   [x] Create `remarkpy/__init__.py` to expose public API and version.

## Phase 3: JavaScript Refinement

-   [ ] **4. JavaScript Bundling and Interface**
    -   [ ] Review `remarkpyjs/index.js` for clarity and export
    -   [ ] Standardize on Webpack:
        -   [ ] Remove `browserify` script from `remarkpyjs/package.json`
    -   [ ] Verify `remarkpy/remarkpy.js` UMD bundle compatibility with `quickjs`
    -   [ ] Review/Optimize `remarkpyjs/webpack.config.js`

## Phase 4: Testing

-   [ ] **5. Testing**
    -   [ ] Create `tests/` directory
    -   [ ] Set up `pytest`
    -   [ ] Write Python tests for the API:
        -   [ ] Basic Markdown features
        -   [ ] `remarkpy/test.md` parsing
        -   [ ] Error handling
        -   [ ] Edge cases

## Phase 5: Build and Packaging

-   [ ] **6. Build Process and Tooling**
    -   [ ] Create `pyproject.toml`
    -   [ ] Configure `setuptools` (or chosen build backend)
    -   [ ] Define package metadata (name, version, author, etc.)
    -   [ ] Ensure `remarkpy/remarkpy.js` is included in the Python package
    -   [ ] (Optional) Create `Makefile` or `justfile` for dev tasks

## Phase 6: Documentation Enhancement

-   [ ] **7. Documentation**
    -   [ ] Update `README.md`:
        -   [ ] Project description
        -   [ ] Installation instructions
        -   [ ] Python API usage examples
        -   [ ] How to run tests
    -   [ ] Write API docstrings for Python code (initial pass done in `core.py`)
    -   [ ] Add comments to `remarkpyjs/index.js` if needed

## Phase 7: Code Quality & Structure

-   [ ] **8. Code Quality and Structure**
    -   [ ] Refactor Python and JavaScript code for clarity
    -   [ ] Setup Linting/Formatting:
        -   [ ] Python: Black, Flake8 (configure in `pyproject.toml`)
        -   [ ] JavaScript: Prettier, ESLint (configure in `remarkpyjs/`)
    -   [ ] Finalize directory structure.

## Phase 8: Dependencies and Finalization

-   [ ] **9. Dependency Management**
    -   [ ] Review/update `md-mdast` version in `remarkpyjs/package.json`
    -   [ ] Specify Python dependencies (`quickjs`, `pytest`) in `pyproject.toml`
-   [ ] **10. Final Review and Versioning**
    -   [ ] Perform thorough end-to-end testing
    -   [ ] Update `CHANGELOG.md` for v1.0.0
    -   [ ] Set version to `1.0.0` (`pyproject.toml`, `__init__.py`)
    -   [ ] Tag Git release `v1.0.0`

## Ongoing Tasks
-   [ ] Update `PLAN.md` as needed
-   [ ] Mark items in `TODO.md` as complete
-   [ ] Record changes in `CHANGELOG.md`
-   [ ] Commit regularly
