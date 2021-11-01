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

export default {
  name: 'App',
  components: {
    Nav,
    Footer,
  },
  data() {
    return {
      // logoURL: Logo
    };
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
  height: 100%;
}
#footer{
  overflow:hidden;
  height: 100%;
  width: 100%;
  clear: both;
}
</style>
