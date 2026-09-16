# Reusable Folloze Components

`Components/` contains versioned interaction modules that board builders compile into self-contained Folloze HTML sections.

These packages are not Codex skills and are not Folloze Content items. A component owns a reusable interface and its runtime contract. A board-specific configuration supplies the audience labels and content changes. Content Center assets stay in the board and open through the native Folloze viewer.

Use `registry.json` to discover the current components and their entry points. Pin a component version in each board's working notes or content manifest, then inline the rendered CSS, markup, and JavaScript into the final board fragment. Do not load component code from GitHub at page-view time.
