<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getProducts, createProduct, updateProduct, deleteProduct, getHealth, getTeam } from './api';
import type { Team } from './api';
import type { Product, ProductPayload } from './types';
import ProductForm from './components/ProductForm.vue';
import ProductTable from './components/ProductTable.vue';

const products = ref<Product[]>([]);
const editingProduct = ref<Product | null>(null);
const healthStatus = ref('...');
const team = ref<Team | null>(null);

async function loadTeam() {
  try {
    team.value = await getTeam();
  } catch (e) {
    console.error('Failed to load team:', e);
  }
}

async function loadHealth() {
  try {
    const data = await getHealth();
    healthStatus.value = data.status.toUpperCase();
  } catch (e) {
    console.error('Health check failed:', e);
    healthStatus.value = 'ERROR';
  }
}

async function loadProducts() {
  try {
    products.value = await getProducts();
  } catch (e) {
    console.error('Failed to load products:', e);
  }
}

onMounted(() => {
  loadHealth();
  loadTeam();
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
    <p>Status: {{ healthStatus }}</p>

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

    <footer v-if="team" class="authors">
      Created by {{ team.name }}: {{ team.members.join(', ') }}
    </footer>
  </div>
</template>

<style scoped>
.authors {
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px solid #222;
  color: #888;
  font-size: 14px;
}
</style>
