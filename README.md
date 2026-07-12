# Review
<p align="center">
<img src="public/logo.png" width="25%">
</p>

*Review* is a lightweight command-line tool for inspecting and navigating source code. It provides syntax-highlighted file viewing and fragment extraction based on indentation and structure.

---

## Usage

### Show a file
```bash
rv show <file>
```
Displays the file with syntax highlighting. Supports fuzzy matching on filenames.

### Show a fragment
```bash
rv show <file> <text>
```
Finds and displays the code fragment containing `<text>`. The fragment is determined by analyzing indentation to capture the full logical block (function, class, loop, etc.).
