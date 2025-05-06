from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


def get_info(soup,response):
    dict_list = []
    front_page_url = response.url[0:response.url.find('ca')-1]
    if soup.find('h3').text != '0 Porsche matching your criteria.':
        for item in soup.find_all('h3'):
            master_dict = {}
            # print(item.text)
            master_dict['car_name'] = item.text
            brothers = item.find_next_siblings()

            master_dict['new_or_not'] = brothers[0].contents[0].text
            master_dict['exterior'] = brothers[1].contents[0].text
            master_dict['interior'] = brothers[1].contents[1].text
            master_dict['milage'] = brothers[2].contents[0].text
            master_dict['n_previous_owner'] = brothers[2].contents[1].text
            master_dict['man_or_aut'] = brothers[2].contents[2].text
            master_dict['power'] = brothers[2].contents[3].text
            master_dict['accident'] = brothers[2].contents[4].text
            master_dict['store_name'] = brothers[3].find('div').contents[0].text
            master_dict['store_address'] = brothers[3].find('div').contents[1].text
            master_dict['price'] = brothers[4].contents[0].text
            master_dict['url_more_info'] = (str(front_page_url) + brothers[5].find('a')['href'])
            try:
                master_dict['fuel_consumption'] = brothers[6].contents[0].text
            except:
                master_dict['fuel_consumption'] = None

            # print(master_dict)
            dict_list.append(master_dict)

        page_df = pd.DataFrame(dict_list)
    else:
        page_df = pd.DataFrame()
    return page_df



def main():
    headers = {
        'authority': 'finder.porsche.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '__Host-next-auth.csrf-token=56f232bf84bf244a1e025d751596eefe732cc372b6a08d532509682af4ad12a1%7Cb9df7bf6a3bd770aaa09ab5f7dabae204c09a8b787226cda58934be8d39d1db1; __Secure-next-auth.callback-url=https%3A%2F%2Ffinder.porsche.com; _gcl_au=1.1.1918311402.1686659711; _fbp=fb.1.1686659711816.644935197; _gid=GA1.2.579919516.1686659919; _ga_1DV4NWZDFX=GS1.1.1686661847.2.1.1686662052.0.0.0; _ga_VEJ4T9F884=GS1.1.1686661847.2.1.1686662053.0.0.0; _ga=GA1.2.1511705357.1686659919',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    run = True
    i = 1
    df = pd.DataFrame()

    while run == True:
        params = {
            'page': str(i)
        }

        response = requests.get('https://finder.porsche.com/ca/en-CA/dealer/search', params=params, headers=headers)

        print('Reading Page ' + str(i))
        print(response)
        print('--------------------------------------------------')
        
        html = response.text
        soup = BeautifulSoup(html , 'html.parser')
        df_page = get_info(soup, response)
        if df_page.empty:
            break
            run = False
        else:
            df = pd.concat([df,df_page], ignore_index= True)
            

        i = i + 1

    df = df.reset_index()
    
    # path = os.getcwd()
    #df.to_csv(path + '\\PorscheWebScraping.csv', index = False)
    
    df.to_csv('PorscheWebScraping.csv', index = False)
    
    return


main()