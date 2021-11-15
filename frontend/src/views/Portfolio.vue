<template>
  <div class="container">
    <div class='profileBanner'>
        <h3>
          <strong>{{userData.username}}'s</strong> Portfolio
        </h3>
        <div class='balances'>
          <p class='balance'>
            <strong>USD Balance:</strong>
            ${{userData.balance}}
          </p>
          <p>
            <strong>Portfolio Worth ($USD): </strong>
            ${{getPortfolioWorth}}
          </p>
        </div>
    </div>
     <h1>Portfolio Break Down</h1>
     <div class='pieCharts'>
        <div class='chart'>
          <h4>Makeup by assets worth $USD</h4>
          <pie-chart :data="pieValueMakeup">
          </pie-chart>
        </div>
        <div class='chart'>
          <h4>Makeup by assets owned</h4>
          <pie-chart :data="pieAssetMakeup">
          </pie-chart>
        </div>
    </div>
    <div class='assetTable'>
      <table class="table">
        <thead class="thead-dark">
          <tr>
            <th scope="col">Currency Name</th>
            <th scope="col">Symbol</th>
            <th scope="col">Amount Owned</th>
            <th scope="col">Current Price</th>
            <th scope="col">Total Worth (USD)</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rowData" :key="row.currencyName">
            <th scope="row"> {{ row.currencyName }}</th>
            <td><img :src="row.currencyImg"> <b> {{ row.currencySymbol}} </b></td>
            <td>{{ row.amountOwned }}</td>
            <td><b>$</b>{{ row.currentPrice }}</td>
            <td><b>$</b>{{ row.totalWorth }}</td>
          </tr>
        </tbody>
      </table>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserService from '../services/user.service';
import EventBus from '../common/EventBus';

export default {
  name: 'Portfolio',
  data() {
    return {
      userData: {},
      pieAssetMakeup: [['USD', '100000']],
      pieValueMakeup: [['USD', '100000']],
      portfolioWorth: 0,
      rowData: [],
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    getAccessToken() {
      return this.$store.state.auth.user;
    },
    getPortfolioWorth() {
      return this.portfolioWorth;
    },
    assetPie: {
      get: function () {
        return this.pieAssetMakeup;
      },
      set: function (assetPie) {
        this.pieAssetMakeup = assetPie;
      },
    },
    valuePie: {
      get: function () {
        return this.pieValueMakeup;
      },
      set: function (assetPie) {
        this.pieValueMakeup = assetPie;
      },
    },
  },
  mounted() {
    if (this.currentUser == null) {
      this.$router.push('/login');
    }
    UserService.getUser().then(
      (response) => { this.setupPortfolio(response.data); },
      (error) => {
        this.content = (error.response && error.response.data && error.response.data.message)
          || error.message
          || error.toString();

        if (error.response && error.response.status === 403) {
          EventBus.dispatch('logout');
        }
      },
    );
  },
  methods: {
    setupPortfolio(userData) {
      this.userData = userData;
      const assetValue = [];
      const assetWorth = [];
      console.log('setting up...');
      axios({
        method: 'get',
        url: 'http://localhost:5000/api/market',
      })
        .then((response) => {
          if (Object.keys(userData.assets).length !== 0) {
            Object.keys(userData.assets).forEach((key) => {
              console.log(`${key}: ${userData.assets[key]}`);
              if (userData.assets[key] !== 0) {
                assetValue.push([key, userData.assets[key]]);
                response.data.markets.forEach((crypto) => {
                  if (crypto.symbol.toUpperCase() === key) {
                    assetWorth.push([key, crypto.current_price]);
                    this.portfolioWorth += (crypto.current_price * Number(userData.assets[key]));
                    this.populateOwnedTable(userData.assets[key], crypto);
                  }
                });
              }
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
      this.valuePie = assetWorth;
      this.assetPie = assetValue;
      const assetPrices = this.getAssetsPrice(userData.assets);
      this.populateAssetTable(assetPrices);
    },
    populateOwnedTable(assetAmount, marketData) {
      console.log(assetAmount);
      console.log(marketData);
      const row = {
        currencyName: marketData.name,
        currencyImg: marketData.image,
        currencySymbol: marketData.symbol,
        amountOwned: assetAmount,
        currentPrice: marketData.current_price,
        totalWorth: (marketData.current_price * assetAmount),
      };
      this.rowData.push(row);
    },
    populateAssetTable(userAssets) {
      return userAssets;
    },
  },
};
</script>

<style scoped>
.profileBanner{
  box-sizing: border-box;
  margin: 0px;
  min-width: 0px;
  display:flex;
  flex-flow: row wrap;
}
.container{
  width: 100%;
  height: 100%;
  background-color: lavender;
}
.balances{
  margin-left: auto;
  text-align: left;
}
.pieCharts{
  width: 100%;
  border-style: solid;
  display:flex;
}
.chart{
  margin: auto;
  padding: 1%;
}
td img{
  width: 15%;
  margin: 1%;
}
td p{
  font-weight: bold;
}
</style>
