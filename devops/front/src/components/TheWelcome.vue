<script setup lang="ts">
import { useApiStore } from '@/stores/api'
import { ref } from 'vue'
import { onMounted } from 'vue'

const apiStore = useApiStore()
var quote = ref('')

function getQuote() {
  apiStore.getRandomFortune().then((q) => {
    console.log(q.prediction)
    quote.value = q.prediction
  })
}

onMounted(() => {
  getQuote()
})
</script>

<template>
  <h1>{{ quote }}</h1>
  <button @click="getQuote()">Other</button>
</template>

<style lang="scss" scoped>
button {
  border: 2px solid #2c2b2b;
  border-radius: 20px;
  background-color: transparent;
  color: #2c2b2b;
  font-size: 1rem;
  padding: 0.2rem 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;

  &:hover {
    background-color: #373737;
    color: #fff;
  }
}
</style>
