<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Product, ProductPayload } from '../types';

const props = defineProps<{
  initial: Product | null;
}>();

const emit = defineEmits<{
  (e: 'submit', product: ProductPayload): void;
  (e: 'cancel'): void;
}>();

const name = ref('');
const cost = ref<number | ''>('');

watch(() => props.initial, (newVal) => {
  if (newVal) {
    name.value = newVal.name;
    cost.value = newVal.cost;
  } else {
    name.value = '';
    cost.value = '';
  }
}, { immediate: true });

function handleSubmit() {
  if (!name.value || cost.value === '') return;

  emit('submit', {
    name: name.value,
    cost: Number(cost.value)
  });

  if (!props.initial) {
    name.value = '';
    cost.value = '';
  }
}

function handleCancel() {
  emit('cancel');
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <label>
      Name
      <input v-model="name" name="name" required />
    </label>
    <label>
      Price
      <input v-model="cost" name="cost" type="number" required />
    </label>
    <button type="submit">{{ initial ? 'Save' : 'Add' }}</button>
    <button v-if="initial" type="button" @click="handleCancel">Zrušit</button>
  </form>
</template>
