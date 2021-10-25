<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <Courses />
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue';
import Courses from '@/components/Courses.vue';

export default {
  name: 'Home',
  components: {
    // HelloWorld,
    Courses,
  },
};
</script>
