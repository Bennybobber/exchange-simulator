<template>
  <div class="container">
    <div class='profileBanner'>
      <div class='profileHeading'>
        <h3>
          <strong>{{userData.username}}'s</strong> Portfolio
        </h3>
        <button  @click="resetProfile" class="btn btn-danger"> Reset Profile</button>
      </div>
        <div class='balances'>
          <p class='balance'>
            <strong>USD Balance:</strong>
            ${{userData.balance.toFixed(2)}}
          </p>
          <p>
            <strong>Portfolio Worth ($USD): </strong>
            ${{getPortfolioWorth}}
          </p>
        </div>
    </div>
    <div class='mainContent'>
     <div class='pieCharts'>
       <h1>Portfolio Break Down</h1>
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
    <div class='tables'>
    <div class='assetTable'>
      <h1> Assets Owned </h1>
      <table class="table">
        <thead>
          <tr>
            <th @click="assetSort('currencyName')" scope="col">Currency Name</th>
            <th @click="assetSort('currencySymbol')" scope="col">Symbol</th>
            <th @click="assetSort('amountOwned')" scope="col">Amount Owned</th>
            <th @click="assetSort('currentPrice')" scope="col">Current Price</th>
            <th @click="assetSort('totalWorth')" scope="col">Total Worth (USD)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in sortedCurrencies" :key="row.currencyName">
            <th scope="row"> {{ row.currencyName }}</th>
            <td><img :src="row.currencyImg"> <b> {{ row.currencySymbol}} </b></td>
            <td>{{ row.amountOwned }}</td>
            <td><b>$</b>{{ row.currentPrice }}</td>
            <td><b>$</b>{{ row.totalWorth }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="this.rowData.length <= 10" class="navButtons">
        <button @click="prevAssetPage" class="btn btn-dark">Previous</button>
        <div class="divider"/>
        <button @click="nextAssetPage" class="btn btn-dark">Next</button>
        </div>
      </div>
      <div class="divider"/>
      <h1> Recent Trades </h1>
      <table class="table">
        <thead>
          <tr>
            <th @click="sort('trade_time')" scope="col">Trade Date</th>
            <th @click="sort('type')" scope="col">Trade Type</th>
            <th @click="sort('asset')" scope="col">Asset</th>
            <th @click="sort('amount')" scope="col">Amount Traded</th>
            <th @click="sort('usd_cost')" scope="col">Total Worth (USD)</th>
            <th @click="sort('asset_cost')" scope="col">Asset Worth At Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in sortedTrades" :key="row.trade_time">
            <th scope="row">
              {{ new Date(row.trade_time) }}
            </th>
            <td :style=setTradeColour(row.type)><b> {{ row.type}} </b></td>
            <td>{{ row.asset }}</td>
            <td>{{ row.amount }}</td>
            <td><b>$</b>{{ row.usd_cost }}</td>
            <td><b>$</b>{{ row.asset_cost }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="this.tradeRowData.length >= 10" class="navButtons">
        <button @click="prevTradePage" class="btn btn-dark">Previous</button>
        <div class="divider"/>
        <button @click="nextTradePage" class="btn btn-dark">Next</button>
      </div>
      <div class="divider"/>
      </div>
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
      userData: {
        balance: 10000,
        assets: {},
        trades: [],
      },
      pieAssetMakeup: [[]],
      pieValueMakeup: [[]],
      portfolioWorth: 0,
      rowData: [],
      tradeRowData: [],
      currentAssetPage: 1,
      currentTradePage: 1,
      pageSize: 10,
      currentSort: 'trade_time',
      currentSortDir: 'asc',
      currentAssetSortDir: 'desc',
      currentAssetSort: 'amountOwned',
    };
  },
  computed: {
    sortedCurrencies: function () {
      return this.updateAssetPage();
    },
    sortedTrades: function () {
      return this.updateTradePage();
    },
    currentUser() {
      return this.$store.state.auth.user;
    },
    getAccessToken() {
      return this.$store.state.auth.user;
    },
    getPortfolioWorth() {
      return this.portfolioWorth.toFixed(2);
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
    this.getUser();
  },
  methods: {
    getUser() {
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
    setupPortfolio(userData) {
      this.userData = userData;
      const assetValue = [];
      const assetWorth = [];
      this.rowData = [];
      axios({
        method: 'get',
        url: 'http://localhost:5000/api/market',
      })
        .then((response) => {
          if (Object.keys(userData.assets).length !== 0) {
            Object.keys(userData.assets).forEach((key) => {
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
      this.populateRecentTrades();
    },
    populateRecentTrades() {
      this.tradeRowData = this.userData.trades;
    },
    populateOwnedTable(assetAmount, marketData) {
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
    updateAssetPage: function () {
      return this.rowData.sort((a, b) => {
        let modifier = 1;
        if (this.currentAssetSortDir === 'desc') modifier = -1;
        if (a[this.currentAssetSort] < b[this.currentAssetSort]) return -1 * modifier;
        if (a[this.currentAssetSort] > b[this.currentAssetSort]) return 1 * modifier;
        return 0;
      }).filter((row, index) => {
        const start = (this.currentAssetPage - 1) * this.pageSize;
        const end = this.currentAssetPage * this.pageSize;
        if (index >= start && index < end) return true;
        return false;
      });
    },
    updateTradePage: function () {
      return this.tradeRowData.sort((a, b) => {
        let modifier = 1;
        if (this.currentSortDir === 'desc') modifier = -1;
        if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      }).filter((row, index) => {
        const start = (this.currentTradePage - 1) * this.pageSize;
        const end = this.currentTradePage * this.pageSize;
        if (index >= start && index < end) return true;
        return false;
      });
    },
    sort: function (s) {
      // if s == current sort, reverse
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
      }
      this.currentSort = s;
    },
    assetSort: function (s) {
      // if s == current sort, reverse
      console.log('Hewwo');
      if (s === this.currentAssetSort) {
        this.currentAssetSortDir = this.currentAssetSortDir === 'asc' ? 'desc' : 'asc';
      }
      this.currentAssetSort = s;
    },
    nextAssetPage: function () {
      if ((this.currentAssetPage * this.pageSize) < this.rowData.length) this.currentAssetPage += 1;
    },
    prevAssetPage: function () {
      if (this.currentAssetPage > 1) this.currentAssetPage -= 1;
    },
    nextTradePage: function () {
      if ((this.currentTradePage * this.pageSize) < this.tradeRowData.length) {
        this.currentTradePage += 1;
      }
    },
    prevTradePage: function () {
      if (this.currentTradePage > 1) this.currentTradePage -= 1;
    },
    setTradeColour: function (tradeType) {
      const color = (tradeType.includes('sell')) ? 'red' : 'green';
      return `color: ${color}`;
    },
    resetProfile: function () {
      if (window.confirm('Are you sure you want to RESET your profile?')) {
        this.userData.assets = {};
        this.userData.trades = [];
        this.userData.balance = 100000;
        UserService.updateUser(this.userData).then(
          (response) => {
            console.log(response);
            this.getUser();
          },
          (error) => {
            this.content = (error.response && error.response.data && error.response.data.message)
            || error.message
            || error.toString();

            if (error.response && error.response.status === 403) {
              EventBus.dispatch('logout');
            }
          },
        );
      }
    },
  },
};
</script>

<style scoped>
.mainContent{
  display: flex;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}
.tables{
  width: 100%;
  border-bottom: solid;
  border-right: solid;
  border-top: solid;
  padding: 1%;
}
.profileBanner{
  min-width: 0px;
  display:flex;
  border-style: solid;
  width: 100%;
  padding: 1%;
  background-color: black;
  color: white;
  border-color: #0d6efd;
}
.profileBanner button{
  height: 50%;
  display: flex;
}
.container{
  min-width: 100%;
  background-color: lavender;
  margin: 0 !important;
  padding: 0 !important;
}
.balances{
  margin-left: auto;
  text-align: left;
}
.pieCharts{
  width: 25%;
  border-style: solid;
  display:block;
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
td, tr{
  border:solid;
  border-color: black;
}
table thead{
  background-color: black;
  color: white;
}
th {
  cursor:pointer;
}
.divider{
    width:5px;
    height:auto;
    display:inline-block;
}
</style>
