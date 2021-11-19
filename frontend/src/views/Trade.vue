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
          <td :style=setPercentageColour(this.coinData.price_change_percentage_24h)>
            {{ this.coinData.price_change_percentage_24h.toFixed(2) }}%
          </td>
          <td>{{ this.coinData.low_24h }}</td>
          <td>{{ this.coinData.high_24h }}</td>
        </tr>
      </tbody>
    </table>
  <div class='tradeChart'>
    <trading-vue :data="this.$data" :width="this.width" :height="this.height"
        :title-txt="`${this.$route.params.coin}USD`"
        :toolbar="true">
    </trading-vue>
    </div>
  <div class='tradePanel'>
    <h1> USD Balance: {{ this.userBalance }} </h1>
    <h1> {{ this.$route.params.coin }} Balance: {{ this.assetBalance }} </h1>
    <div class='panel'>
      <h1> 1 {{ this.$route.params.coin }} = ${{ currentPrice }} </h1>
        <div class='inputForm'>
          <input v-on:input="updateAmount()" v-model='amount' class="form-control"
            @keypress='isNumber($event)'
            type="text"
            placeholder="Amount to Buy">
          <div>
            Total Cost: {{ this.totals }}
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
      width: window.innerWidth * 0.75,
      height: window.innerHeight * 0.75,
      ohlcv: [
      ],
    };
  },
  computed: {
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
    this.fetchUser();
    this.retrieveCandlesticks();
    this.retrieveCoinInformation();
    this.loggedIn = this.$route.query.page;
    this.connection = new WebSocket(`wss://ws.coincap.io/prices?assets=${this.$route.params.name}`);

    this.connection.onmessage = (event) => {
      const price = JSON.parse(event.data);
      this.currentPrice = price[this.$route.params.name];
      this.latestChartPrice = price[this.$route.params.name];
      this.chart = this.latestChartPrice;
      this.updateAmount();
    };
    this.connection.onopen = function (event) {
      console.log(event);
    };
  },
  methods: {
    retrieveCandlesticks() {
      axios({
        method: 'get',
        url: 'http://localhost:5000/api/coin/history',
        params: { coin: this.$route.params.name, interval: 'h1' },
      })
        .then((response) => {
          this.chart = this.stripDictonary(response.data.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    retrieveCoinInformation() {
      axios({
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
      const completeList = [];
      let subList = [];
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
      if (percentage == null) return '';
      const color = (String(percentage).includes('-')) ? 'red' : 'green';
      return `color: ${color}`;
    },
    executeBuy(amount, total) {
      if (this.userBalance >= total && amount !== 0) {
        if (window.confirm('Are you sure you want to execute this sell?')) {
          this.userBalance -= total;
          this.userData.trades.push({
            trade_time: new Date().getTime(),
            type: 'buy',
            asset: this.$route.params.coin,
            amount: amount,
            usd_cost: total,
            asset_cost: total / amount,
          });
          this.assetBalance += amount;
          this.updateDatabase();
        }
      }
      this.amount = 0;
    },
    executeSell(amount, total) {
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
          this.assetBalance -= amount;
          this.updateDatabase();
        }
      }
      this.amount = 0;
    },
    updateAmount() {
      this.totals = this.amount * this.currentPrice;
    },
    updateDatabase() {
      this.userData.balance = this.userBalance;
      UserService.updateUser(this.userData).then(
        (response) => { console.log(response); },
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
      const event = inputEvent || window.event;
      const charCode = (event.which) ? event.which : event.keyCode;
      if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
        event.preventDefault();
      }
      if (String(this.amount).includes('.') && charCode === 46) event.preventDefault();
    },
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
  },
  beforeRouteLeave(to, from, next) {
    // called when the route that renders this component is about to
    // be navigated away from.
    // has access to `this` component instance.

    // this.connection is your ws
    this.connection.close();
    next();
  },
};
</script>
<style scoped>
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
  display:flex;
  width:50%;
  margin:auto;
  padding:1%;
}
.tradeChart{
  margin:auto;
  width:100%;
}
.trading-vue{
  margin:auto;
}
#tradeScreen{
  background-color: rgb(41, 39, 39);
}
</style>
