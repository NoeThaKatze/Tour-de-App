export interface Product {
  id: number;
  name: string;
  cost: number;
}

export type ProductPayload = Omit<Product, 'id'>;
