# TSA Website

The public visibility site for TSU's Transportation Student Association — the umbrella
student organization for the Department of Transportation. Not a Vantage AI client project;
this is Milo's own school organization as its president.

## Current state

Single self-contained `index.html` (no build step, no framework) — matches the `rombys`/
`ai-consulting-site` pattern of a static one-file site. Content is honest about where TSA
actually stands right now: Milo is the only filled officer role (President), every other
Executive Board seat is marked "Open," and the sub-orgs directory is empty placeholder slots
inviting affiliation — **don't replace these with fabricated officers or sub-orgs**, update
them only as roles/orgs are actually filled/confirmed.

## Design

- TSU brand colors (verified against TSU's official Brand Standards PDF, Pantone-to-hex
  converted since TSU doesn't publish hex directly): maroon `#7C183E`, gray `#9DA6AB`.
- Display face: Oswald (condensed grotesk, transit/wayfinding-signage character), embedded
  as a base64 `@font-face` data URI directly in `index.html` — no external font request, no
  CDN dependency. Body text uses the system font stack.
- The "route-line" and "network tier" visual motifs in the hero and Organization section are
  a deliberate echo of the actual governance structure (see
  `~/School/TSU/TSA/tsa_governance_structure.md` for the source document this content is
  built from) — keep them in sync if that structure changes.
- Both light and dark mode are implemented via CSS custom properties re-defined under
  `prefers-color-scheme` and `[data-theme]` overrides.

## Content source of truth

`~/School/TSU/TSA/tsa_governance_structure.md` is the governance proposal this site's
Organization/Get Involved sections are built from, including the open questions (dues,
sub-org affiliation process, 8th exec role) noted there. Update the site after those
decisions are actually made, not before.

## Deploy

Static site, no backend — deploys to Netlify or Vercel by dragging the folder in or
connecting the repo. No environment variables or build step required.
