# Phase 2 Asset Requirements

## Character Sprites

Required per playable character:

- Walk cycle: 4 directions, 64x64 frame, transparent PNG, consistent row order.
- Idle cycle: 4 directions, can reuse first walk frame for prototype.
- Interact/cast/open cycle: 4 directions or at least front-facing.
- Optional damaged/fall cycle for later combat or error states.

Current usable prototype assets:

- `frontend/public/assets/sprites/mage-walk.png`: usable as 64x64, 9 columns, 4 rows.
- `frontend/public/assets/sprites/baldric-walk.png`: usable as 64x64, 9 columns, 4 rows.
- `frontend/public/assets/sprites/mage-spell.png`: candidate interact/cast sheet, needs final frame mapping.
- `frontend/public/assets/sprites/mage-fall.png`: candidate fall/error state sheet.

## Library Map Tiles

Required:

- Floor tiles: stone/wood/carpet, 32x32 or 16x16.
- Wall tiles: top wall, side wall, corners.
- Door/portal tiles: open/closed/active states, preferably 2-4 animation frames.
- Bookshelf tiles: normal/active/empty states.
- Interaction highlight marker.

The provided Pokemon box-background sheet is not a clean tileset for this library map. It is useful as reference or temporary texture only.

## UI Assets

Required:

- Pixel frame/panel borders.
- Small icons for profile, character switch, interact/open, search/chat.
- Cursor/selection marker.
- Loading indicator.

## Data Models Needed Next

Backend models already added for:

- Game character and sprite metadata.
- Game session with `user_name`, `display_name`, selected character, and position.
- Game world with portals and bookshelves.
- Game interaction response for portal/bookshelf targets.

Next model candidates:

- Persistent player profile table or file store.
- Room/map config instead of generated coordinates.
- Asset manifest endpoint with license/author/source fields.
- Inventory or quest state if business flows become progress-based.
- RAG chat thread scoped by portal or bookshelf.
