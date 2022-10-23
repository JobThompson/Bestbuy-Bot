import helium as h
import time
from Logging import write_to_log
from Config import instanceConfig
from Credentials import credentials

def buy_product(product_url):
    """This function is the bot that opens a firefox browser, signs into the BestBuy site, then calls the product URL.
    If the product is in stock, it purchases the product. If the product is not in stock, it refreshes the page until
    it is."""
    h.start_firefox('https://www.bestbuy.com/identity/global/signin', headless=instanceConfig.isHeadlessFlag) # Starts firefox instance, headless = True wont come up as a intractable window
    h.write(credentials.email, into='Email Address') # Enters Email address into email input box from Info file
    h.write(credentials.password, into='Password') # Enters password into password input box from Info file
    h.click(h.S('.btn-secondary')) # Clicks log in
    h.go_to(product_url) # Directs the browser to pull up the specified product page.
    attempts = 0 # Sets retrieval attempts to 0, not really necessary
    h.Config.implicit_wait_secs = 2 # Sets the amount of time the script will wait for an element to load to 2 seconds
    
    while True:
        while True:
            h.Config.implicit_wait_secs = instanceConfig.script_timeout
            try:
                h.click(h.Button('Add To Cart')) # Attempts to click add to cart button
                write_to_log('Button: Add to Cart.', 'INFO')
                break
            except:
                attempts += 1 # Add 1 to the attempt number
                print('failed:', attempts) # Prints the failed attempt number
                write_to_log(f'Button: Out Of Stock. Attempt Number {attempts} Failed.')
                h.refresh() # Refreshes the product webpage
                
        h.Config.implicit_wait_secs = 7
        
        if h.Text('not in Cart.').exists(): # Checks for BestBuy anti bot message
            write_to_log('Item was not added to cart')
            h.refresh()
            
        elif h.Text('Error').exists(): # Checks for error messages on webpage
            write_to_log('Webpage returned an error.')
            h.click(h.Button('Add To Cart'))
        
        elif h.Text('Added to Cart').exists(): # Verifies that the product was added to cart
            write_to_log('Item successfully added to cart.')
            break
        
    h.Config.implicit_wait_secs = 100 # Sets the amount of time the script will wait for an element to load to 5 seconds
    h.go_to('https://www.bestbuy.com/cart') # Sends browser to card
    h.click(h.Button('Checkout')) # Clicks on checkout button
    h.go_to('https://www.bestbuy.com/checkout/r/fast-track') # Sends browser to checkout page
    
    try:
        h.write(credentials.card_cvv, into=h.S('#credit-card-cvv')) # Attempts to find CVV input, if doesn't show up within 5 seconds, passes on to next command
    except Exception:
        pass
    
    h.click(h.Button('Place Your Order')) # Clicks the place order button
    time.sleep(30)
    h.kill_browser() # Closes the browser instance
    return attempts