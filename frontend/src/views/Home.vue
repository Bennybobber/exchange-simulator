<template>
  <div class="home">
    <h1>SimEx Cryptocurrency Exchange Simulator </h1>

  <table class="table">
  <thead class="thead-dark">
    <tr>
      <th scope="col">Rank #</th>
      <th scope="col">Symbol</th>
      <th scope="col">Market Capitalisation</th>
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>BTC</td>
      <td>1 Trillion</td>
      <td>Trade</td>
    </tr>
  </tbody>
</table>

  </div>

</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    // HelloWorld,
  },
};
</script>

<style scoped>
.home{
  margin: auto;
  width: 75%;
}
</style>
