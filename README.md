# livePM10PolutionInPoland

## Project created to provide dashboard that presents up-to-date PM10 and PM2.5 dust polution in Poland

To supply data to dashboard I created script in python. 
At first script get data about all avaliable measurement stations in Poland. Next for every station script crawls polution data on specified parametr.
Last step is to join information about sensor and measurment stand and send data to remote google sheet. 

Sript hosted on python anywhere executes every 24 hour. 

Visualization was created in ArcGisOnline that reads data from google sheets. Based on longitude, latittude and polution amount, live dashboard provides very user fiendly information about current polution in any region in Poland.
