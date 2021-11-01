<template>
  <div class="container">
    <header class="jumbotron">
      <h3>
        <strong>{{currentUser.username}}</strong> Profile
      </h3>
    </header>
    <p>
      <strong>Token:</strong>
      {{currentUser.accessToken.substring(0, 20)}} ...
      {{currentUser.accessToken.substr(currentUser.accessToken.length - 20)}}
    </p>
    <p>
      <strong>Id:</strong>
      {{currentUser.id}}
    </p>
    <strong>Authorities:</strong>
    <ul>
      <li v-for="(role,index) in currentUser.roles" :key="index">{{role}}</li>
    </ul>
  </div>
</template>

<script>
import UserService from '../services/user.service';

export default {
  name: 'Portfolio',
  computed: {
    currentUser() {
      console.log(this.$store.state.auth.user);
      return this.$store.state.auth.user;
    },
    getAccessToken() {
      console.log(this.$store.state.auth.user);
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    if (this.currentUser == null) {
      this.$router.push('/login');
    }
    const accessToken = this.getAccessToken;
    console.log(accessToken);
    this.getUserInfo();
  },
  methods: {
    getUserInfo() {
      UserService.getUser().then(
        (response) => {
          console.log(response.data);
        },
        (error) => {
          this.content = (error.response && error.response.data)
          || error.message
          || error.toString();
        },
      );
    },
  },
};
</script>
