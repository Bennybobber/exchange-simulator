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
        <div class = "tips">
          <h1> Trading 'Tips 'N Tricks' </h1>
          <h3>Here are 5 things to consider when trading!</h3>
          <ol>
            <li><b>Doing your own research (DYOR)</b> decreases chances of
              making a loss, investigate about an asset before you buy.
              Simply hearing about an asset isn't enough,
              you want to look at price trends as well as the people behind
              the asset, what their plans are. Looking at their white paper
              (The document that outlines the mission for their asset) will
              give good insight into the future of an asset.
            </li>
            <li>Create a <b>diverse portfolio</b>. The more your funds are spread
              across multiple assets, the likelihood of big losses decreases
              because you're not putting all of your money into one asset.
              If that asset crashes, you've lost everything. Whereas if you
              put it into 5 different assets, you still have 4 other assets
              that could be doing well.
            </li>
            <li>Don't buy in because you feel you might miss out.
              <b>"FOMO" (Fear of missing out)</b> can be tempting when you see an
              asset rapidly growing all of a sudden, but it's important to
              think about corrections. Corrections occur when an asset rises
              in price rapdidly, and then current investors tend to take profits.
              This leads into a drop in the price, and could lead to a loss if
              you bought in near the top of the price.
            </li>
            <li>Be weary of others, very often people will <b>"shill"</b> and tell you buy
              certain assets. This is likely down to them owning the asset themselves
              and are trying to get others to buy too. They're more likely to gloss over
              or not even mention any possible risks with an asset and focus on only the
              good points. This falls back to <b>DYOR</b>, but most importantly is to not use
              blind trust, as it can lead to risk and losses.
            </li>
            <li><b>Beware of scammers</b>, there are many in the cryptocurrency world. They're going
              to try and gain access to both your exchange accounts, and your cryptocurrency
              keys. Many of them act as customer service helpers, and will try to gain access
              to your account via a scam technique known as "phishing". Phishing is where
              scammers will act as a valid authority and get you to try and give up your personal
              information. An example is recieving an email that looks like it's from an exchange
              but it's actually a fake account.
            </li>
          </ol>
        </div>
        <div class='jargon'>
          <h1>Cryptocurrency Jargon</h1>
          <p> A helpful list of phrases and words used in cryptocurrency </p>
          <ul>
            <li>
              <b>FOMO</b><br> Means Fear of Missing Out and is described when people buy into an
              asset simply because it's popular, and want to jump on the upwards trend. This can be
              risky as people like to take profits and can cause to a loss of money if bought at the
              top of the trend.
            </li>
            <li>
              <b>White Paper</b><br> A white paper is a document issued by an asset provider that
              provides information about their asset and the plans for the future. It's always
              advised to read this before any purchase.
            </li>
            <li>
              <b>DYOR</b><br> Means Do your Own Research and is used to tell people to research an
              asset before they go ahead and buy into it. Many new investors make the mistake of
              going by what others say, rather than going out and doing their own research into
              an asset such as viewing the white paper of an asset.
            </li>
            <li>
              <b>Altcoin</b><br> This is simply any asset that isn't bitcoin and the direct
              definition is "alternative coin".
            </li>
            <li>
              <b>Shorting</b><br> Much like stocks, on some exchanges you can "short" an asset. This
              is betting that the value of an asset will decrease. This is very risky,
              and if it does
              not happen, your position in the asset will be liquidated and you can lose all
              your money.
            </li>
            <li>
              <b>Shill</b><br>Shilling is the practice of trying to get others to buy
              into an asset you own. When doing research it's very common for people to
              try and sell an asset on you by only talking about the positives, and not
              mentioning anything that might be of concern before buying.
            </li>
            <li>
              <b>Fiat</b><br>These are currencies that are backed by a sovereign government.
              Examples include, American Dollars, British Pound Sterling, Euros etc...
            </li>
            <li>
              <b>Bull Market</b><br>This is where there is confidence in the market and prices
              trend upwards, sometimes even aggressively with big price changes trending upwards
              over short amount of time. Lots of profits to be made in a bull market.
            </li>
            <li>
              <b>Bear Market</b><br>Most traders dread a bear market, in which prices trend
              downwards, and often quite aggressively. There is usually panic, and distrust in
              the market and people pull their money out. These markets can last years, and the
              price of an asset can plummet upwards of 90% or completely disappear from the market.
            </li>
          </ul>
          </div>
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
import {
  Hooper,
  Slide,
  Navigation as HooperNavigation,
} from 'hooper';
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
.jargon{
  border-top: solid;
}
.jargon ul{
  text-align: left;
  width: 50%;
  margin: auto;
}
.jargon li{
  padding-bottom: 1%;
}
.tips ol {
  margin: 0 0 1.5em;
  padding: 0;
  counter-reset: item;
}
.tips h3, h1{
  padding: 0.3%;
  padding-bottom: 0;
}
.tips ol > li {
  margin: 0;
  padding: 2%;
  text-indent: -2em;
  list-style-type: none;
  counter-increment: item;
}

.tips ol > li:before {
  display: inline-block;
  width: 1em;
  padding-right: 0.5em;
  font-weight: bold;
  text-align: right;
  content: counter(item) ".";
}
.tips ol{
  width: 50%;
  margin: auto;
  padding: 2%;
}
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
  border-top: solid;
  margin-top: 2%;
}
.mainContent{
  font-family: "Times New Roman", Times, serif;
  font-size: large;
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
  background-color: rgb(226, 109, 0);
  padding: 1%;
  border-radius: 25px;
}
.jumbotron{
  width: 80%;
  margin: auto;
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
@media only screen and (max-width: 600px) {
.mainContent{
  width: 100%;
}
.tutImage{
  width: 100%;
}
ul{
  width: 100%;
}
.tips ol{
  width: 90%;
  margin:auto;
  text-align: left;
}
.jargon ul{
  width: 100%;
}
.jumbotron{
  width: 100%;
}
.topHeading{
  width: 90%;
  font-size: 1%;
}
}
</style>
