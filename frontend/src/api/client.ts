import axios, { AxiosError } from "axios";
import type {
  ChatResponse,
  Conversation,
  ConversationDetail,
  User,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const client = axios.create({ baseURL: API_BASE_URL });

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken && !(error.config as any)?._retry) {
        try {
          const { data } = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
          const originalConfig: any = error.config;
          originalConfig._retry = true;
          originalConfig.headers.Authorization = `Bearer ${data.access_token}`;
          return client(originalConfig);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
      } else {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  register: (full_name: string, email: string, password: string) =>
    client.post<User>("/auth/register", { full_name, email, password }),
  login: (email: string, password: string) =>
    client.post<{ access_token: string; refresh_token: string }>("/auth/login", {
      email,
      password,
    }),
  me: () => client.get<User>("/auth/me"),
};

export const chatApi = {
  send: (message: string, conversation_id?: string, clarification_answer?: string) =>
    client.post<ChatResponse>("/chat", {
      message,
      conversation_id,
      clarification_answer,
    }),
};

export const historyApi = {
  list: () => client.get<Conversation[]>("/history/conversations"),
  get: (id: string) => client.get<ConversationDetail>(`/history/conversations/${id}`),
  remove: (id: string) => client.delete(`/history/conversations/${id}`),
};

export const agentsApi = {
  graphInfo: () => client.get("/agents/graph-info"),
  services: () => client.get<{ services: string[] }>("/agents/services"),
};

export default client;
