const webdriver = require("selenium-webdriver");
var assert = require("assert");

const driver = new webdriver.Builder()
    .forBrowser("firefox")
    .build();

describe("SimEx Test Suit USER REGISTER/LOGIN/RESET/DELETE accounts", function() {
    
    before(async function(){
        
        // do something before test suite execution
        // no matter if there are failed cases
        await driver
            .get("http://localhost:8080/");
        await driver
            .manage()
            .setTimeouts( { implicit: 5000 } );
    
    });

    after(function(){
        // quit the driver after all tests are complete
        return driver.quit();
    });

    beforeEach(function(){
        
        // do something before test case execution
        // no matter if there are failed cases
    
    });
 
    afterEach(function(){
 
        // do something after test case execution is finished
        // no matter if there are failed cases
 
    });

    it("Test-1 Correct Home Title", async function() {
        const title = await driver.getTitle();
        assert( title.match('SimEx Home'));
    });

    it("Test-2 Check Table Headings Exist", async function() {
        const rankHeaderCheck = await driver
            .findElement(webdriver.By.xpath("//*[contains(text(),'Rank')]"))
            .getText()
        assert(
            rankHeaderCheck.match('Rank #')
        )
        const currencyHeaderCheck = await driver
                .findElement(webdriver.By.xpath("//*[contains(text(),'Currency Name')]"))
                .getText()
        assert(
            currencyHeaderCheck.match('Currency Name')
        )
        
    })

    it("Test-3 Navigate to register", async function() {
        await driver
            .findElement(webdriver.By.id("login"))
            .click()
        await driver
            .findElement(webdriver.By.id("register"))
            .click()
        const title = await driver
            .getTitle()
        assert( title.match('Register'))
    })

    it("Test-4 Fill register an account", async function() {
        await driver
            .findElement(webdriver.By.name("username"))
            .sendKeys("test_username")
        await driver
            .findElement(webdriver.By.name("password"))
            .sendKeys("test_password")
        await driver
            .findElement(webdriver.By.xpath("//*[contains(text(),'Sign Up')]"))
            .click()
        const successMessage = await driver
            .findElement(webdriver.By.xpath("//*[contains(text(),'successfully registered user')]"))
            .getText()
        assert (
            successMessage.match ("successfully registered user")
        )
    })

    it("Test-5 Login to the new account", async function() {
        await driver
            .findElement(webdriver.By.id("login"))
            .click()
        await driver
            .findElement(webdriver.By.name("username"))
            .sendKeys("test_username")
        await driver
            .findElement(webdriver.By.name("password"))
            .sendKeys("test_password")
        await driver
            .findElement(webdriver.By.id("submit__login"))
            .click()
        
    })
    it("Test-6 Navigate to the portfolio page and reset account", async function() {
        await driver
            .findElement(webdriver.By.id("portfolio"))
            .click()
        await driver
            .findElement(webdriver.By.id("reset__button"))
            .click()
        await driver
            .switchTo()
            .alert()
            .accept()
        balance = await driver
            .findElement(webdriver.By.className("balance"))
            .getText()
        assert (balance === "USD Balance: $100000.00")
    })

    it("Test-7 Delete account", async function() {
        await driver
            .findElement(webdriver.By.id("delete__button"))
            .click()
        await driver
            .switchTo()
            .alert()
            .accept()
    })

    it("Text-8 Try to login deleted account, and check it fails", async function() {
        await driver
            .findElement(webdriver.By.id("login"))
            .click()
        await driver
            .findElement(webdriver.By.name("username"))
            .sendKeys("test_username")
        await driver
            .findElement(webdriver.By.name("password"))
            .sendKeys("test_password")
        await driver
            .findElement(webdriver.By.id("submit__login"))
            .click()
        const errorMessage = await driver
            .findElement(webdriver.By.xpath("//*[contains(text(),'could not verify')]"))
            .getText()
        assert (
            errorMessage.match ("could not verify")
        )
    })
})