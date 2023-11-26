import requests
from bs4 import BeautifulSoup
import json
import time
import csv

cookies = {
    "zguid": "24^|^%^2437ddf7ac-45b0-413d-91b2-c45bd99d51c4",
    "zjs_anonymous_id": "^%^2237ddf7ac-45b0-413d-91b2-c45bd99d51c4^%^22",
    "zjs_user_id": "null",
    "zg_anonymous_id": "^%^22bda50833-2164-4a5c-b99b-7a4811bda1ca^%^22",
    "AWSALB": "lwbOTHTCGpBqGWeKhphQHDh6c2VX2dzJNCQ3YJ+Fcljoe/ux5MmKvFLGiPzy6XQr/I5o0T9i6kIIPIJXA4Rm7y6dSdivQF9s/v+dAuBrFsmQzdS15jYQizlppYyV",
    "AWSALBCORS": "lwbOTHTCGpBqGWeKhphQHDh6c2VX2dzJNCQ3YJ+Fcljoe/ux5MmKvFLGiPzy6XQr/I5o0T9i6kIIPIJXA4Rm7y6dSdivQF9s/v+dAuBrFsmQzdS15jYQizlppYyV",
    "search": "6^|1703610420512^%^7Crect^%^3D40.8356640592369^%^2C-73.4399776308594^%^2C40.55975337598839^%^2C-74.51938436914065^%^26rid^%^3D6181^%^26disp^%^3Dmap^%^26mdm^%^3Dauto^%^26p^%^3D1^%^26z^%^3D0^%^26listPriceActive^%^3D1^%^26lt^%^3Dfsbo^%^26fs^%^3D1^%^26fr^%^3D0^%^26mmm^%^3D0^%^26rs^%^3D0^%^26ah^%^3D0^%^26singlestory^%^3D0^%^26housing-connector^%^3D0^%^26abo^%^3D0^%^26garage^%^3D0^%^26pool^%^3D0^%^26ac^%^3D0^%^26waterfront^%^3D0^%^26finished^%^3D0^%^26unfinished^%^3D0^%^26cityview^%^3D0^%^26mountainview^%^3D0^%^26parkview^%^3D0^%^26waterview^%^3D0^%^26hoadata^%^3D1^%^26zillow-owned^%^3D0^%^263dhome^%^3D0^%^26featuredMultiFamilyBuilding^%^3D0^%^26commuteMode^%^3Ddriving^%^26commuteTimeOfDay^%^3Dnow^%^09^%^096181^%^09^%^7B^%^22isList^%^22^%^3Atrue^%^2C^%^22isMap^%^22^%^3Atrue^%^7D^%^09^%^09^%^09^%^09^%^09",
    "zgsession": "1^|321feb48-96a7-41b1-a86e-49a76b31d316",
    "JSESSIONID": "B6DD2D397081641D75FB4F185CA63E76",
}


class ZillowScraper:
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Connection": "keep-alive",
        # 'Cookie': 'zguid=24^|^%^2437ddf7ac-45b0-413d-91b2-c45bd99d51c4; zjs_anonymous_id=^%^2237ddf7ac-45b0-413d-91b2-c45bd99d51c4^%^22; zjs_user_id=null; zg_anonymous_id=^%^22bda50833-2164-4a5c-b99b-7a4811bda1ca^%^22; AWSALB=lwbOTHTCGpBqGWeKhphQHDh6c2VX2dzJNCQ3YJ+Fcljoe/ux5MmKvFLGiPzy6XQr/I5o0T9i6kIIPIJXA4Rm7y6dSdivQF9s/v+dAuBrFsmQzdS15jYQizlppYyV; AWSALBCORS=lwbOTHTCGpBqGWeKhphQHDh6c2VX2dzJNCQ3YJ+Fcljoe/ux5MmKvFLGiPzy6XQr/I5o0T9i6kIIPIJXA4Rm7y6dSdivQF9s/v+dAuBrFsmQzdS15jYQizlppYyV; search=6^|1703610420512^%^7Crect^%^3D40.8356640592369^%^2C-73.4399776308594^%^2C40.55975337598839^%^2C-74.51938436914065^%^26rid^%^3D6181^%^26disp^%^3Dmap^%^26mdm^%^3Dauto^%^26p^%^3D1^%^26z^%^3D0^%^26listPriceActive^%^3D1^%^26lt^%^3Dfsbo^%^26fs^%^3D1^%^26fr^%^3D0^%^26mmm^%^3D0^%^26rs^%^3D0^%^26ah^%^3D0^%^26singlestory^%^3D0^%^26housing-connector^%^3D0^%^26abo^%^3D0^%^26garage^%^3D0^%^26pool^%^3D0^%^26ac^%^3D0^%^26waterfront^%^3D0^%^26finished^%^3D0^%^26unfinished^%^3D0^%^26cityview^%^3D0^%^26mountainview^%^3D0^%^26parkview^%^3D0^%^26waterview^%^3D0^%^26hoadata^%^3D1^%^26zillow-owned^%^3D0^%^263dhome^%^3D0^%^26featuredMultiFamilyBuilding^%^3D0^%^26commuteMode^%^3Ddriving^%^26commuteTimeOfDay^%^3Dnow^%^09^%^096181^%^09^%^7B^%^22isList^%^22^%^3Atrue^%^2C^%^22isMap^%^22^%^3Atrue^%^7D^%^09^%^09^%^09^%^09^%^09; zgsession=1^|321feb48-96a7-41b1-a86e-49a76b31d316; JSESSIONID=B6DD2D397081641D75FB4F185CA63E76',
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "DNT": "1",
        "Sec-GPC": "1",
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    def fetch(self, url, cookies, params):
        response = requests.get(
            url, headers=self.headers, cookies=cookies, params=params
        )
        print(response.status_code)
        if response.status_code == 500:
            print("Server error (HTTP 500). Retrying...")
            print(response.text)  # Print the response content for further investigation
            time.sleep(5)
            return self.fetch(url, cookies, params)
        return response

    def parse(self, response):
        content = BeautifulSoup(response, "lxml")
        deck = content.find(
            "ul", {"class": "photo-cards photo-cards_wow photo-cards_short"}
        )

        if deck:
            for card in deck.contents:
                script = card.find("script", {"type": "application/ld+json"})
                if script:
                    script_json = json.loads(script.contents[0])

                    self.results.append(
                        {
                            "latitude": script_json["geo"]["latitude"],
                            "longitude": script_json["geo"]["longitude"],
                            "floorSize": script_json["floorSize"]["value"],
                            "url": script_json["url"],
                            "price": card.find(
                                "div", {"class": "list-card-price"}
                            ).text,
                        }
                    )
        else:
            print("No matching elements found in the response.")

    def to_csv(self):
        if not self.results:
            print("No data to write to CSV.")
            return

        with open("zillow.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        url = "https://www.zillow.com/new-york-ny/fsbo/?searchQueryState=^%^7B^%^22pagination^%^22^%^3A^%^7B^%^7D^%^2C^%^22isMapVisible^%^22^%^3Atrue^%^2C^%^22mapBounds^%^22^%^3A^%^7B^%^22west^%^22^%^3A-74.51938436914065^%^2C^%^22east^%^22^%^3A-73.4399776308594^%^2C^%^22south^%^22^%^3A40.55975337598839^%^2C^%^22north^%^22^%^3A40.8356640592369^%^7D^%^2C^%^22regionSelection^%^22^%^3A^%^5B^%^7B^%^22regionId^%^22^%^3A6181^%^2C^%^22regionType^%^22^%^3A6^%^7D^%^5D^%^2C^%^22filterState^%^22^%^3A^%^7B^%^22sort^%^22^%^3A^%^7B^%^22value^%^22^%^3A^%^22globalrelevanceex^%^22^%^7D^%^2C^%^22fsba^%^22^%^3A^%^7B^%^22value^%^22^%^3Afalse^%^7D^%^2C^%^22nc^%^22^%^3A^%^7B^%^22value^%^22^%^3Afalse^%^7D^%^2C^%^22cmsn^%^22^%^3A^%^7B^%^22value^%^22^%^3Afalse^%^7D^%^2C^%^22auc^%^22^%^3A^%^7B^%^22value^%^22^%^3Afalse^%^7D^%^2C^%^22fore^%^22^%^3A^%^7B^%^22value^%^22^%^3Afalse^%^7D^%^7D^%^2C^%^22category^%^22^%^3A^%^22cat2^%^22^%^2C^%^22isListVisible^%^22^%^3Atrue^%^7D"

        for page in range(1, 13):
            params = {
                "searchQueryState": '{"pagination":{},"isMapVisible":true,"mapBounds":{"west":-74.51938436914065,"east":-73.4399776308594,"south":40.55975337598839,"north":40.8356640592369},"regionSelection":[{"regionId":6181,"regionType":6}],"filterState":{"sort":{"value":"globalrelevanceex"},"fsba":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fore":{"value":false}},"category":"cat2","isListVisible":true}',
                "page": page,
            }

            res = self.fetch(url, cookies, params)
            if res.status_code == 200:
                self.parse(res.text)
                time.sleep(2)
            else:
                print(f"Failed to fetch page {page}. Status code: {res.status_code}")


if __name__ == "__main__":
    scraper = ZillowScraper()
    scraper.run()
