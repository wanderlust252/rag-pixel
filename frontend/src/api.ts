import axios from "axios";

import type {
  GameCharacter,
  GameSession,
  GameWorld,
  InteractionResponse,
  Position,
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
