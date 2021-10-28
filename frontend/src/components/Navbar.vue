<!-- src/components/Courses.vue -->

<template>
  <nav class="navbar navbar-expand-lg navbar navbar-dark bg-primary">
  <div class="collapse navbar-collapse" id="navbarText">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <router-link to="/" class="nav-link">Home</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/portfolio" class="nav-link">Portfolio</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/trade" class="nav-link">Trade</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/learn" class="nav-link">Learn</router-link>
      </li>
    </ul>
    <div style="margin-left: auto;">
      Welcome, {TO BE ADDED}
    </div>
  </div>
</nav>
</template>

<script>

export default {
  data() {
    return {
      courses: [],
    };
  },
};
</script>

<style scoped>
#navbarText a.router-link-exact-active{
  color: #000000;
  font-weight: bold;
}
#topbarText a.router-link-exact-active:hover {
  color: rgb(255, 255, 255);
}
</style>
