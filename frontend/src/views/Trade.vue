<template>
<div>
    <h1>Currency: {{ this.$route.params.coin }} </h1>
    <p> {{ loggedIn }} </p>
</div>
</template>

<script>
export default {
  data() {
    return {
      loggedIn: 'arg',
    };
  },
  created() {
    this.loggedIn = this.$route.query.page;
    console.log(this.$route.params);
  },
  methods: {

  },
};
</script>
