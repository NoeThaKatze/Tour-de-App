import type { Product, ProductPayload } from './types';

const envApiUrl = import.meta.env.VITE_API_URL;
const API_URL = (envApiUrl && envApiUrl.trim()) ? envApiUrl : (import.meta.env.DEV ? "http://localhost:8080/api" : "/api");

export async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${API_URL}/product`);
  return res.json();
}

export async function createProduct(product: ProductPayload): Promise<Product> {
  const res = await fetch(`${API_URL}/product`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  return res.json();
}

export async function updateProduct(id: number, product: ProductPayload): Promise<Product> {
  const res = await fetch(`${API_URL}/product/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  if (res.status === 404) {
    const err = await res.json();
    throw new Error(err.message);
  }
  return res.json();
}

export async function deleteProduct(id: number): Promise<void> {
  const res = await fetch(`${API_URL}/product/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
