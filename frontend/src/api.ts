import type { Product, ProductPayload } from './types';

const envApiUrl = import.meta.env.VITE_API_URL;
const API_URL = (envApiUrl && envApiUrl.trim()) ? envApiUrl : (import.meta.env.DEV ? "http://localhost:8080/api" : "/api");

// Pokud server vrátí chybu, vyhodí Error s textem z pole "detail" (tak ho posílá FastAPI).
async function checkResponse(res: Response): Promise<void> {
  if (res.ok) return;
  let message = `Request failed: ${res.status}`;
  try {
    const err = await res.json();
    if (typeof err.detail === 'string') message = err.detail;
  } catch {
    // odpověď nebyla JSON, zůstane obecná hláška
  }
  throw new Error(message);
}

export async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${API_URL}/product`);
  await checkResponse(res);
  return res.json();
}

export async function createProduct(product: ProductPayload): Promise<Product> {
  const res = await fetch(`${API_URL}/product`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  await checkResponse(res);
  return res.json();
}

export async function updateProduct(id: number, product: ProductPayload): Promise<Product> {
  const res = await fetch(`${API_URL}/product/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  await checkResponse(res);
  return res.json();
}

export async function deleteProduct(id: number): Promise<void> {
  const res = await fetch(`${API_URL}/product/${id}`, {
    method: "DELETE",
  });
  await checkResponse(res);
  return res.json();
}

export async function getHealth(): Promise<{ status: string }> {
  const res = await fetch(`${API_URL}/v1/health`);
  if (!res.ok) {
    throw new Error(`Health check failed: ${res.status}`);
  }
  return res.json();
}

export interface Team {
  name: string;
  members: string[];
}

export async function getTeam(): Promise<Team> {
  const res = await fetch(`${API_URL}/v1/team`);
  if (!res.ok) {
    throw new Error(`Team request failed: ${res.status}`);
  }
  return res.json();
}
