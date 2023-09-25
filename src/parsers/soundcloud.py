
# Create an instance of the SoundCloudDownloader class
# sc_downloader = SoundCloudDownloader()

# # url = input("URL: ")
# # sc_downloader.get_track(url)

# # url = "https://soundcloud.com/username/trackname"
# # sc_downloader.get_track(url)

# url_list = [
#     "https://soundcloud.com/liltecca/fellinlove",
# ]


# sc_downloader.get_track(url_list)
import requests, re, os, threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
import schedule
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SoundCloudDownloader:
    # Setting the request headers and getting the client_id
    def __init__(self):
        self.headers = {
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'api-v2.soundcloud.com',
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
        }
        self.client_id = self.get_client_id()

    # Getting the client_id
    def get_client_id(self):
        url = "https://soundcloud.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script")[-1]['src']
        script = requests.get(scripts).text
        client_id = script.split(",client_id:")[1].split('"')[1]
        return client_id

    # Getting the track name
    def get_track_name(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("title").text
        track_name = re.search(r"Stream\s(.+)\sby", title).group(1)
        return track_name

    # Getting the track ID
    def get_track_id(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        track_id = soup.find("meta", property="twitter:app:url:googleplay")["content"].split(":")[-1]
        return track_id

    # Get the chunks of the track from SoundCloud API
    def get_track_chunks(self, track_id):
        url = f"https://api-v2.soundcloud.com/tracks?ids={track_id}&client_id={self.client_id}"
        res = requests.get(url, headers=self.headers).json()

        # Extract the stream URL from the response
        stream_url = res[0]["media"]["transcodings"][0]["url"]
        stream_url += "?client_id=" + self.client_id

        # Get m3u8 URL from the stream URL
        m3u8_url = requests.get(stream_url, headers=self.headers).json()["url"]
        
        # Get the content of the m3u8 file
        m3u8_file = requests.get(m3u8_url).text

        # Split the m3u8 file into chunks and filter out comments
        m3u8_file_split = m3u8_file.splitlines()
        chunks = []
        for chunk in m3u8_file_split:
            if "#" not in chunk:
                chunks.append(chunk)
        return chunks

    def download_track(self, file_name, chunks, type):
        file_name = file_name.strip()
        
        # Check if the file already exists
        if os.path.isfile(file_name + ".mp3"):
            i = 1
            while os.path.isfile(file_name + f" ({i:02d})" + ".mp3"):
                i += 1
            file_name += f" ({i:02d})"

        file_name += ".mp3"

        if type == "dnb":
            file = open("./music/dnb/" + file_name, "ab")
        if type == "techno":
            file = open("./music/techno/" + file_name, "ab")
        if type == "phonk":
            file = open("./music/phonk/" + file_name, "ab")
        # Download each chunk and write its content to the file
        for chunk in chunks:
            content = requests.get(str(chunk), headers={}).content
            file.write(content)
        file.close()


    def get_track(self, url_list, type):
        # Check if the input is a string or a list
        if isinstance(url_list, str):
            url_list = [url_list]
        elif not isinstance(url_list, list):
            raise ValueError("Invalid input type. Expected str or list.")
                   
        def download_track_wrapper(url, type):
            # Call helper functions
            try:
                track_name = self.get_track_name(url)
                track_id = self.get_track_id(url)
                chunks = self.get_track_chunks(track_id)
                print(f"Downloading... \nName: {track_name}\nId: {track_id}")       
                self.download_track(track_name, chunks, type=type)
                print(f"{track_name} downloaded successfully!")
            except ValueError:
                print(f"Error downloading {url}. Invalid URL entered. Try again.")

        # Download tracks concurrently using threading
        threads = []
        for url in url_list:
            t = threading.Thread(target=download_track_wrapper, args=(url, type))
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete before returning
        for t in threads:
            t.join()


    def scan_search(self, uri, type):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # Initialize the webdriver with ChromeOptions
        driver = webdriver.Remote(
    command_executor="http://selenium-chrome:4444/wd/hub",
    options=chrome_options
)

        # Navigate to a website
        driver.implicitly_wait(30000)
        driver.get(uri)

        # Perform actions (e.g., fill out forms, click buttons)

        # Wait for some time (useful for dynamic content)
        
        time.sleep(7)

        actions = ActionChains(driver)
        for _ in range(30):  # Scroll down 3 times, you can adjust as needed
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.7)  # Wait for a moment between scrolls
        # Get page content or perform other operations
        page_source = driver.page_source
        print(page_source)

        # Close the WebDriver when done
        driver.quit()


# Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all 'a' elements with the specified class
        elements = soup.find_all('a', class_='sc-link-primary soundTitle__title sc-link-dark sc-text-h4')

        # Extract the 'href' attributes from the 'a' elements
        href_list = [element['href'] for element in elements]

        # Print the extracted 'href' links
        links = []
        for href in href_list:
            links.append("https://soundcloud.com" + href)

        print(links)

        self.get_track(links, type)
        


# dwn = SoundCloudDownloader()

# dwn.scan_search("https://soundcloud.com/search/sounds?q=dnb&filter.created_at=last_week")
# #dwn.get_client_id()

def update():
    print("Start updating")
    dwn = SoundCloudDownloader()


    # Update dnb
    dwn.scan_search("https://soundcloud.com/search/sounds?q=dnb&filter.created_at=last_month", "dnb")


    dwn.scan_search("https://soundcloud.com/search/sounds?q=techno&filter.created_at=last_month", "techno")

    dwn.scan_search("https://soundcloud.com/search/sounds?q=atmosphere%20phonk&filter.created_at=last_month", "phonk")
#dwn.get_client_id()


if __name__ == "__main__":
    update()
    schedule.every(2).weeks.do(update)

    while True:
        # Run pending scheduled jobs
        schedule.run_pending()

        # Sleep for a while (e.g., 1 minute) to avoid busy-waiting
        time.sleep(60)