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
  tenant_id?: string | null;
  market?: string | null;
  country?: string | null;
  domain?: string | null;
  module?: string | null;
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
  source_format?: string | null;
  canonical_format?: string | null;
  raw_path?: string | null;
  converted_path?: string | null;
  conversion_status?: string | null;
  conversion_error?: string | null;
  conversion_method?: string | null;
  updated_at?: string | null;
  source_path: string;
};

export type DocumentUploadResponse = {
  document: DocumentDetail;
  index_persisted: boolean;
  ingested_documents?: number | null;
};

export type QueryFilters = {
  doc_id?: string;
  doc_type?: string | string[];
  tenant_id?: string;
  market?: string;
  country?: string;
  domain?: string;
  module?: string;
  business_flow?: string;
  room_id?: string;
  shipment_id?: string;
  customer?: string;
  carrier?: string;
  warehouse?: string;
  route?: string;
  date?: string;
};

export type SourceReference = {
  doc_id: string;
  doc_type: string;
  title?: string | null;
  snippet: string;
  score?: number | null;
  metadata: Record<string, unknown>;
};

export type UiDataBlock = {
  block_id: string;
  block_type: string;
  label: string;
  category: string;
  metadata: Record<string, unknown>;
};

export type QueryResponse = {
  answer: string;
  sources: SourceReference[];
  ui_blocks: UiDataBlock[];
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
