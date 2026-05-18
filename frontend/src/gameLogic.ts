import type {
  Bookshelf,
  Direction,
  GameWorld,
  InteractableTarget,
  LibraryPortal,
  Position,
} from "./types";

const STEP = 16;
const PLAYER_SIZE = 64;
const INTERACTION_RADIUS = 78;

export function movePosition(
  position: Position,
  direction: Direction,
  world: GameWorld,
): Position {
  const next = { ...position };
  if (direction === "up") next.y -= STEP;
  if (direction === "down") next.y += STEP;
  if (direction === "left") next.x -= STEP;
  if (direction === "right") next.x += STEP;

  return {
    x: clamp(next.x, 24, world.width - PLAYER_SIZE - 24),
    y: clamp(next.y, 96, world.height - PLAYER_SIZE - 24),
  };
}

export function findNearestTarget(
  position: Position,
  world: GameWorld,
): InteractableTarget | null {
  const targets: InteractableTarget[] = [
    ...world.portals.map(portalToTarget),
    ...world.shelves.map(shelfToTarget),
  ];

  let nearest: { target: InteractableTarget; distance: number } | null = null;
  for (const target of targets) {
    const distance = Math.hypot(target.position.x - position.x, target.position.y - position.y);
    if (distance <= INTERACTION_RADIUS && (!nearest || distance < nearest.distance)) {
      nearest = { target, distance };
    }
  }

  return nearest?.target ?? null;
}

function portalToTarget(portal: LibraryPortal): InteractableTarget {
  return {
    type: "portal",
    id: portal.portal_id,
    label: portal.label,
    position: portal.position,
  };
}

function shelfToTarget(shelf: Bookshelf): InteractableTarget {
  return {
    type: "bookshelf",
    id: shelf.shelf_id,
    label: shelf.label,
    position: shelf.position,
  };
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
