import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useApiStore = defineStore('api', () => {
  const baseUrl = ref('http://localhost:3000/api')
  const language = ref('en')

  function changeLanguage(lang: string) {
    language.value = lang
  }

  async function getRandomFortune() {
    console.log('fetching random fortune')
    const response = await fetch(`${baseUrl.value}/fortune/random`)
    return response.json()
  }

  return { changeLanguage, getRandomFortune }
})
