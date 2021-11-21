<template>
    <div class="content">
      <div class='jumbotron'
        >
        <div class='topHeading'>
          <h1>What is cryptocurrency?</h1>
          <h3>Cryptocurrencies are digital currencies in which transactions are
            verified and records maintained by a decentralized system using
            cryptography, rather than by a centralized authority.
            The first cryptocurrnecy was created in 2008 by an individual who went
            by the pseudo name 'Satoshi Nakamoto'. They released Bitcoin, as a way
            to securely make decentralized transactions. Since then, there's been
            hundreds of new cryptocurrencies released such as Ethereum (ETH), Cardano (ADA)
            and Litecoin (LTE).
          </h3>
        </div>
      </div>
      <div class='mainContent'>
        <div id='tutorial'>
          <h2> How to use the SimEx trading platform </h2>
          <p> Below is a step by step guide to get started with the SimEx Platform </p>
          <div class='line' />
          <hooper :settings="hooperSettings" style="height: 100%">
            <slide>
              <div class='step'>
          <h2> Step One: Sign Up! </h2>
          <img
          src="@/assets/register.jpg"
          class='tutImage'
          alt='View of the registration page'
          />
          <div class='line' />
          <p>You first need to create an account, for free by setting up a username
            and password, you'll be given $10,000 dollars to spend on cryptocurrencies
            of your choosing. Afterwards navigate to the login page and login.</p>
          </div>
            </slide>
            <slide>
              <div class='step'>
          <h2> Step Two: Find a cryptocurrency! </h2>
          <img
          src="@/assets/step2.jpg"
          class='tutImage'
          alt='View of home page, with arrows pointed towards the trade button'
          />
          <div class='line' />
          <p>Navigate to the homepage, and browse through the table of available cryptocurrencies.
            Pick one you want to investigate further, and press the 'trade' link to be taken to the
            trade page.
          </p>
          </div>
            </slide>
            <slide>
              <div class='step'>
                <h2> Step Three: Buy/Sell! </h2>
                <img
                  src="@/assets/step3.jpg"
                  class='tutImage'
                  alt='View of the trade page, with arrows pointed to the Buy and Sell panel,
                  with notes that describe how to trade'
                 />
                 <div class='line' />
                <p>Look at the graph, and then if you decide you want to buy/sell, enter the amount
                  you want to buy/sell
                  and then press buy/sell, making sure to press the confirm. Afterwards,
                  your balance is
                  updated and a log of the trade is recorded (This can be checked in portfolio).
                </p>
              </div>
            </slide>
            <slide>
              <div class='step'>
                <h2> Step Four: Check your portfolio! </h2>
                <img
                  src="@/assets/step4.jpg"
                  class='tutImage'
                  alt='View of the portfolio page'
                />
                <div class='line' />
                <p>You can checkout your portfolio page when you're logged in.
                This will give you a breakdown of all the different assets you own,
                as well as their worth, the distribution and a log of all the different
                trades that have been done.
                </p>
              </div>
            </slide>
            <hooper-navigation slot="hooper-addons"></hooper-navigation>
          </hooper>
        </div>
      </div>
    </div>
</template>

<script>
// Importing the Hooper component to use as a slide show for the tutorial
import { Hooper, Slide, Navigation as HooperNavigation } from 'hooper';
import 'hooper/dist/hooper.css';

export default {
  name: 'Learn',
  components: {
    Hooper,
    Slide,
    HooperNavigation,
  },
  data() {
    return {
      // Hooper Settings Configuration
      hooperSettings: {
        itemsToShow: 1,
        centerMode: true,
      },
    };
  },
};
</script>

<style scoped>
.topHeading{
  text-align: center;
  width: 75%;
  margin: auto;
}
#tutorial h2{
  padding: 1%;
  font-weight: bold;
}
#tutorial {
  border-bottom: solid;
}
.mainContent{
  width: 80%;
  margin: auto;
  border-left: solid;
  border-right: solid;
  min-height: 100%;
}
.step{
  text-align: center;
  width: 100%;
  margin:auto;
}
.step p{
  padding: 1%;
}
.topHeading h1{
  background-color: rgb(20, 20, 20);
  padding: 1%;
}
.jumbotron{
  width: 100%;
  background-color: rgb(0, 0, 0);
  color: white;
  padding: 1%;
}
.tutImage{
  width: 75%;
  display: block;
  margin:auto;
  padding: 1%;
}
.header-image{
  height: 300px;
  width:50%;
}
.line{
  min-width: 100%;
  border-bottom: solid;
}
p {
   font-size: large;
   width: 50%;
   margin:auto;
}
</style>
