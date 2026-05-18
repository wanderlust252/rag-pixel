export type Direction = "down" | "left" | "right" | "up";

export type Position = {
  x: number;
  y: number;
};

export type SpriteAnimation = {
  name: Direction;
  row: number;
  frames: number;
  frame_duration_ms: number;
};

export type CharacterSprite = {
  image_url: string;
  frame_width: number;
  frame_height: number;
  columns: number;
  rows: number;
  animations: SpriteAnimation[];
};

export type GameCharacter = {
  character_id: string;
  display_name: string;
  description: string;
  sprite: CharacterSprite;
};

export type DocumentSummary = {
  doc_id: string;
  doc_type: string;
  title: string;
  business_flow?: string | null;
  room_id?: string | null;
  shelf_id?: string | null;
  shipment_id?: string | null;
  customer?: string | null;
  carrier?: string | null;
  warehouse?: string | null;
  route?: string | null;
};

export type DocumentDetail = DocumentSummary & {
  date?: string | null;
  source_type?: string | null;
  source_path: string;
};

export type GameSession = {
  session_id: string;
  user_name: string;
  display_name: string;
  character: GameCharacter;
  position: Position;
};

export type LibraryPortal = {
  portal_id: string;
  label: string;
  business_flow: string;
  position: Position;
  document_count: number;
};

export type Bookshelf = {
  shelf_id: string;
  label: string;
  doc_id: string;
  doc_type: string;
  portal_id: string;
  position: Position;
  document: DocumentSummary;
};

export type GameWorld = {
  world_id: string;
  name: string;
  width: number;
  height: number;
  tile_size: number;
  spawn: Position;
  portals: LibraryPortal[];
  shelves: Bookshelf[];
};

export type InteractionResponse = {
  interaction_id: string;
  target_type: "portal" | "bookshelf";
  title: string;
  message: string;
  document?: DocumentDetail | null;
  related_documents: DocumentSummary[];
};

export type InteractableTarget =
  | {
      type: "portal";
      id: string;
      label: string;
      position: Position;
    }
  | {
      type: "bookshelf";
      id: string;
      label: string;
      position: Position;
    };
