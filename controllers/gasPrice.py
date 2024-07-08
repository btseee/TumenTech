import requests
from bs4 import BeautifulSoup
import pandas as pd


class GasPriceScraper:
    def __init__(self, url='http://www.shunkhlai.mn/prices', columns_to_average=None):
        self.url = url
        self.dataframe = None
        self.columns_to_average = columns_to_average or ['А-80', 'АИ-92', 'Евро-5-92', 'АИ-95', 'АИ-98', 'ДТ',
                                                         'Евро-ДТ', 'ДТ /хурд/', 'LPG']

    def scrape_data(self):
        response = requests.get(self.url)
        web_content = response.content
        soup = BeautifulSoup(web_content, 'html.parser')
        table = soup.find('table', {'id': 'shtsprices'})

        # Extract headers
        headers = [th.text.strip() for th in table.find_all('th')]

        # Extract rows
        rows = []
        for tr in table.find_all('tr')[1:]:
            tds = tr.find_all('td')
            row = [td.text.strip() for td in tds]
            rows.append(row)

        # Find the maximum number of columns
        max_columns = max(len(row) for row in rows)

        # Ensure all rows have the same number of columns
        adjusted_rows = []
        for row in rows:
            while len(row) < max_columns:
                row.append('')
            adjusted_rows.append(row)

        # Ensure headers match the number of columns
        while len(headers) < max_columns:
            headers.append(f'Extra Column {len(headers) + 1}')

        # Create DataFrame
        self.dataframe = pd.DataFrame(adjusted_rows, columns=headers)

        return self.dataframe

    def calculate_average(self):
        if self.dataframe is None:
            self.scrape_data()

        averages = {}
        for column_name in self.columns_to_average:
            if column_name in self.dataframe.columns:
                # Convert the column to numeric, forcing errors to NaN
                self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name], errors='coerce')
                # Calculate the average, ignoring NaN values
                average_value = self.dataframe[column_name].mean()
                averages[column_name] = average_value

        return averages


if __name__ == '__main__':
    scraper = GasPriceScraper()
    averages = scraper.calculate_average()['ДТ']
    print(f'Averages of specified columns: {averages}')