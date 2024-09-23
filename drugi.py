import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scrape_realitica_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    properties = []
    
    for item in soup.find_all('div', class_='property-item'):  
        try:
            vrsta = item.find('span', class_='property-type').text.strip() if item.find('span', class_='property-type') else 'N/A'
            podrucje = item.find('span', class_='property-area').text.strip() if item.find('span', class_='property-area') else 'N/A'
            lokacija = item.find('span', class_='property-location').text.strip() if item.find('span', class_='property-location') else 'N/A'
            broj_soba = int(item.find('span', class_='property-bedrooms').text.strip()) if item.find('span', class_='property-bedrooms') else 0
            broj_kupatila = int(item.find('span', class_='property-bathrooms').text.strip()) if item.find('span', class_='property-bathrooms') else 0
            cijena = float(item.find('span', class_='property-price').text.replace('€', '').replace(',', '').strip()) if item.find('span', class_='property-price') else 0.0
            povrsina = int(item.find('span', class_='property-area').text.replace('m²', '').strip()) if item.find('span', class_='property-area') else 0
            parking_mjesta = int(item.find('span', class_='property-parking').text.strip()) if item.find('span', class_='property-parking') else 0
            od_mora = int(item.find('span', class_='property-distance-sea').text.replace('m', '').strip()) if item.find('span', class_='property-distance-sea') else 0
            novogradnja = True if item.find('span', class_='property-new') else False
            klima = True if item.find('span', class_='property-air-conditioning') else False
            naslov = item.find('span', class_='property-title').text.strip() if item.find('span', class_='property-title') else 'N/A'
            opis = item.find('span', class_='property-description').text.strip() if item.find('span', class_='property-description') else 'N/A'
            oglasio = item.find('span', class_='property-publisher').text.strip() if item.find('span', class_='property-publisher') else 'N/A'
            mobilni = item.find('span', class_='property-phone').text.strip() if item.find('span', class_='property-phone') else 'N/A'
            oglas_id = int(item.find('span', class_='property-id').text.strip()) if item.find('span', class_='property-id') else 0
            zadnja_promjena = item.find('span', class_='property-last-change').text.strip() if item.find('span', class_='property-last-change') else 'N/A'
            slike = [img['src'] for img in item.find_all('img', class_='property-image')]
            link = item.find('a', class_='property-link')['href'] if item.find('a', class_='property-link') else 'N/A'

            properties.append({
                'vrsta': vrsta,
                'područje': podrucje,
                'lokacija': lokacija,
                'broj_spavaćih_soba': broj_soba,
                'broj_kupatila': broj_kupatila,
                'cijena': cijena,
                'stambena_površina': povrsina,
                'parking_mjesta': parking_mjesta,
                'od_mora': od_mora,
                'novogradnja': novogradnja,
                'klima': klima,
                'naslov': naslov,
                'opis': opis,
                'web_stranica': link,
                'oglasio': oglasio,
                'mobilni': mobilni,
                'broj_id_oglasa': oglas_id,
                'zadnja_promjena': zadnja_promjena,
                'slike': slike,
                'link_do_nekretnine': link
            })
            print(f"Added property: {vrsta}, {cijena}, {povrsina}")  

        except Exception as e:
            print(f"Error parsing item: {e}")
    
    return properties

def scrape_realitica_all_pages(base_url):
    page_num = 1
    all_properties = []

    while True:
        url = f"{base_url}&page={page_num}"
        print(f"Scraping page: {page_num}")
        properties = scrape_realitica_page(url)
        
        if not properties:
            break
        
        all_properties.extend(properties)
        page_num += 1
    
    return all_properties

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def save_sorted_to_csv(data, filename):
    df = pd.DataFrame(data)
    print("DataFrame columns before sorting:", df.columns) 
    if not df.empty:  
        df_sorted = df.sort_values(by=['cijena', 'stambena_površina'], ascending=[False, False])
        df_sorted.to_csv(filename, index=False)
    else:
        print("DataFrame is empty. No data to sort and save.")

if __name__ == "__main__":
    base_url = 'https://www.realitica.com/?option=search&c=real-estate'  
    
    all_properties = scrape_realitica_all_pages(base_url)

    save_to_csv(all_properties, 'nekretnine.csv')
    
    save_sorted_to_csv(all_properties, 'nekretnine_sortirano.csv')

    print("Podaci su uspešno sačuvani u CSV fajlove.")
