<!-- src/components/Courses.vue -->

<template>
<footer class="footer fixed-bottom">
  <div class="footer-copyright text-center py-3">© 2021 Copyright:
    <p> Benjamin Sinyard</p>
  </div>
</footer>
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
  },
  created() {
    this.getCourses();
  },
};
</script>

<style scoped>
.footer{
    background-color: #0d6efd;
}
</style>
