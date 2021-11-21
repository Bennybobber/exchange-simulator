<template>
  <div id="app">
    <Nav />
    <div id="content-wrap">
      <router-view/>
    </div>
    <div id="footer">
    <Footer />
    </div>
  </div>
</template>

<script>
import Nav from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import EventBus from './common/EventBus';

export default {
  name: 'App',
  components: {
    Nav,
    Footer,
  },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    },
  },
  data() {
    return {
      // logoURL: Logo
    };
  },
  mounted() {
    EventBus.on('logout', () => {
      this.logOut();
    });
  },
  beforeDestroy() {
    EventBus.remove('logout');
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: relative;
  min-height: 100vh;
}
body, html{
  margin: 0;
  height: 100%;
  width: 100%;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
#content-wrap{
  min-height: 100%;
  padding-bottom: 10rem;
}
#footer{
  overflow:hidden;
  height: 100%;
  width: 100%;
  clear: both;
}
</style>
