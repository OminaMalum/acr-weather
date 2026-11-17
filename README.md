# ACR Live Contractor Forecast

Live National Weather Service forecast for ACR Supply's 8 store areas, made for the store TVs (TPM Web layer).

- `index.html` shows all 8 stores. Add `?store=raleigh` (durham, carrboro, burlington, greensboro, winstonsalem, greenville, wilmington) for one store.
- Data: api.weather.gov, pulled in the browser every 15 minutes. The page reloads itself every 6 hours.
- Design changes: edit `source/template.html`, then run `python3 source/build_page.py` from a copy that has the NC outline file.
