<template>
<div>
  <div class='coinInformation'>
    <h1>Currency: {{ this.$route.params.coin }} </h1>
    <p> Latest Price: ${{ currentPrice }} </p>
  </div>
  <div class='tradeChart'>
    <trading-vue :data="this.$data" :width="this.width" :height="this.height"
        :title-txt="`${this.$route.params.coin}USD`"
        :toolbar="true">
    </trading-vue>
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
import axios from 'axios';
import TradingVue from 'trading-vue-js';

export default {
  components: {
    TradingVue,
  },
  data() {
    return {
      loggedIn: 'arg',
      connection: null,
      price: null,
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
        // this.ohlcv.at(-1).at(-2) = parseFloat(newPrice);
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
  },
  created() {
    this.retrieveCandlesticks();
    this.retrieveCoinInformation();
    this.loggedIn = this.$route.query.page;
    console.log('Setting Up New Websocket Connection');
    this.connection = new WebSocket(`wss://ws.coincap.io/prices?assets=${this.$route.params.name}`);

    this.connection.onmessage = (event) => {
      const price = JSON.parse(event.data);
      this.currentPrice = price[this.$route.params.name];
      this.latestChartPrice = price[this.$route.params.name];
      this.chart = this.latestChartPrice;
    };
    this.check();
    this.connection.onopen = function (event) {
      console.log(event);
      console.log('successfully connected to the websocket server...');
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
        params: { symbol: this.$route.params.name },
      })
        .then((response) => {
          this.currentPrice = Number(response.data.data.priceUsd).toFixed(2);
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
  display:flex;
  margin:auto;
}
.panel{
  display:flex;
  width:50%;
  margin:auto;
  padding:2%;
}
.tradeChart{
  margin:auto;
  width:100%;
}
.trading-vue{
  margin:auto;
}
</style>
