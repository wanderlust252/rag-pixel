import axios from "axios";

import type {
  DocumentUploadResponse,
  GameCharacter,
  GameSession,
  GameWorld,
  InteractionResponse,
  Position,
  QueryFilters,
  QueryResponse,
} from "./types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "/api",
  timeout: 10000,
});

type CharacterListResponse = {
  characters: GameCharacter[];
};

export async function getCharacters(): Promise<GameCharacter[]> {
  const response = await api.get<CharacterListResponse>("/game/characters");
  return response.data.characters;
}

export async function getWorld(): Promise<GameWorld> {
  const response = await api.get<GameWorld>("/game/world");
  return response.data;
}

export async function uploadDocument(input: {
  file: File;
  docId: string;
  docType: string;
  title: string;
  businessFlow?: string;
  roomId?: string;
  shelfId?: string;
  shipmentId?: string;
  customer?: string;
  carrier?: string;
  warehouse?: string;
  route?: string;
  date?: string;
  sourceType?: string;
  overwrite?: boolean;
  reindex?: boolean;
}): Promise<DocumentUploadResponse> {
  const formData = new FormData();
  formData.append("file", input.file);
  formData.append("doc_id", input.docId);
  formData.append("doc_type", input.docType);
  formData.append("title", input.title);

  const optionalFields: Record<string, string | boolean | undefined> = {
    business_flow: input.businessFlow,
    room_id: input.roomId,
    shelf_id: input.shelfId,
    shipment_id: input.shipmentId,
    customer: input.customer,
    carrier: input.carrier,
    warehouse: input.warehouse,
    route: input.route,
    date: input.date,
    source_type: input.sourceType,
    overwrite: input.overwrite,
    reindex: input.reindex,
  };

  for (const [key, value] of Object.entries(optionalFields)) {
    if (value !== undefined) {
      formData.append(key, String(value));
    }
  }

  const response = await api.post<DocumentUploadResponse>("/documents/upload", formData);
  return response.data;
}

export async function queryRag(input: {
  question: string;
  filters?: QueryFilters;
}): Promise<QueryResponse> {
  const response = await api.post<QueryResponse>("/rag/query", {
    question: input.question,
    filters: input.filters,
  });
  return response.data;
}

export async function createSession(input: {
  userName: string;
  displayName: string;
  characterId: string;
}): Promise<GameSession> {
  const response = await api.post<GameSession>("/game/sessions", {
    user_name: input.userName,
    display_name: input.displayName,
    character_id: input.characterId,
  });
  return response.data;
}

export async function changeCharacter(
  sessionId: string,
  characterId: string,
): Promise<GameSession> {
  const response = await api.patch<GameSession>(`/game/sessions/${sessionId}/character`, {
    character_id: characterId,
  });
  return response.data;
}

export async function syncPosition(sessionId: string, position: Position): Promise<GameSession> {
  const response = await api.patch<GameSession>(`/game/sessions/${sessionId}/position`, {
    position,
  });
  return response.data;
}

export async function interact(input: {
  sessionId: string;
  targetType: "portal" | "bookshelf";
  targetId: string;
  question?: string;
}): Promise<InteractionResponse> {
  const response = await api.post<InteractionResponse>("/game/interactions", {
    session_id: input.sessionId,
    target_type: input.targetType,
    target_id: input.targetId,
    question: input.question,
  });
  return response.data;
}
