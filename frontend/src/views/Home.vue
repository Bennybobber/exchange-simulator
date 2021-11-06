<template>
  <div class="home">
    <div id="introduction">
    <h1>SimEx Cryptocurrency Exchange Simulator </h1>
    <p>Welcome to SimEx, a cryptocurrency simulator that utilises the latest cryptocurrnecy prices.
      Sign up today, and instantly get access to $100,000 US dollars that can be traded across the
      simulator.</p>
    </div>

  <table class="table">
  <thead class="thead-dark">
    <tr>
      <th scope="col">Rank #</th>
      <th scope="col">Symbol</th>
      <th scope="col">Currency Name</th>
      <th scope="col">Market Capitalisation</th>
      <th scope="col">Current Price (USD) </th>
      <th scope="col">24hr Price High</th>
      <th scope="col">Percentage Change 24hr</th>
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="row in marketRowData" :key="row.currencyName">
      <th scope="row"> {{ row.rank }}</th>
      <td><img :src="row.currencyImg"> <b> {{ row.currencySymbol}} </b></td>
      <td>{{ row.currencyName }}</td>
      <td><b>$</b>{{ row.mCap }}</td>
      <td><b>$</b>{{ row.currentPrice }}</td>
      <td><b>$</b>{{ row.day_high}}</td>
      <td :style=setPercentageColour(row.day_percentage_change)>{{ row.day_percentage_change}}%</td>
      <td><router-link :to='"/trade/"+ row.currencySymbol' class="nav-link">Trade</router-link></td>
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
      currencyImg: '',
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
    try {
      const user = localStorage.getItem('user');
      if (user != null) {
        console.log(user);
      }
    } catch (error) {
      console.log('User not logged in');
    }
  },
  methods: {
    extractData(marketData) {
      Object.keys(marketData).forEach((key) => {
        const row = {
          currencyName: marketData[key].id,
          currencyImg: marketData[key].image,
          currencySymbol: marketData[key].symbol.toUpperCase(),
          currentPrice: marketData[key].current_price,
          day_high: marketData[key].high_24h,
          day_percentage_change: marketData[key].price_change_percentage_24h.toPrecision(2),
          mCap: marketData[key].market_cap.toLocaleString(),
          rank: marketData[key].market_cap_rank,
        };
        this.marketRowData.push(row);

        this.currencyName = '';
        this.currencyImg = '';
        this.currencySymbol = '';
        this.currentPrice = '';
        this.day_high = '';
        this.day_percentage_change = '';
        this.mCap = '';
        this.rank = '';
      });
    },
    setPercentageColour(percentage) {
      const color = (percentage.includes('-')) ? 'red' : 'green';
      return `color: ${color}`;
    },
  },
};
</script>

<style scoped>
.home{
  margin: auto;
  width: 75%;
}
h1{
  padding: 2%;
  font-weight: bold;
}
#introduction p{
  padding: 5%;
}
#introduction{
  width: 50%;
  margin: auto;
}
td img{
  width: 15%;
  margin: 1%;
}
td p{
  font-weight: bold;
}
td {
  margin: auto;
}
</style>
