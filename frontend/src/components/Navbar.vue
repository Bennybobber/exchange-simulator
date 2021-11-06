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
        <router-link to="/trade?coin=BTC" class="nav-link">Trade</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/learn" class="nav-link">Learn</router-link>
      </li>
    </ul>
    <div id="userButton" style="margin-left: auto;">
      <button class="btn p-3 mb-2 bg-black text-light"
        v-if="this.$store.state.auth.status.loggedIn"
          @click="handleLogout()">
            Logout
      </button>
      <button class="btn p-3 mb-2 bg-black text-light" v-else @click="handleLogin()">Login</button>
    </div>
  </div>
</nav>
</template>

<script>

export default {
  data() {
    return {
      loggedIn: this.checkLoginStatus,
    };
  },
  created() {
  },
  computed: {

  },
  methods: {
    handleLogout() {
      this.$store.dispatch('auth/logout', this.user).then(
        () => {
          this.$router.push('/');
        },
        (error) => {
          this.loading = false;
          this.message = (error.response && error.response.data)
            || error.message
            || error.toString();
        },
      );
    },
    handleLogin() {
      this.$router.push('/login');
    },
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

#userButton{
  margin-right: 1%;
}
</style>
