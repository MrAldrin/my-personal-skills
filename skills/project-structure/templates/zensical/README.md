# Zensical layout template

The owner's default look for a Zensical docs site. Source: `agent-workflows`.

| File | Effect |
| --- | --- |
| `stylesheets/headings.css` | Solid-colour, bold, larger headings in light and dark mode. |
| `stylesheets/navigation.css` | Left menu: section titles large and bold, groups bold, pages normal. Uses `--aw-heading-color` from `headings.css`. |
| `stylesheets/layout.css` | Wider page (max 100rem). Styles for the hide buttons. |
| `javascripts/layout-toggle.js` | Two top-bar buttons that hide the left menu and the right page overview. The browser remembers the choice. |

## Apply

1. Copy `stylesheets/` and `javascripts/` into `docs/assets/`.
2. Add to `[project]` in `zensical.toml` (keep existing entries):

   ```toml
   extra_css = ["assets/stylesheets/headings.css", "assets/stylesheets/navigation.css", "assets/stylesheets/layout.css"]
   extra_javascript = ["assets/javascripts/layout-toggle.js"]
   ```

3. Restart `zensical serve`. Check at desktop width (1220px or more): bold menu sections, wide page, two buttons left of search.
