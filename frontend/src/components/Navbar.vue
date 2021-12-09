<!-- src/components/Courses.vue -->

<template>
  <nav class="navbar navbar-expand-lg navbar">
    <img src="@/assets/SimEx.jpg">
  <div class ='nav-items' id="navbarText">
    <ul class="navbar-nav">
      <li class="nav-item">
        <router-link to="/" class="nav-link color">Home</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/portfolio" class="nav-link color">Portfolio</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/trade/BTC/bitcoin" class="nav-link color">Trade</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/learn" class="nav-link color">Learn</router-link>
      </li>
    </ul>
  </div>
  <div class='loginB' id="userButton" style="margin-left: auto;">
      <button class="btn p-3 mb-2 bg-black text-light"
        v-if="this.$store.state.auth.status.loggedIn"
          @click="handleLogout()">
            Logout
      </button>
      <button class="btn p-3 mb-2 bg-black text-light" v-else @click="handleLogin()">Login</button>
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
nav img{
  width: 5%;
  margin-right: 1%;
  margin-left: 1%;
}
nav {
  background-color: #298cd6;
}
.nav-labels{
  display: flex;
}
.color{
  color: white;
}
ul li{
  font-size: 150%;
}
@media only screen and (max-width: 600px) {
  #userButton{
    margin-right: 5%;
  }
  nav{
    height: 20%;
    display: flex;
  }
  .loginB button{
    display: flex;
    margin-right: 2%;
  }
  nav ul{
    margin: auto;
    flex-direction: row;
  }
  nav ul li {
    display: block;
    list-style-type: none;
    padding: 3%;
    margin: 1%;
  }
  ul li{
  font-size: 0.9rem;
}
  nav img{
    display: none;
  }
}
</style>
