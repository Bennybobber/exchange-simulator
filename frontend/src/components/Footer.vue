<!-- src/components/Courses.vue -->

<template>
<footer class="footer">
  <div class="footer-copyright text-center py-3">
    <p> © 2021 Copyright: Benjamin Sinyard</p>
  </div>
    <h3> SimEx Risk Warning </h3>
    <p> Investing is always a risk, as there is no certain way an assets
      will go. Only invest what you can afford to lose and at YOUR own risk.
      This Simulator uses NO real money, and all funds are simulated </p>
</footer>
</template>

<script>

export default {
  data() {
    return {
      courses: [],
    };
  },
  methods: {
  },
  created() {
  },
};
</script>

<style scoped>
.footer{
    background-color: #298cd6;
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 10rem;
}
</style>
