<template>
<div>
  <div class='coinInformation'>
    <h1>Currency: {{ this.$route.params.coin }} </h1>
    <p> {{ loggedIn }} </p>
  </div>
  <div class='tradePanel'>
    <div id='sellForm' class='panel'>
      <input class="form-control" type="text" placeholder="Amount to Sell">
    <button type="button" class="btn btn-success">Sell</button>
    </div>
    <div id='buyForm' class='panel'>
      <input class="form-control" type="text" placeholder="Amount to Buy">
      <button type="button" class="btn btn-danger">Buy</button>
    </div>
  </div>
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
<style scoped>
.tradePanel{
  display:flex;
  width:75%;
  margin:auto;
}
.panel{
  display:flex;
  width:50%;
  margin:auto;
  padding:2%;
}
</style>
