export interface User {
  id: string;
  email: string;
  role: 'user' | 'admin';
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  role?: 'user' | 'admin';
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface WatchlistItem {
  id: string;
  user_id: string;
  token_symbol: string;
  target_price: number;
  notes?: string;
  created_at: string;
}

export interface WatchlistItemCreate {
  token_symbol: string;
  target_price: number;
  notes?: string;
}

export interface WatchlistItemUpdate {
  token_symbol?: string;
  target_price?: number;
  notes?: string;
}
