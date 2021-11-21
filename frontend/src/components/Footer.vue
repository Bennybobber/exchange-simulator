<!-- src/components/Courses.vue -->

<template>
<footer class="footer">
    <h3> SimEx Risk Warning </h3>
    <p class='warning'> Investing is always a risk, as there is no certain way an assets
      will go. Only invest what you can afford to lose and at YOUR own risk.
      This Simulator uses NO real money, and all funds are simulated </p>
    <div class="footer-copyright text-center py-3">
    <p> © 2021 Copyright: Benjamin Sinyard</p>
  </div>
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
h3{
  font-weight: bold;
}
.warning{
  font-weight: bold;
}
@media only screen and (max-width: 600px) {
.footer{
  height: 19rem;
}
h3{
  padding: 2%;
}
.warning{
  padding: 5%;
}
}
</style>
