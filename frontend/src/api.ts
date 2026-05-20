import axios from "axios";

import type {
  DocumentUploadResponse,
  GameWorld,
  InteractionResponse,
  QueryFilters,
  QueryResponse,
} from "./types";

const QUERY_TIMEOUT_MS = 60_000 * 10; // 10 minutes

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "/api",
  timeout: 10000,
});

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
  try {
    const response = await api.post<QueryResponse>(
      "/rag/query",
      {
        question: input.question,
        filters: input.filters,
      },
      {
        timeout: QUERY_TIMEOUT_MS,
      },
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === "ECONNABORTED") {
      throw new Error("RAG phản hồi quá chậm. Vui lòng thử lại sau.");
    }
    throw error;
  }
}

export async function interact(input: {
  targetType: "portal" | "bookshelf";
  targetId: string;
  question?: string;
}): Promise<InteractionResponse> {
  const response = await api.post<InteractionResponse>("/game/interactions", {
    target_type: input.targetType,
    target_id: input.targetId,
    question: input.question,
  });
  return response.data;
}
