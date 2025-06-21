<template>
  <div class="modal-overlay" @click.self="emitClose">
    <div class="modal-content">
      <h2>{{ date }}의 일정</h2>
      <p>{{ memo }}</p>
      <button @click="emitClose">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  date: String,
  memo: String,
})

const emit = defineEmits(['close'])

const emitClose = () => {
  emit('close')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  width: 300px;
  text-align: center;
}
</style>