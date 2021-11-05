<template>
  <div class="container">
    <div class='profileBanner'>
        <h3>
          <strong>{{userData.username}}</strong> Portfolio
        </h3>
          <p class='balance'>
            <strong>Balance:</strong>
            ${{userData.balance}}
        </p>
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
          <tr v-for="row in marketRowData" :key="row.currencyName">
            <th scope="row"> {{ row.rank }}</th>
            <td><img :src="row.currencyImg"> <b> {{ row.currencySymbol}} </b></td>
            <td>{{ row.currencyName }}</td>
            <td><b>$</b>{{ row.mCap }}</td>
            <td><b>$</b>{{ row.currentPrice }}</td>
            <td> <a :href="'http://localhost:8080/api/trade?coin=' + row.currencySymbol">Trade</a></td>
          </tr>
        </tbody>
      </table>
      </div>
    <p>
      <strong>Id:</strong>
      {{currentUser.id}}
    </p>
    <strong>Authorities:</strong>
    <ul>
      <li v-for="(role,index) in currentUser.roles" :key="index">{{role}}</li>
    </ul>
  </div>
</template>

<script>
import UserService from '../services/user.service';
import EventBus from '../common/EventBus';

export default {
  name: 'Portfolio',
  data() {
    return {
      userData: {},
      rowData: {},
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    getAccessToken() {
      return this.$store.state.auth.user;
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
      console.log(userData);
      this.userData = userData;
      if (Object.keys(userData.assets).length === 0) {
        console.log('No Assets Currently Owned');
      }
      const assetPrices = this.getAssetsPrice(userData);
      this.populateAssetTable(assetPrices);
    },
    getAssetsPrice(userAssets) {
      return userAssets;
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
.balance{
  margin-left: auto;
}
</style>
