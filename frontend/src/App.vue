<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getProducts, createProduct, updateProduct, deleteProduct } from './api';
import type { Product, ProductPayload } from './types';
import ProductForm from './components/ProductForm.vue';
import ProductTable from './components/ProductTable.vue';

const products = ref<Product[]>([]);
const editingProduct = ref<Product | null>(null);

async function loadProducts() {
  try {
    products.value = await getProducts();
  } catch (e) {
    console.error('Failed to load products:', e);
  }
}

onMounted(() => {
  loadProducts();
});

async function handleCreate(product: ProductPayload) {
  await createProduct(product);
  await loadProducts();
}

async function handleUpdate(product: ProductPayload) {
  if (!editingProduct.value) return;
  await updateProduct(editingProduct.value.id, product);
  editingProduct.value = null;
  await loadProducts();
}

async function handleDelete(id: number) {
  await deleteProduct(id);
  await loadProducts();
}

function handleCancel() {
  editingProduct.value = null;
}
</script>

<template>
  <div>
    <h1>Think different Academy</h1>

    <ProductForm
      :initial="editingProduct"
      @submit="editingProduct ? handleUpdate($event) : handleCreate($event)"
      @cancel="handleCancel"
    />

    <ProductTable
      :products="products"
      @edit="p => editingProduct = p"
      @delete="handleDelete"
    />
  </div>
</template>
