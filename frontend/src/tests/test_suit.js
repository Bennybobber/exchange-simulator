const webdriver = require("selenium-webdriver");
var assert = require("assert");

const driver = new webdriver.Builder()
    .forBrowser("firefox")
    .build();

describe("SimEx Test Suit", function() {
    
    before(function(done){
        
        // do something before test suite execution
        // no matter if there are failed cases
        driver
            .get("http://localhost:8080/");
        driver.manage().setTimeouts( { implicit: 5000 } ).then(function(){done()});
    
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

    it("Test-1 Correct Home Title", function(done) {
        driver.getTitle()
            .then(function(title) {
                assert( title.match('SimEx Home'))
                done();
            })
            .catch(err => done(err));
    });

    it("Test-2 Check Table Headings Exist", function(done) {
        driver
            .findElement(webdriver.By.xpath("//*[contains(text(),'Rank')]"))
            .getText()
            .then(function(text) {
                assert(
                    text.match('Rank #')
                )
                driver
                    .findElement(webdriver.By.xpath("//*[contains(text(),'Currency Name')]"))
                    .getText()
                    .then(function(text) {
                        assert(
                            text.match('Currency Name')
                        )
                     done();
                    })
                    .catch(err => done(err));
            })
            .catch(err => done(err));
        
    })

    it("Test-3 Navigate to register", function(done) {
        driver
            .findElement(webdriver.By.id("login"))
            .click()
            .then(function() {
                driver
                    .findElement(webdriver.By.id("register"))
                    .click()
                    .then(function() {
                        driver
                            .getTitle()
                            .then(function(title) {
                                assert( title.match('Register'))
                                done();
                            })
                            .catch(err => done(err));
                            })
                    .catch(err => done(err));

                })
            .catch(err => done(err));
        
    })

    it("Test-4 Fill register an account", function(done) {
        driver
            .findElement(webdriver.By.name("username"))
            .sendKeys("test_username")
            .catch(err => done(err));
        driver
            .findElement(webdriver.By.name("password"))
            .sendKeys("test_password")
            .catch(err => done(err))
        driver
            .findElement(webdriver.By.xpath("//*[contains(text(),'Sign Up')]"))
            .click()
            .then(function() {
                driver
                    .findElement(webdriver.By.xpath("//*[contains(text(),'successfully registered user')]"))
                    .getText()
                    .then(function(text) {
                        assert (
                            text.match ("successfully registered user")
                        )
                        done()
                    })
                    .catch (err => done(err))
                })
            .catch (err => done(err))
    })

    it("Test-5 Login to the new account", function(done) {
        driver
            .findElement(webdriver.By.id("login"))
            .click()
            .then( function() {
                driver
                    .findElement(webdriver.By.name("username"))
                    .sendKeys("test_username")
                    .catch(err => done(err));
                driver
                    .findElement(webdriver.By.name("password"))
                    .sendKeys("test_password")
                    .catch(err => done(err))
                driver
                    .findElement(webdriver.By.id("submit__login"))
                    .click()
                    .then(function() {
                            done();
                        })
            .catch (err => done(err))
            }
                
            )
            .catch(err => done(err));
        
    })

    it("Test-6 Navigate to the portfolio page and delete account", function(done) {
        driver
            .findElement(webdriver.By.id("portfolio"))
            .click()
            .then(function() {
                driver
                    .findElement(webdriver.By.id("delete__button"))
                    .click()
                    .then(function() {
                        driver.switchTo().alert().accept();
                        done();
                    })
               
            })
            .catch(err => done(err))
    })
})