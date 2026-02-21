from basics.start_driver import start_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def unsubscribe_from_account(driver, account_index=0):
    """Unsubscribe from emails in a specific Gmail account."""
    try:
        # Navigate to the specific account
        driver.get(f'https://mail.google.com/mail/u/{account_index}/')

        # Wait for Gmail to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]'))
        )

        print(f"\n=== Processing account u/{account_index} ===")

        # Search for emails with unsubscribe links
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.clear()
        search_box.send_keys('unsubscribe OR "manage preferences" OR "email preferences"')
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)

        # Process emails
        unsubscribe_count = 0
        max_emails = 20  # Limit to prevent infinite loops

        for i in range(max_emails):
            try:
                # Find email rows
                emails = driver.find_elements(By.CSS_SELECTOR, 'tr.zA, div[role="main"] table tr')

                if not emails or i >= len(emails):
                    print(f"No more emails to process (processed {unsubscribe_count})")
                    break

                # Click on the email
                emails[i].click()

                # Wait for email to load
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]'))
                )
                time.sleep(2)

                # Look for unsubscribe link (multiple possible text variations)
                unsubscribe_found = False
                for link_text in ['Unsubscribe', 'unsubscribe', 'UNSUBSCRIBE', 'Opt out']:
                    try:
                        unsubscribe_link = driver.find_element(By.PARTIAL_LINK_TEXT, link_text)
                        unsubscribe_link.click()
                        print(f"  ✓ Unsubscribed from email {i + 1}")
                        unsubscribe_count += 1
                        unsubscribe_found = True
                        time.sleep(2)

                        # Handle confirmation if needed
                        try:
                            confirm_btn = driver.find_element(By.XPATH,
                                                              "//button[contains(text(), 'Confirm') or contains(text(), 'Unsubscribe')]")
                            confirm_btn.click()
                            time.sleep(1)
                        except:
                            pass

                        break
                    except NoSuchElementException:
                        continue

                if not unsubscribe_found:
                    print(f"  ✗ No unsubscribe link in email {i + 1}")

                # Go back to search results
                driver.back()
                time.sleep(2)

            except Exception as e:
                print(f"  ✗ Error processing email {i + 1}: {str(e)}")
                try:
                    driver.back()
                    time.sleep(2)
                except:
                    break

        print(f"Total unsubscribed in u/{account_index}: {unsubscribe_count}")
        return True

    except Exception as e:
        print(f"Error accessing account u/{account_index}: {str(e)}")
        return False


def detect_gmail_accounts(driver):
    """Detect how many Gmail accounts are available."""
    accounts = []

    for i in range(10):  # Check up to 10 accounts
        try:
            driver.get(f'https://mail.google.com/mail/u/{i}/')
            time.sleep(2)

            # Check if we're redirected or if the page loads properly
            current_url = driver.current_url

            if f'/u/{i}/' in current_url or (i == 0 and 'mail.google.com' in current_url):
                # Check if we're actually logged in (not on login page)
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]'))
                    )
                    accounts.append(i)
                    print(f"Found account: u/{i}")
                except TimeoutException:
                    break
            else:
                break

        except Exception as e:
            break

    return accounts


def main():
    """Main function to unsubscribe from all detected Gmail accounts."""
    driver = start_driver()

    try:
        print("Starting Gmail unsubscribe automation...")
        print("Please make sure you're already logged into Gmail in your browser.\n")

        # Open Gmail first
        driver.get('https://mail.google.com/')
        time.sleep(3)

        # Check if user is logged in
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]'))
            )
            print("✓ Successfully accessed Gmail\n")
        except TimeoutException:
            print("✗ Not logged in to Gmail. Please log in manually first.")
            input("Press Enter after logging in...")

        # Detect all available accounts
        print("Detecting Gmail accounts...")
        accounts = detect_gmail_accounts(driver)

        if not accounts:
            print("No Gmail accounts detected. Please ensure you're logged in.")
            return

        print(f"\nFound {len(accounts)} account(s): {accounts}\n")

        # Process each account
        for account_index in accounts:
            unsubscribe_from_account(driver, account_index)
            time.sleep(2)

        print("\n=== All accounts processed! ===")

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    finally:
        input("\nPress Enter to close the browser...")
        driver.quit()


if __name__ == "__main__":
    main()