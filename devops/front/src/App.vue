<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="content">
    <header>
      <img alt="Vue logo" class="logo" src="@/assets/dice.png" width="125" height="125" />
      <nav>
        <RouterLink to="/">Fortune</RouterLink>
        <RouterLink to="/astrology">Astrology</RouterLink>
      </nav>
    </header>

    <RouterView />
  </div>
</template>

<style scoped lang="scss">
.content {
  width: 80%;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex-direction: row;
  gap: 3rem;
}

header {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;
  nav {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    flex-direction: column;
    a {
      color: var(--text);
      &.router-link-exact-active {
        color: hsla(160, 100%, 37%, 1);
      }
      &.router-link-exact-active:hover {
        background-color: transparent;
      }
    }
  }
}
</style>
