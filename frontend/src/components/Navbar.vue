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
import axios from 'axios';

export default {
  data() {
    return {
      courses: [],
    };
  },
  methods: {
    getCourses() {
      const path = 'http://localhost:5000/courses';
      axios.get(path)
        .then((res) => {
          this.courses = res.data.courses;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    burger: () => {
      const x = document.getElementById('myTopNav');
      if (x.className === 'topNav') {
        x.className += ' responsive';
      } else {
        x.className = 'topNav';
      }
    },
  },
  created() {
    this.getCourses();
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
