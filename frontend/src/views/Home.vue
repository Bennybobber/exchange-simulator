<template>
  <div class="home">
    <h1>SimEx Cryptocurrency Exchange Simulator </h1>

  <table class="table">
  <thead class="thead-dark">
    <tr>
      <th scope="col">Rank #</th>
      <th scope="col">Symbol</th>
      <th scope="col">Currency Name</th>
      <th scope="col">Market Capitalisation</th>
      <th scope="col">24hr Price High</th>
      <th scope="col">Percentage Change 24hr</th>
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="row in marketRowData" :key="row.currencyName">
      <th scope="row"> {{ row.rank }}</th>
      <td>{{ row.currencySymbol }}</td>
      <td>{{ row.currencyName }}</td>
      <td>{{ row.mCap }}</td>
      <td>{{ row.day_high}}</td>
      <td>{{ row.day_percentage_change}}</td>
      <td> <a href="">Trade</a></td>
    </tr>
  </tbody>
</table>

  </div>

</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue';
import axios from 'axios';

export default {
  name: 'Home',
  components: {
    // HelloWorld,
  },
  data() {
    return {
      currencyName: '',
      currencySymbol: '',
      currentPrice: '',
      day_high: '',
      day_percentage_change: '',
      mCap: '',
      rank: '',
      marketRowData: [],
    };
  },
  created() {
    axios({
      method: 'get',
      url: 'http://localhost:5000/api/market',
    })
      .then((response) => {
        this.extractData(response.data.markets);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    extractData(marketData) {
      console.log(marketData);
      Object.keys(marketData).forEach((key) => {
        // console.log(marketData.markets[key]);
        console.log(marketData[key]);
        const row = {
          currencyName: marketData[key].id,
          currencySymbol: marketData[key].symbol,
          currentPrice: marketData[key].current_price,
          day_high: marketData[key].high_24h,
          day_percentage_change: marketData[key].price_change_percentage_24h,
          mCap: marketData[key].market_cap,
          rank: marketData[key].market_cap_rank,
        };
        console.log(row);
        this.marketRowData.push(row);

        this.currencyName = '';
        this.currencySymbol = '';
        this.currentPrice = '';
        this.day_high = '';
        this.day_percentage_change = '';
        this.mCap = '';
        this.rank = '';
      });
    },
  },
};
</script>

<style scoped>
.home{
  margin: auto;
  width: 75%;
}
</style>
