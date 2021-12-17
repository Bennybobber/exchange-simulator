<template>
<div id='tradeScreen'>
    <table class="table table-bordered table-dark">
      <thead>
        <tr>
          <th scope="col">{{this.$route.params.coin}}/USD</th>
          <th scope="col">Price</th>
          <th scope="col">24h Change</th>
          <th scope="col">24h Low</th>
          <th scope="col">24h High</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">{{ this.coinData.id }}</th>
          <td>${{ currentPrice }}</td>
          <td v-if=this.coinData.price_change_percentage_24h
            :style=setPercentageColour(this.coinData.price_change_percentage_24h)>
            {{ this.coinData.price_change_percentage_24h.toFixed(2) }}%
          </td>
          <td v-else>
            0%
          </td>
          <td>${{ this.coinData.low_24h }}</td>
          <td>${{ this.coinData.high_24h }}</td>
        </tr>
      </tbody>
    </table>
  <div class='tradeChart' :class="{ hide: !candlesExist }">
    <div class = "timeButtons">
      <div class="timeContainer">
      <button @click="retrieveCandlesticks('m15')"
        :class="{active: interval === 'm15' }"> 15m </button>
      <button @click="retrieveCandlesticks('m30')"
        :class="{active: interval === 'm30' }"> 30m </button>
      <button @click="retrieveCandlesticks('h1')"
        :class="{active: interval === 'h1' }"> 1hr </button>
      <button @click="retrieveCandlesticks('d1')"
        :class="{active: interval === 'd1' }"> 1d </button>
      <button @click="retrieveCandlesticks('w1')"
        :class="{active: interval === 'w1' }"> 1w </button>
      </div>
    </div>
    <trading-vue ref="tradingVue"
        :data="this.$data"
        :width="this.width"
        :height="this.height"
        :title-txt="`${this.$route.params.coin}USD`"
        :toolbar="true">
    </trading-vue>
    </div>
  <div class='noGraph' :class="{ hide: candlesExist }">
    <h1> There is currently no available graphs for this coin. </h1>
    <p> Please check back again at a future date, as graphs will become
      available as and when the API supports it! </p>
  </div>
  <div class='tradePanel'>
    <h1> USD Balance: {{ this.userBalance.toFixed(2) }} </h1>
    <h1> {{ this.$route.params.coin }} Balance: {{ this.assetBalance }} </h1>
    <div class='panel'>
      <h1> 1 {{ this.$route.params.coin }} = ${{ currentPrice }} </h1>
        <div class='inputForm'>
          <input v-on:input="updateAmount()" v-model='amount' class="form-control"
            @keypress='isNumber($event)'
            type="text"
            placeholder="Amount to Buy">
          <div>
            Total Cost: {{ this.totals.toFixed(2) }}
        </div>
      </div>
      <button @click="executeBuy(Number(amount), Number(totals))"
        type="button" class="btn btn-danger">
          Buy</button>
      <button @click="executeSell(Number(amount), Number(totals))"
        type="button" class="btn btn-success">
          Sell</button>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import TradingVue from 'trading-vue-js';
import UserService from '../services/user.service';
import EventBus from '../common/EventBus';

export default {
  components: {
    TradingVue,
  },
  data() {
    return {
      userData: {
        blanace: 0,
        assets: { [this.$route.params.coin]: 0 },
        trades: [],
      },
      coinData: {},
      UsdBalance: 0,
      loggedIn: 'arg',
      connection: null,
      price: null,
      amount: 0,
      totalCost: 0,
      width: window.innerWidth * 0.80,
      height: window.innerHeight * 0.60,
      ohlcv: [],
      interval: '1h',
      candlesExist: false,
    };
  },
  computed: {
    // Computed events so that all data on the page is kept up to date and updates
    // for the user without the need to refresh the page
    currentPrice: {
      get: function () {
        return this.price;
      },
      set: function (newPrice) {
        this.price = newPrice;
      },
    },
    chart: {
      get: function () {
        return this.ohlcv;
      },
      set: function (graphData) {
        this.ohlcv = graphData;
      },
    },
    latestChartPrice: {
      get: function () {
        return this.ohlcv;
      },
      set: function (latestPrice) {
        this.ohlcv[this.ohlcv.length - 1][4] = parseFloat(latestPrice);
      },
    },
    userBalance: {
      get: function () {
        return this.UsdBalance;
      },
      set: function (blanace) {
        this.UsdBalance = blanace;
      },
    },
    assetBalance: {
      get: function () {
        return this.userData.assets[this.$route.params.coin];
      },
      set: function (assetBalance) {
        this.userData.assets[this.$route.params.coin] = assetBalance;
      },
    },
    totals: {
      get: function () {
        return this.totalCost;
      },
      set: function (amount) {
        this.totalCost = amount;
      },
    },
  },
  created() {
    // Fetch user, candlestick, and coin data to set the page up when a user arrives.
    this.fetchUser();
    this.retrieveCandlesticks();
    this.retrieveCoinInformation();
    this.loggedIn = this.$route.query.page;
    // Connects to the websocket for the current asset to recieve constant real time updates.
    this.connection = new WebSocket(`wss://ws.coincap.io/prices?assets=${this.$route.params.name}`);

    this.connection.onmessage = (event) => {
      // Every time the price updates, make sure to update the current price, the chart price,
      // the chart and the amount users will have to pay for a trade.
      const price = JSON.parse(event.data);
      this.currentPrice = price[this.$route.params.name];
      if (this.ohlcv.length !== 0) {
        this.latestChartPrice = price[this.$route.params.name];
      }
      try {
        this.chart = this.latestChartPrice;
      } catch {
        this.chart = [];
      }
      this.updateAmount();
    };
    this.connection.onopen = function (event) {
      console.log(event);
    };
  },
  methods: {
    async retrieveCandlesticks(interval = 'h1') {
      /**
       * Retrieves the candlestick history data from the backend api
       * using parameters for the crypto asset as well as the interval
       * :params: interval - The timeframe of candlesticks that we want.
       */
      await axios({
        method: 'get',
        url: 'http://localhost:5000/api/coin/history',
        params: { coin: this.$route.params.name, interval: interval },
      })
        .then((response) => {
          if (response.data.data !== undefined) {
            this.$refs.tradingVue.resetChart();
            console.log(response.data.data.length);
            if (response.data.data.length !== 0) {
              this.chart = this.stripDictonary(response.data.data);
              this.interval = interval;
              this.candlesExist = true;
            } else { this.candlesExist = false; }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async retrieveCoinInformation() {
      /**
       * Retrieves the information about the given coin from the backend api
       */
      await axios({
        method: 'get',
        url: 'http://localhost:5000/api/coin/info',
        params: { symbol: this.$route.params.coin },
      })
        .then((response) => {
          this.currentPrice = Number(response.data.current_price).toFixed(2);
          this.coinData = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    stripDictonary(data) {
      /**
       * Takes the response data and splits it into open, high, low, close, volume
       * data for the chart to take in.
       */
      const completeList = [];
      let subList = [];
      console.log(data);
      data.forEach((element) => {
        subList.push(element.period);
        subList.push(parseFloat(element.open));
        subList.push(parseFloat(element.high));
        subList.push(parseFloat(element.low));
        subList.push(parseFloat(element.close));
        subList.push(parseFloat(element.volume));
        completeList.push(subList);
        subList = [];
      });
      return completeList;
    },
    fetchUser() {
      /**
       * Retrieves the user object from the dictionary hosted on the backend flask framework.
       */
      UserService.getUser().then(
        (response) => {
          this.userData = response.data;
          this.UsdBalance = response.data.balance;
          if (this.userData.assets[this.$route.params.coin] === undefined) {
            this.$set(this.userData.assets, this.$route.params.coin, 0);
          }
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
    },
    setPercentageColour(percentage) {
      /**
       * Checks to see if the 24h % change is negative, if it is
       * changes it to red, else changes it to green.
       * :params:
       *      percentage (String): String value of the percentage.
       * :return:
       *    color (String): string of the CSS colour style.
       */
      if (percentage == null) return '';
      const color = (String(percentage).includes('-')) ? 'red' : 'green';
      return `color: ${color}`;
    },
    executeBuy(amount, total) {
      /**
       * Executes a buy trade for a given coin, checking that the user first has enough
       * balance available and the total they're trying to buy is more than 0
       * :params:
       *      amount (integer): The amount of an asset the user wants to buy
       *      total (integer): The total cost of the asset trade
       */
      if (this.userBalance >= total && amount !== 0) {
        if (window.confirm('Are you sure you want to execute this buy?')) {
          this.userBalance -= total;
          this.userData.trades.push({
            trade_time: new Date().getTime(),
            type: 'buy',
            asset: this.$route.params.coin,
            amount: amount,
            usd_cost: total,
            asset_cost: total / amount,
          });
          const assetBalance = this.assetBalance + amount;
          this.updateDatabase(assetBalance);
        }
      }
      this.amount = 0;
    },
    executeSell(amount, total) {
      /**
       * Executes a sell trade for an asset, by first checking to see if the user has enough
       * of the asset to sell, and ensuring that they want to sell more than 0 of the asset.
       * :params:
       *      amount (integer): The amount of an asset the user wants to sell
       *      total (integer): The total cost of the asset trade
       */
      if (this.assetBalance >= amount && amount !== 0) {
        if (window.confirm('Are you sure you want to execute this sell?')) {
          this.userBalance += total;
          this.userData.trades.push({
            trade_time: new Date().getTime(),
            type: 'sell',
            asset: this.$route.params.coin,
            amount: amount,
            usd_cost: total,
            asset_cost: total / amount,
          });
          const assetBalance = this.assetBalance - amount;
          this.updateDatabase(assetBalance);
        }
      }
      this.amount = 0;
    },
    updateAmount() {
      // Dynamically updates the total cost of a buy/sell trade for the user.
      this.totals = this.amount * this.currentPrice;
    },
    updateDatabase(assetBalance) {
      // Sends an update to the database after a buy or sell has been executed to update a user.
      UserService.updateUser(this.userData).then(
        (response) => {
          console.log(response);
          this.userData.balance = this.userBalance;
          this.assetBalance = assetBalance;
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
    },
    isNumber(inputEvent) {
      /**
       * Checks to see that a number and only 1 decimal point can be used. Will reject any other
       * characters that are entered in.
       * :params:
       *      inputEvent (char): The character a user inputs into the input box for a buy/sell
       */
      const event = inputEvent || window.event;
      const charCode = (event.which) ? event.which : event.keyCode;
      if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
        event.preventDefault();
      }
      if (String(this.amount).includes('.') && charCode === 46) event.preventDefault();
    },
  },
  beforeRouteLeave(to, from, next) {
    // called when the route that renders this component is about to
    // be navigated away from.
    // has access to `this` component instance.

    // close the connection if the user is going to another page.
    this.connection.close();
    next();
  },
};
</script>
<style scoped>
.hide {
  visibility: hidden !important;
}
.tradePanel{
  color:white;
  margin:auto;
  width: 75%;
  padding: 3%;
}
.tradePanel h1{
  display:inline;
  padding: 5%;
}
.panel{
  display:inline-block;
  width:100%;
  margin:auto;
  padding:2%;
  border-style: solid;
}
.panel h1{
  display: inline-block;
  margin: auto;
}
.panel button{
  width: 100px;
  height: 50px;
  margin: 1%;
}
.inputPanel{
  display:flex;
}
.inputForm{
  display:block;
  width:50%;
  margin:auto;
  padding:1%;
}
.inputForm{
  font-weight: bold;
  font-size: large;
}
.tradeChart{
  margin:auto;
  width:100%;
}
.trading-vue{
  margin:auto;
}
.timeButtons{
  width: 80.5%;
  margin: auto;
}
.timeContainer{
  margin-left: auto;
  margin-right: auto;
  display:flex;
  justify-content: flex-end;
}
.timeContainer button{
  width: 5%;
  border-style: solid;
  display: inline-block;
}
#tradeScreen{
  background-color: rgb(41, 39, 39);
}
.active{
  background-color: gray;
}
.noGraph {
  border-style: solid;
  background-color: red;
}
@media only screen and (max-width: 600px) {
.tradePanel{
  width: 100%;
}
.tradePanel h1{
 text-align: left;
 display: block;
}
.inputForm{
  width: 100%;
}
.panel h1{
  text-align: center;
}
.timeContainer button{
  width: 25%;
}
}

</style>
