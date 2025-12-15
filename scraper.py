from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from basics.start_driver import start_driver
import requests
import os
import time
import json
from urllib.parse import urlparse, unquote
from PIL import Image
import io


class NillaveeCakesScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome"""
        self.driver = start_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = 'https://nillavee.co.ke/all-cakes/'
        self.cakes_data = []

    def scroll_to_load_all(self):
        """Scroll down to load all cakes (infinite scroll)"""
        print("Scrolling to load all cakes...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 20  # Safety limit

        while scroll_attempts < max_scrolls:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load

            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # Check if we've reached the bottom
            if new_height == last_height:
                print("Reached bottom of page")
                break

            last_height = new_height
            scroll_attempts += 1
            print(f"Scroll {scroll_attempts}: Height {new_height}")

        print(f"Finished scrolling after {scroll_attempts} attempts")

    def get_requests_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Referer": self.base_url,
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"
        })

        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])

        return session

    def extract_cake_info(self, cake_element):
        try:
            img = cake_element.find_element(By.TAG_NAME, 'img')

            img_src = None

            if not img_src:
                for attr in ["data-src", "data-lazy-src", "src"]:
                    val = img.get_attribute(attr)
                    if val and not val.startswith("data:"):
                        img_src = val
                        break

            if not img_src:
                return None

            # Normalize URL
            if img_src.startswith("//"):
                img_src = "https:" + img_src
            elif img_src.startswith("/"):
                img_src = "https://nillavee.co.ke" + img_src

            alt_text = img.get_attribute("alt") or "cake"

            return {
                "image_url": img_src,
                "alt_text": alt_text,
                "cake_name": alt_text,
                "downloaded": False,
                "filename": None
            }

        except Exception as e:
            print(f"Extract error: {e}")
            return None

    def download_image(self, image_url, folder='cake_images', alt_text='cake', index=0):
        if image_url is None:
            return None
        try:
            os.makedirs(folder, exist_ok=True)

            safe = ''.join(c for c in alt_text[:40] if c.isalnum() or c in " -_").strip()
            safe = safe.replace(" ", "_") or f"cake_{index}"

            parsed = urlparse(image_url)
            ext = os.path.splitext(parsed.path)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
                ext = ".jpg"

            filename = f"{safe}_{index}{ext}"
            path = os.path.join(folder, filename)

            session = self.get_requests_session()

            # Retry logic
            for attempt in range(3):
                resp = session.get(image_url, timeout=30)
                if resp.ok:
                    break
                time.sleep(1)
            else:
                raise ValueError("Failed after retries")

            # MIME validation
            ctype = resp.headers.get("Content-Type", "")
            if not ctype.startswith("image/"):
                raise ValueError(f"Blocked (Content-Type={ctype})")

            # Size validation (filters placeholders)
            if len(resp.content) < 2048:
                raise ValueError("Placeholder / tiny image")

            # HTML guard
            if resp.content[:4].lower().startswith(b"<ht"):
                raise ValueError("HTML page saved as image")

            # Convert WebP → JPG
            if "webp" in ctype or ext == ".webp":
                img = Image.open(io.BytesIO(resp.content)).convert("RGB")
                path = path.replace(".webp", ".jpg")
                img.save(path, "JPEG", quality=92)
            else:
                with open(path, "wb") as f:
                    f.write(resp.content)

            print(f"  ✓ Saved: {os.path.basename(path)} ({len(resp.content)} bytes)")
            return path

        except Exception as e:
            print(f"  ✗ Skipped invalid image: {e}")
            return None

    def scrape_cakes(self):
        """Main scraping function"""
        print(f"Navigating to {self.base_url}")
        self.driver.get(self.base_url)

        # Wait for page to load
        time.sleep(3)

        # Scroll to load all cakes
        self.scroll_to_load_all()

        # Find all cake elements - try multiple selectors
        print("Looking for cake elements...")

        # Try to find product cards/containers
        selectors = [
            'div[class*="product"]',
            'div[class*="card"]',
            'article',
            'div.grid > div',
            'div.flex > div',
            'div[class*="item"]',
            'div[class*="cake"]'
        ]

        cake_elements = []
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 3:  # Found reasonable number of elements
                    print(f"Found {len(elements)} elements with selector: {selector}")
                    cake_elements = elements
                    break
            except:
                continue

        # Fallback: find all divs containing images
        if not cake_elements:
            print("Using fallback: looking for all image containers")
            all_images = self.driver.find_elements(By.TAG_NAME, 'img')
            # Get parent elements of images that might be cake containers
            for img in all_images:
                try:
                    parent = img.find_element(By.XPATH, '..')
                    if parent not in cake_elements:
                        cake_elements.append(parent)
                except:
                    continue

        print(f"Found {len(cake_elements)} potential cake containers")

        # Extract information from each cake
        for i, cake_element in enumerate(cake_elements):
            print(f"\nProcessing cake {i + 1}/{len(cake_elements)}")

            cake_info = self.extract_cake_info(cake_element)

            if cake_info and cake_info.get('image_url'):
                self.cakes_data.append(cake_info)
                print(f"✓ Extracted: {cake_info.get('title', 'Unknown')[:60]}...")
                print(f"  Image URL: {cake_info['image_url'][:80]}...")
            else:
                print(f"✗ Could not extract cake {i + 1}")

        return self.cakes_data

    def download_all_images(self, folder='cake_images'):
        """Download all cake images"""
        if not self.cakes_data:
            print("No cakes data available to download")
            return 0

        downloaded_count = 0

        print(f"\n{'=' * 60}")
        print(f"DOWNLOADING IMAGES")
        print(f"{'=' * 60}")

        self.cakes_data = list({
           cake["image_url"]: cake
           for cake in self.cakes_data
              if cake.get("image_url")
        }.values())

        for i, cake in enumerate(self.cakes_data):
            image_url = cake.get('image_url')
            alt_text = cake.get('alt_text', f'cake_{i + 1}')

            if image_url:
                print(f"\n[{i + 1}/{len(self.cakes_data)}] {alt_text[:50]}...")

                filepath = self.download_image(image_url, folder, alt_text, i + 1)

                if filepath:
                    cake['downloaded'] = True
                    cake['local_path'] = filepath
                    cake['filename'] = os.path.basename(filepath)
                    downloaded_count += 1
                else:
                    cake['downloaded'] = False

        print(f"\n{'=' * 60}")
        print(f"DOWNLOAD SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total cakes: {len(self.cakes_data)}")
        print(f"Successfully downloaded: {downloaded_count}")
        print(f"Failed: {len(self.cakes_data) - downloaded_count}")

        return downloaded_count

    def save_data(self, filename='cakes.json'):
        """dump scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.cakes_data, f, indent=2, ensure_ascii=False)
        print(f"\nData saved to {filename}")

    def display_summary(self):
        """Display summary of scraped data"""
        print(f"\n{'=' * 60}")
        print(f"SCRAPING SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total cakes found: {len(self.cakes_data)}")

        downloaded = sum(1 for cake in self.cakes_data if cake.get('downloaded', False))
        print(f"Images downloaded: {downloaded}")

        if self.cakes_data:
            print(f"\nSample of first 3 cakes:")
            for i, cake in enumerate(self.cakes_data[:3]):
                print(f"\n{i + 1}. {cake.get('title', 'No title')[:60]}...")
                print(f"   Image: {cake.get('image_url', 'No URL')[:80]}...")
                if cake.get('downloaded'):
                    print(f"   Saved as: {cake.get('filename', 'Unknown')}")
                if cake.get('price'):
                    print(f"   Price: {cake['price']}")

    def close(self):
        """Close the browser"""
        self.driver.quit()


def main():
    scraper = NillaveeCakesScraper(headless=True)

    try:
        # Scrape the data
        print("Starting scraping...")
        cakes_data = scraper.scrape_cakes()

        if cakes_data:

            # Download all images
            print("\nStarting image downloads...")
            scraper.download_all_images('images')

            # Save data to JSON
            scraper.save_data('cakes.json')
            
            # Display summary
            scraper.display_summary()

            # Print location of files
            print(f"\nFiles saved in:")
            print(f"- Images: images/ folder")
            print(f"- Data: cakes.json")
        else:
            print("No cakes data was scraped")

    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Close the browser
        scraper.close()


if __name__ == "__main__":
    # Install required packages if not already installed
    # pip install selenium requests

    main()