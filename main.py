
POSITIONS = 2

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import pyfiglet

# przygotuj dane do tworzenia stron

url = "https://everynoise.com/"
r = requests.get(url, allow_redirects=True)
soup = BeautifulSoup(r.content, 'html.parser')

datas = []

for i in range(1, POSITIONS + 1):
    print(f"processing... {i}/{POSITIONS}")
    
    div = soup.find('div', id=f'item{i}')
    
    preview_url = div.get("preview_url")
    genre = div.text[:-2]

    ai_input = f"Opowiedz mi coś o gatunku muzycznym {genre}."
    ai_output = DDGS().chat(ai_input, model='gpt-4o-mini')
    
    datas.append({
        "preview_url" : preview_url,
        "genre" : genre,
        "ai_input" : ai_input,
        "ai_output" : ai_output
    })
   
# stwórz index    
page = open("index.md", "w", encoding="utf8")

page.write(
'''\
---
layout: default
---
'''
)

page.write(
f'''
# Zaczerpnij muzyki!

Przykładowa lista {POSITIONS} gatunków muzycznych zaczerpniętych ze strony [Every Noice at Once]({url}) 🎧


'''
)

for data in datas:
    page.write(
f'''
- ## {data["genre"]}

[**👉 posłuchaj kawałka?**]({data["preview_url"]})

[**👉 dowiedz się więcej!**]({data["genre"]})

'''
    )
    
page.write(
f'''**Więcej** możesz znaleźć na stronie [Every Noice at Once]({url})!'''
)

page.close()
    
# stwórz podstrony
for data in datas:
    page = open(f"{data['genre']}.md", "w", encoding="utf8")
    
    page.write(
'''\
---
layout: default
---
'''
    )
    
    page.write(
f'''
```
{pyfiglet.figlet_format(data["genre"])}
```
**Wspaniały** wybór!

Przykładowego utworu możesz posłuchać [tutaj]({data["preview_url"]})!
## Dowiedz się więcej
Zerknij proszę na poniższy krótki opis tego dźwięcznego gatunku, zaproponowany przez sztuczną inteligencję!



**Zapytanie:**

{data["ai_input"]}

**Odpowiedź:**

''' + data["ai_output"].replace("\n", "<br>")
    )
    page.close()


