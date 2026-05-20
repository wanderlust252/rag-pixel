import type { GameCharacter, SpriteAnimation } from "./types";

const WALK_ANIMATIONS: SpriteAnimation[] = [
  { name: "up", row: 0, frames: 9, frame_duration_ms: 90 },
  { name: "left", row: 1, frames: 9, frame_duration_ms: 90 },
  { name: "down", row: 2, frames: 9, frame_duration_ms: 90 },
  { name: "right", row: 3, frames: 9, frame_duration_ms: 90 },
];

function walkSprite(imageUrl: string) {
  return {
    image_url: imageUrl,
    frame_width: 64,
    frame_height: 64,
    columns: 9,
    rows: 4,
    animations: WALK_ANIMATIONS,
  };
}

export const CHARACTERS: GameCharacter[] = [
  {
    character_id: "mage",
    display_name: "Mage Archivist",
    description: "Balanced library explorer with walk, spell, and fallback sheets.",
    sprite: walkSprite("/assets/sprites/mage-walk.png"),
  },
  {
    character_id: "baldric",
    display_name: "Baldric Runner",
    description: "Alternative character for testing character switching.",
    sprite: walkSprite("/assets/sprites/baldric-walk.png"),
  },
  {
    character_id: "shipper-male",
    display_name: "Shipper Male",
    description: "Logistics courier character for delivery workflows.",
    sprite: walkSprite("/assets/sprites/shipper-male.png"),
  },
  {
    character_id: "shipper-female",
    display_name: "Shipper Female",
    description: "Logistics courier character for delivery workflows.",
    sprite: walkSprite("/assets/sprites/shipper-female.png"),
  },
];

export function getCharacter(characterId: string): GameCharacter | null {
  return CHARACTERS.find((character) => character.character_id === characterId) ?? null;
}
