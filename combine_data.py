import pandas as pd
import numpy as np

# Get website data
website_data = pd.read_csv('data/interim/website_data.csv')
website_data = website_data.rename(columns={'ServiceStationName': 'name',
                                            'Address': 'address',
                                            'Brand': 'brand',
                                            'FuelCode': 'fuel_type',
                                            'cleaned_date': 'last_updated',
                                            'Price': 'price'})
website_data['last_updated'] = pd.to_datetime(website_data['last_updated'], format='%Y-%m-%d %H:%M:%S')

# Get server data
server_data = pd.read_csv('data/interim/server_data.csv')
server_data['last_updated'] = pd.to_datetime(server_data['last_updated'], format='%Y-%m-%d %H:%M:%S')
duplicates = server_data.duplicated()
server_data[duplicates]

# Website data file has local time while server data has UTC time
# Therefore server data needs to be converted from UTC to GMT
server_data['last_updated'] = server_data['last_updated'].dt.tz_localize('UTC').dt.tz_convert('Australia/Sydney').dt.tz_localize(None)

# Website data does not have data on latitude and longitude. 
station_loc = server_data[['address', 'loc_latitude', 'loc_longitude']]
station_loc = station_loc.drop_duplicates()
station_loc['address_modified'] = station_loc['address'].str.lower()
station_loc['address_modified'] = station_loc['address_modified'].str.replace('[^\w\s]', '')
station_loc = station_loc.drop('address', axis=1)

# Get stations that have missing latitude and longitude data
website_coordinates = website_data[['address']].drop_duplicates()
website_coordinates['address_modified'] = website_coordinates['address'].str.lower()
website_coordinates['address_modified'] = website_coordinates['address_modified'].str.replace('[^\w\s]', '')
website_coordinates = pd.merge(website_coordinates, station_loc, how='left', on='address_modified')

# Merge the coordinates from the server data to the website data
website_data_updated = pd.merge(website_data, website_coordinates, how='left', on='address')
#missing = website_data_updated['loc_latitude'].isnull()
#missing = website_data_updated[missing]
#create_lookup(missing['address'].value_counts().index, dictname='coordinates_lookup')

# Create lookup list
coordinates_lookup = {'Smithfield Rd Cnr Elizabeth Dr, Bonnyrigg NSW 2177': (-33.888260, 150.881140),
                      '477-481 Port Hacking Rd, Lilli Pilli NSW 2229': (-34.063540, 151.120070),
                      '531 Princes Highway, Tempe NSW 2216': (-33.920270, 151.167540),
                      '1509-1511 Pittwater Rd, Narrabeen NSW 2101': (-33.704620, 151.296920),
                      '57 Winnima Way, Berkeley NSW 2056': (-34.479930, 150.845920),
                      '1285-1289 Canterbury Rd Cnr Duncan, Punchbowl NSW 2196': (-33.931460, 151.059630),
                      '636-644 Woodville Rd Cnr Orchardlei, Old Guildford NSW 2161': (-33.866500, 150.988150),
                      'Fairlight St Cnr Ramsay Rd, Five Dock NSW 2046': (-33.870130, 151.130910),
                      '118 Old South Head Rd, Woollahra NSW 2025': (-33.889610, 151.255380),
                      '280-286 Canley Vale Rd, Canley Heights NSW 2166': (-33.883930, 150.924160),
                      '278 Sandgate Road, Shortland NSW 2307': (-32.887470, 151.695180),
                      '2/407 Wagga Road, Lavington NSW 2641': (-36.045980, 146.941350),
                      '603-611 Anzac Pde Cnr Snape St, Kingsford NSW 2032': (-33.934350, 151.237110),
                      'Cnr Camden Valley Way & Ash Road, Prestons NSW 2170': (-33.956250, 150.872720),
                      '363 Mona Vale Rd, St Ives North NSW 2075': (-33.716890, 151.173530),}
                    #   '680 Great Western Hwy, FAULCONBRIDGE NSW 2776':
                    #   '236-238 Condamine St, Manly Vale NSW 2093':
                    #   '150 Woodville Rd Cnr Merrylands Rd, Merrylands NSW 2160':
                    #   '169-173 Malabar Rd, Coogee South NSW 2034':
                    #   '229 Woodville Rd Cnr Lackey St, Merrylands NSW 2160':
                    #   '208 Newcanterbury Rd, Petersham NSW 2049':
                    #   '485 - 487 Smithfield Road, Prairiewood NSW 2176':
                    #   '151 Prospect Hwy & Corner Station Road, Seven Hills NSW 2147':
                    #   '166 John St Cnr Gladstone St, Cabramatta NSW 2166':
                    #   '144 Maitland Rd, ISLINGTON NSW 2296':
                    #   '1344 Princes Highway, Heathcote NSW 2233':
                    #   '22 Stanmore Road (Corner Fotheringham Street), Enmore NSW 2042':
                    #   '6 Minjungbal Drive, Tweed Heads NSW 2486':
                    #   '8 - 10 Crystal Street, Petersham NSW 2049':
                    #   '795 Luxford Road (Corner Buckwell Drive), Hassall Grove NSW 2761':       
                    #   '641 King Georges Rd Cnr Percival St, Penshurst NSW 2222':
                    #   '301-305 Hume Highway & Boronia Road, Greenacre NSW 2190':
                    #   '31 Princes Hwy, Albion Park Rail NSW 2527':
                    #   '128 Barker Street, Randwick NSW 2031':
                    #   '244-248 Windang Rd, Windang NSW 2528':
                    #   '198 Great Western Highway, Hazelbrook NSW 2779':
                    #   '86 Cartwright Ave Cnr Woodward Cres, Miller NSW 2168':
                    #   '55 Garfield Road, Riverstone NSW 2765':
                    #   '25 Oxford Street, Paddington NSW 2021':
                    #   '560-562 Victoria Rd Cnr Lawson St, Ermington NSW 2115':
                    #   '351-357 Stoney Creek Rd, Kingsgrove NSW 2208':
                    #   '1 Gregory Hills Drive, Gledswood Hills NSW 2557':
                    #   '133 Wyndham St Cnr Mcevoy St, Alexandria NSW 2015':
                    #   '488 Old South Head Rd Cnr Albemarle, Rose Bay NSW 2029': 
                    #   '165 Parramatta Rd, Haberfield NSW 2045':
                    #   '141-151 Hume Hwy Cnr Chadderton St, Lansvale NSW 2166':
                    #   'Burns Bay Road, Lane Cove NSW 2066':
                    #   '10 Milperra Road, Revesby NSW 2212':
                    #   '50 Bells Line Of Rd Cnr Terrace Rd, North Richmond NSW 2754':
                    #   'Castlereagh Rd Cnr Lugard St, Penrith NSW 2750':
                    #   '435 Church Street, Parramatta NSW 2150':
                    #   '61 Maitland Rd, SANDGATE NSW 2304':
                    #   'Newcastle Rd Cnr William St, East Maitland NSW 2323':
                    #   '49 Canterbury Rd, Bankstown NSW 2200':
                    #   '217-219 Seven Hills Road, Baulkham Hills NSW 2153': 
                    #   '519 Hume Highway & Corner William Street, Yagoona NSW 2199':
                    #   '45 Rookwood road, Yagoona South NSW 2199':
                    #   'Shop 6, 148 Sunnyholt Rd, BLACKTOWN NSW 2148':
                    #   '1962 Camden Valley Way, Edmondson Park NSW 2171':
                    #   '476 Rocky Point Road & Sandringham Street, Sans Souci NSW 2219':
                    #   '67 Shepherds Dr Cnr Macquarie Dr, Cherrybrook NSW 2126':
                    #   '102 Heathcote Road, Moorebank NSW 2170':
                    #   '1 Glenwood Dr, THORNTON NSW 2322':
                    #   'Cobra St Cnr Brisbane St, Dubbo NSW 2830':
                    #   '611-615 Mimosa Street (Corner Forest Road), Bexley NSW 2207':
                    #   '320 Polding Street, Fairfield NSW 2165':
                    #   '61 Warf St, Tweed Heads NSW 2485':
                    #   '121 Victoria Rd Cnr Wellington St, Rozelle NSW 2039':
                    #   '142 Windsor Road (Corner Mulgrave Road), McGraths Hill NSW 2756':        
                    #   '162 - 166 Pioneer Road, Towradgi NSW 2518':
                    #   '200-202 Pennant Hills Rd, Thornleigh NSW 2120':
                    #   'Home Mart Centre Lot1 Minjungbal Drive, Tweed Heads South NSW 2486':     
                    #   '51 Bondi Rd Cnr Park Rd, Bondi NSW 2026':
                    #   '172-174 Princes Highway, Albion Park Rail NSW 2527':
                    #   'Corner Hoxton Park & Websters Roads, Lurnea NSW 2170':
                    #   '125 Princes Highway & Fowles Road, Dapto NSW 2530':
                    #   'Cnr Dunheved Rd & Henry Lawson Dr, Werrington NSW 2747':
                    #   '106 Princes Hwy (Cnr Tannery St), Unanderra NSW 2526':
                    #   '797 Pennant Hills Rd, Carlingford NSW 2118':
                    #   '59-61 Pacific Hwy Cnr Unwin Rd, Waitara NSW 2077':
                    #   'Wilsons Road (Lake Macquarie Fair), Mount Hutton NSW 2290':
                    #   '132 Maitland Road, Mayfield NSW 2304':
                    #   '150-152 Pacific Hwy, Tuggerah NSW 2259':
                    #   '637 Forest Road, Peakhurst NSW 2210':
                    #   '68 Goldsmith St Cnr Bourke St, Goulburn NSW 2580':
                    #   '98 March St Cnr East Market St, Richmond NSW 2753':
                    #   '136 Appin Road, Appin NSW 2560':
                    #   '127 Victoria Road, Rozelle NSW 2039':
                    #   '79 Union Rd, Albury North NSW 2640':
                    #   '198 Parramatta Road (Corner Pyrmont Bridge Road), Camperdown NSW 2050':  
                    #   '516 Punchbowl Rd Cnr Wangee Rd, Lakemba NSW 2195':
                    #   '515 Bunnerong Road, Matraville NSW 2036':
                    #   '210 Guildford road, Guildford NSW 2161':
                    #   'Lot 2 Langford Drive Cnr Mitchell D, Kariong NSW 2250':
                    #   '131 Pennant Hills Rd Cnr Bettington, Carlingford NSW 2118':
                    #   'Lot 1 Cowpasture Rd, Hoxton Park NSW 2171': 
                    #   '387-427 Wattle (Cnr Kelly St), Ultimo NSW 2007':
                    #   '334-336 PARRAMATTA Road, Homebush NSW 2140':
                    #   'Great Western Highway, Marrangaroo NSW 2790':
                    #   '273 Charlestown Road, Charlestown NSW 2290':
                    #   '130 Hamilton Road, Fairfield NSW 2165':
                    #   '159 Mona Vale Rd (Cnr Putarri Av) (Clsd 16 Jun'16), St Ives NSW 2075':   
                    #   '189 South Creek Rd, Cromer NSW 2099':
                    #   '50 Pacific Highway, Doyalson NSW 2262':
                    #   '141 Church St, Gloucester NSW 2422':
                    #   '659 Grose Vale Road, Grose Vale NSW 2753':
                    #   '41 - 43 Princes Highway, Unanderra NSW 2526':
                    #   'Cnr Adelaide & Glenelg Streets, Raymond Terrace NSW 2324':
                    #   '662 Main Rd Cnr Turnbull St, Edgeworth NSW 2285':
                    #   '406 Macquarie Street, Liverpool NSW 2145': 
                    #   'Mid Western Hwy Cnr Emu St, West Wyalong NSW 2671':
                    #   '307-311 Barrenjoey Road (Corner Seaview Avenue), Newport NSW 2106':      
                    #   '770 Pacific Highway & Marks Point Road, Marks Point NSW 2280':
                    #   '86-98 Princes Hwy Cnr Central Rd, Unanderra NSW 2526':
                    #   'Wordoo St Cnr Forrester St, St Marys NSW 2760':
                    #   '21-25 Oxford St, PADDINGTON NSW 2021':
                    #   '189 Belmore Road, Riverwood NSW 2210':
                    #   '30 Argyle Street, Camden NSW 2570':
                    #   '144 Sunnyholt Road, Blacktown NSW 2148':
                    #   '315 Auburn St Cnr Bradley St, Goulburn NSW 2580':
                    #   'The Entrance Rd Cnr Bellevue Rd, Forresters Beach NSW 2260':
                    #   'Kent St Cnr Kathleen St, Tamworth NSW 2340':
                    #   '59-63 Tudor St Cnr Gordon Ave, Hamilton NSW 2303':
                    #   '198 Parramatta Road, CAMPERDOWN NSW 2050':
                    #   '393 Hillsborough Road (Corner Macquarie Road), Warners Bay NSW 2282':    
                    #   '37 Elizabeth St (Cnr Victoria St), Wetherill Park NSW 2164':
                    #   '290 The Entrance Road, Long Jetty NSW 2261':
                    #   '369-375 Concord Rd, Concord West NSW 2138':
                    #   '80-84 Campbell Street, Moruya NSW 2537':
                    #   '75-77 King St Cnr Hoskins St, Warrawong NSW 2502':
                    #   '263 Great Western Highway, Blackheath NSW 2785':
                    #   '745 Main Road, Edgeworth NSW 2285':
                    #   '64-68 Sydney Rd, Kelso NSW 2795':
                    #   'Docker St Cnr Edward St, Wagga Wagga NSW 2650':
                    #   '68 Duri Road, Tamworth NSW 2340':
                    #   '69  Richmond Road, Blacktown NSW 2148':
                    #   '126 Windsor Road, Mcgraths Hill NSW 2756':
                    #   '37 Shellharbour Road, Lake Illawarra NSW 2528':
                    #   '3723 Sturt Hwy, Gumly Gumly NSW 2652':
                    #   '31 Bourke St, Turvey Park NSW 2650':
                    #   '72 Thorney Road, Fairfield West NSW 2165':
                    #   'Cnr Pennant Hills Rd & Parkes St, Thornleigh NSW 2120':
                    #   '101 Hector Street, Sefton NSW 2162': 
                    #   'Anne St Cnr Dangar St, Narrabri NSW 2390':
                    #   'Cnr Hume Hwy & Pine Avenue, Casula NSW 2170':
                    #   '21 White St Cnr Marius St, Tamworth NSW 2340':
                    #   '26 Summerland Way, Kyogle NSW 2474':
                    #   '130 Edgar Street, Condell Park NSW 2200':
                    #   '5-11 Gateway Bvd, MORISSET NSW 2264':
                    #   '426 Princes Hwy, Woonona NSW 2517':
                    #   '769 The Horsley Drive, Smithfield NSW 2164':
                    #   'Barrier Highway, Cobar NSW 2835':
                    #   '406 Pacific Hwy Cnr Floraville Rd, Belmont North NSW 2280':
                    #   '69 Davies Road, Padstow NSW 2211':
                    #   '307-311 Barrenjoey Road  (Corner Seaview Avenue), Newport NSW 2106':     
                    #   '72-74 Clinton Street, Goulburn NSW 2580':
                    #   '133-139 Pettwater Rd, Manly NSW 2095':
                    #   '1a Tumbi Creek Rd, BERKELEY VALE NSW 2261':
                    #   '237 Union St Cnr Three Chain Rd, Lismore South NSW 2480':
                    #   'Church St Cnr Meade St, Glen Innes NSW 2370':
                    #   '84-86 Maitland Road, Muswellbrook NSW 2333':
                    #   '200 Pennant Hills Rd, THORNLEIGH NSW 2120':
                    #   'Cnr Fitzroy & Cobra Streets, Dubbo NSW 2830':
                    #   'New England Highway, Moonbi NSW 2353':
                    #   'Northgate Ctr 224 Princess Hway, Fairy Meadow NSW 2519':
                    #   'Dean St Cnr Creek St, Albury NSW 2640':
                    #   '183 The Horsley Drive, Fairfield NSW 2165':
                    #   '394-396 Crown Street, Wollongong NSW 2500':
                    #   'Cnr Pacific Hwy & Herber Street, Grafton South NSW 2461':
                    #   '638 New South Head Rd, Rose Bay NSW 2029':
                    #   '64 Orange Grove Road, Warwick Farm NSW 2170':
                    #   '66 Memorial Avenue, Woy Woy NSW 2256':
                    #   '147 Cary St, Toronto NSW 2283':
                    #   '2 Blaxcell St, Granville NSW 2142':
                    #   'Pennant Hills Rd & Park St, THORNLEIGH NSW 2120':
                    #   '572-574 Hume Hwy, Casula NSW 2170':
                    #   '1-7 Buchanan St, Murwillumbah NSW 2484':
                    #   '59-63 Tudor Street, Hamilton NSW 2033':
                    #   'Isabella St Cnr Primrose St, Wingham NSW 2429':
                    #   '35 Alison Road, Wyong NSW 2259':
                    #   '139-141 Otho St Cnr Glen Innes Rd, Inverell NSW 2360':
                    #   '1542 Federal Highway Service Road, Sutton NSW 2620':
                    #   '160-162 Jerilderie St, BERRIGAN NSW 2712': 
                    #   '24 Railwayst, Lidcombe NSW 2141':
                    #   '182 Tweed Valley Way, Murwillumbah NSW 2484':
                    #   '190-198 Princess Hwy, South Nowra NSW 2541':
                    #   '1 Minjungbal Dr, TWEED HEADS SOUTH NSW 2486':
                    #   '8-10 Perouse Rd, Randwick NSW 2031':
                    #   '88 Clovelly Road, Randwick NSW 2031':
                    #   '34 Links Ave, East Ballina NSW 2478':
                    #   '73-75 Dawson Street, LISMORE NSW 2480':
                    #   '147 Cary St, TORONTO NSW 2283':
                    #   '3030 Remembrance Driveway, BARGO NSW AUSTRALIA 2574': 
                    #   '16-18 Lake St Cnr Macintosh St, Forster NSW 2428':
                    #   'Lang Street and Hunter ExpressWay, Kurri Kurri NSW 2327':
                    #   '61 Maitland Road, Sandgate NSW 2304':
                    #   '114,Boundary Rd, Peakhurst NSW 2210':
                    #   'Cnr Main and Else Streets, Cundletown NSW 2090':
                    #   '4-6 Kosciusko Rd, Jindabyne NSW 2627':
                    #   'Cnr Gordan & Hollingsworth Sts, Port Macquarie NSW 2444':
                    #   '629 Pacific Hwy, Kempsey South NSW 2440':
                    #   '36 -38 Lanecove Road, Ryde NSW 2112':
                    #   '85-87 John Street, Coonabarabran NSW 2357':
                    #   '114-116 Church St, Mudgee NSW 2850':
                    #   '1413 Elizabeth Drive, Kemps Creek NSW 2178':
                    #   '729 The Horsley Drive, Smithfield NSW 2164':
                    #   '36 Lane Cove Rd, RYDE NSW 2112':
                    #   '115 Mann Street, Nambucca Heads NSW 2448':
                    #   '411-417 Cleveland St, REDFERN NSW 2016':
                    #   '105 Bent Street, Grafton Fourway NSW 2460':
                    #   '85 Muldoon Street, Taree NSW 2430':
                    #   '54 Alice Street, Moree NSW 2400':
                    #   '181 The River Rd Cnr Uranus Rd, Revesby NSW 2212':
                    #   '700 Victoria Road, Ermington NSW 2115':
                    #   '144 Parramatta Rd Cnr Bold Street, Granville NSW 2142':
                    #   '760 Kingswat, Gymea NSW 2227':
                    #   '442A Punchbowl Road, Belmore NSW 2192':
                    #   'Cnr. Mudgee & Wallerawang Roads, Lidsdale NSW 2790':
                    #   '988 Punchbowl Rd, PUNCHBOWL NSW 2196':
                    #   '134-138 New England Hwy, Rutherford NSW 2320':
                    #   '387 New England Highway, Rutherford NSW 2320':
                    #   '1-3 Church St, PORT KEMBLA NSW 2505':
                    #   '334-336 Parramatta Rd, Homebush NSW 2140':
                    #   '345 Avoca Street, Randwick NSW 2130':
                    #   'Lot 1 Ryre Street, Michelago NSW 2620':
                    #   '426 Ballina Road, Lismore Heights NSW 2480':
                    #   '20 Waratah Street, Bendalong NSW 2539':
                    #   '3 Salt Ash Ave, Salt Ash NSW 2318':
                    #   '32 Bryant Street, NARWEE NSW 2209':
                    #   '239 Union Street, LISMORE NSW 2480': 
                    #   'Cnr Wollombi Road & Alexander Street, Cessnock NSW 2325':
                    #   '66-70 Regent Street, Chippendale NSW 2008':
                    #   '930 King Georges Rd, Blakehurst NSW 2221':
                    #   'Cnr Nelson Bay Road And Lavis Lane, WILLIAMTOWN NSW 2043': 
                    #   'Cnr Pacific Hwy & Amy Close, Wyong NSW 2259':
                    #   '2-14 Henry Lawson Drive, Terranora NSW 2486':
                    #   '92 Lakeside Drive, KANAHOOKA NSW 2530':
                    #   '69 Richmond Road, Blacktown NSW 2148':
                    #   '60 Princes Highway, Narooma NSW 2546':
                    #   'Pacific Hwy, Coolongolook NSW 2423':
                    #   '142 Marsh St Cnr Barney St, Armidale NSW 2350':
                    #   '50E Fitzroy Street, Walcha NSW 2354':
                    #   '82-86 Hamilton Road, Fairfield NSW 2165':
                    #   '73-75 Dawson St, Lismore NSW 2480':
                    #   '397 Main Road (Corner Lowry Street), Cardiff NSW 2285':
                    #   'Cnr Hume Highway & Sheahan Drive, Gundagai NSW 2722':
                    #   '494 Forest Road, Penshurst NSW 2222':
                    #   '2-4 Marsh St, Armidale NSW 2350':
                    #   '2 Lowe Street, Queanbeyan NSW 2620':
                    #   '68 Bathurst Rd, ORANGE NSW 2800':
                    #   '67 Stewart Avenue, Hamilton South NSW 2303':
                    #   '127, ROZELLE NSW 2039':
                    #   '34 Bryant street, Narwee NSW 2208':
                    #   'Caltex 3723 Sturt Hwy, GUMLY GUMLY NSW 2652':
                    #   '1135 Pacific Hwy, Lake Munmorah NSW 2259':
                    #   '8/24 Lagonda Drive, Ingleburn NSW 2565':
                    #   '31 Bourke St, TURVEY PARK NSW 2650':
                    #   '16 King St, Warners Bay NSW 2282':
                    #   '551 Darling St, Rozelle NSW 2039':
                    #   '1 Glenwood Drive, THORNTON NSW 2322':
                    #   '307-313 Ocean Beach Road, UMINA BEACH NSW 2257':
                    #   '7 Lake Albert Road, Wagga Wagga NSW 2650':
                    #   '219 Cobra Street, Dubbo NSW 2830':
                    #   '61-68 Clinton Street, GOULBURN NSW 2580':
                    #   '1109 Argyle Street, Wilton NSW 2571':
                    #   '87-89 Princes Hwy Cnr Hughes St, Batemans Bay NSW 2536': 
                    #   '103 Bridge Street, Uralla NSW 2358':
                    #   '264 Beach Road, Batehaven NSW 2536':
                    #   '1/1 Craft Close, Toormina NSW 2452':
                    #   '84 Oberon Street, Oberon NSW 2787':
                    #   'Lot 51 Bourke Street, DUBBO NORTH NSW 2830':
                    #   '140 Adelaide St, Blayney NSW 2799':
                    #   '1 Ryrie St, MICHELAGO NSW 2620':
                    #   '5 Princes Highway, Moruya NSW 2537':
                    #   '2900 Remembrance Drwy, BARGO NSW 2574':
                    #   '5 Macquarie Rd, MORISSET PARK NSW 2264':
                    #   '61 Maitland Road, SANDGATE NSW 2304':
                    #   '524 Great Western Hwy, St Marys NSW 2760':
                    #   '100 Cambelltown Road, Minto NSW 2566':
                    #   '21 White St, TAMWORTH NSW 2340':
                    #   '39  Alexandra  St, Grenfell NSW 2810':
                    #   '2399 Princes Highway, Bewong NSW 2540':
                    #   '4949 New England Highway, Mcdougalls Hill NSW 2330':
                    #   '616-624 Young Street, Albury NSW 2640':
                    #   '7087 Bucketts Way, Taree NSW 2430':
                    #   '4623 Olympic Hwy, Young NSW 2594':
                    #   '43 Ferguson Street, Canowindra NSW 2804':
                    #   '91-93 Kelly St, Scone NSW 2337':
                    #   '30-34 Banna Avenue, Griffith NSW 2860':
                    #   '215 Kinghorne Street, Nowra NSW 2541':
                    #   '753 Ballina Rd, GOONELLABAH NSW 2480':
                    #   '21 Clunes Road, Clunes NSW 2480':
                    #   '171 Clyde Street, South Granville NSW 2142':
                    #   '85 Travers St, Wagga Wagga NSW 2650':
                    #   '1/39 Melbourne St, East Maitland NSW 2323':
                    #   '305-309 Victoria Road, RYDALMERE NSW 2116':
                    #   '40 Princes Highway, Unanderra NSW 2526':
                    #   '95-97 Ramsey Road, Haberfield NSW 2045':
                    #   '3030 Remembrance Drive, Bargo NSW 2574':
                    #   '41 Minmi Rd, Maryland NSW 2287':
                    #   '13 Castlereagh St, GILGANDRA NSW 2827': 
                    #   '115 Sacville St, Fairfield NSW 2165':
                    #   '38A Gilba Rd, Girraween NSW 2145':
                    #   'Crn Richardson Rd & Nelson Bay Rd, SALT ASH NSW 2318':
                    #   '200 Paterson Rd,, Bolwarra Heights NSW 2320':
                    #   '60-68 Clinton Street, GOULBURN NSW 2580':
                    #   '12-16 Sydney St, Muswellbrook NSW 2333':
                    #   'N2 Woollamia Rd, Huskisson NSW 2540':
                    #   '4 Greta Road, Kulnura NSW 2250':
                    #   'Sturt Highway, Hay NSW 2711': 
                    #   '180 Wyrallah Road, East Lismore NSW 2480':
                    #   '85 Main St, YOUNG NSW 2594':
                    #   '56 Yass St, Gunning NSW 2581':
                    #   '60-64 Schwinghammer Street, Grafton South NSW 2460':
                    #   '112-118 Caswell St, Peak Hill NSW 2869':
                    #   '80 Barker St, Casino NSW 2470':
                    #   '57 Central Coast Hig, West Gosford NSW 2250':
                    #   'Onyx St Cnr Morilla St, Lightning Ridge NSW 2834':
                    #   'Cnr Fox & Edwards Streets, Wagga Wagga NSW 2650':
                    #   '2 Bunga Street, Bermagui NSW 2546':
                    #   '1625 Yarramalong Road, Yarramalong NSW 2259':
                    #   '98 Kurrajong Avenue, Leeton NSW 2705':
                    #   '5243 Snowy Mountains Highway, Adaminaby NSW 2629':
                    #   '11541 Newell Highway, Narrabri NSW 2390':
                    #   '54 Ballina st, Lismore NSW 2480':
                    #   '24 Murray Road, Wingham NSW 2429':
                    #   '60 Hill Road, Lurnea NSW 2170':
                    #   '339 Ballina Road, Goonellabah NSW 2480':
                    #   'Cnr Water St & Werrington Rd, St Marys NSW 2760':
                    #   '236 Lemon Tree Passage, Tanilba Bay NSW 2319':
                    #   '534 Arthur Kaine Drive, Merimbula NSW 2548':
                    #   '88 Bega Street, Tathra NSW 2145':
                    #   'Cnr Pennnant Street & Belford Place, Newcastle NSW 2285':
                    #   '2 Langford Dr, KARIONG NSW 2250':
                    #   '224 Irrigation Way, Narrandera NSW 2700':
                    #   '464-468 Armidale Road, Nemingha NSW 2340':
                    #   '3 Bridge St, Tumbarumba NSW 2653':
                    #   '16 New England Highway, Nemingha NSW 2340':
                    #   '37 Ross St, Goulburn NSW 2580':
                    #   '325 Main Street, Lithgow NSW 2790':
                    #   'Pacific Hwy Cnr Gwyder Hwy, Grafton South NSW 2460':
                    #   '11 Gateway Boulevard, Morisset NSW 2264':
                    #   '637 Forest Road, Peakhurst East NSW 2210':
                    #   '1823 New England Highway, JENNINGS NSW 4383':
                    #   '358 Hoxton Park Rd, Prestons NSW 2170':
                    #   '997 Pemberton St, WEST ALBURY NSW 2640': 
                    #   '760 Kingsway, GYMEA NSW 2227':
                    #   '1 Castlereagh Hwy, LIDSDALE NSW 2790':
                    #   '7 Wyangan Avenue, Griffith NSW 2680':
                    #   '307-309 Bexley Road, Bexley NSW 2207':
                    #   'Olympic Hwy, Culcairn NSW 2660':
                    #   '1600 Princess Hwy, Termeil NSW 2539':
                    #   '2 Belinda St, Gerringong NSW 2534':
                    #   '30 Hovell St, Cootamundra NSW 2590':
                    #   '531 Ocean Drive, North Haven NSW 2443':
                    #   '570 Woodburn Road, Doonbah NSW 2473': 
                    #   '51 Lambton Road, Waratah NSW 2298':
                    #   'Pacific Highway, Clybucca NSW 2440':
                    #   '23 - 25 Grant Street, Broulee NSW 2537':
                    #   '444 West Botany Street, ROCKDALE NSW 2216':
                    #   '153 Princes Highway, Ulladulla NSW 2539':
                    #   '63 Marsden Street, Boorowa NSW 2586':
                    #   '133 Bridge Street, Uralla NSW 2358':
                    #   '656 Warringah Road, Forestville NSW 2087':
                    #   '94 Rouse Street, Tenterfield NSW 2372':
                    #   '16 Davies Rd, Kandos NSW 2848':
                    #   '184 Byng St, Orange NSW 2800':
                    #   '30-34 Princes Highway, Fairy Meadow NSW 2519':
                    #   '5 King St, GOOLOOGONG NSW 2805':
                    #   '151A Mort Street, Lithgow NSW 2790':
                    #   '206 Adelaide St, Heatherbrae NSW 2324':
                        # 'Lot 51 Bourke St (Newell Hwy) Cnr R, Dubbo North NSW 2830':
                        # '5 King St, GOOLOOGONG NSW 2805':
                        # 'Cnr Main and Short Street, YOUNG NSW 2594':
                        # '1 Warners Bay Road, Warners Bay NSW 2280':
                        # '10173 Newell Highway, Forbes NSW 2871':
                        # '29 Pacific Highway, Ulmarra NSW 2462':
                        # '65 Cooma Rd, Narrabri NSW 2390':
                        # '114-116 Church Street, MUDGEE NSW 2850':
                        # '57 Central Coast Highway, West Gosford NSW 2250':
                        # '96 Solitary Islands, Sapphire Beach NSW 2450':
                        # '1 Mulyan St, COWRA NSW 2794': 
                        # 'Cnr Adelaide St And Speedy Lock Lane, HEATHERBRAE NSW 2324':
                        # '49 Burroway Street, Narromine NSW 2821':
                        # '122 Princess Highway, Bodalla NSW 2545':
                        # '2, Ceduna Street, Mount Austin, Wagga Wagga NSW 2650':
                        # '176 Rd, BEACON HILL NSW 2100':
                        # '1185 Bruxner Highway, Wollongbar NSW 2477':
                        # '1 Morilla Street, LIGHTNING RIDGE NSW 2834':
                        # '295 Murray Street, Finley NSW 2713':
                        # 'Cnr Appin Road & Kellerman Drive, ST HELENS PARK NSW 2560':
                        # '45 Foster St, LAKE CARGELLIGO NSW 2672':
                        # '9 Melrose Rd, Albert NSW 2873':
                        # '85 Tenterfield st, Deepwater NSW 2371':
                        # 'lot 8 Woodenbong Road, Bonalbo NSW 2469':
                        # '18 Single Street, Werris Creek NSW 2341':
                        # '84 Cowabbie Street, Coolamon NSW 2701':
                        # '9 Rouse Street, TENTERFIELD NSW 2372':
                        # 'Hume Hwy & Sheahan Bridge, GUNDAGAI NSW 2722':
                        # '2848 Pacific Highway, Tyndale NSW 2460':
                        # '1049 Armidale Road, Nemingha NSW 2340':
                        # '125 Cobra Street, DUBBO NSW 2830':
                        # '10 George Street, Marulan NSW 2579':
                        # '134 MacQueen St, ABERDEEN NSW 2336':
                        # '111 Sutton Street, Cootamundra NSW 2590':
                        # '210 High Street, Wauchope NSW 2446': 
                        # 'Briscoe Street, Tibooburra NSW 2880':
                        # '14456 Newell Highway, Edgeroi NSW 2390':
                        # 'Cnr Katherine and Horse Park Road, Amaroo ACT 2914':
                        # '595 Ocean Drive, North Haven NSW 2443':
                        # '46 Kyogle Road, Bray Park NSW 2484':
                        # '145 Arthur St, Wellington NSW 2820':
                        # 'Palms Oasis Shop Res 321 Boomerang Dr, BLUEYS BEACH NSW 2428':
                        # '122 High St (Cnr West St), Greta NSW 2334':
                        # '5 Young Rd, Cowra NSW 2794':
                        # '50 Sydney Street, Muswellbrook NSW 2333':
                        # '159  Rouse Street, Tenterfield NSW 2372':
                        # '1 Tumut St, Adelong NSW 2729':
                        # '92 Queen Street, Barmedman NSW 2668':
                        # '90 Victoria Street, Temora NSW 2666':
                        # '5 Young  Rd, Cowra NSW 2794':
                        # '23-25 Maitland Rd, Newcastle NSW 2300':
                        # '5 Casino Road, Junction Hill NSW 2460':
                        # '21 Railway Parade, Henty NSW 2658':
                        # '49 Dawson Street, Lismore NSW 2480':
                        # '2126 Camden Valley Way, EDMONDSON PARK NSW 2174': 
                        # '1549 Legetts Drive, Brunkerville NSW 2323':
                        # '1 Jocob Drive, Sussex Inlet NSW 2540':
                        # '11312 Hume Hwy, Holbrook NSW 2644':
                        # 'Coila Service Station 3926 Princes Hwy, COILA NSW 2537':
                        # '34 -38 Bellata Street, Gurley NSW 2398':
                        # 'Corunna St, Burren Junction NSW 2386':
                        # '1 Orlando Street, Coffs Harbour NSW 2450':
                        # 'Ingenia Lifestyle 321 Boomerang Dr, BLUEYS BEACH NSW 2428':
                        # '342 Kanahooka Road, BROWNSVILLE NSW 2530':
                        # '928 Hume Hwy, BASS HILL NSW 2197':
                        # '271-273 Camden Valle, Narellan NSW 2567': 
                        # '176-178 Peisley Street, ORANGE NSW 2800':
                        # '842-844 David Street, Albury NSW 2640':
                        # 'Cnr Arthur Kaine Dr and Dunns Ln, MERIMBULA NSW 2548':
                        # '20 Carrington Street, Goulburn NSW 2583':
                        # '229, Bourke Street, Tolland, Wagga Wagga NSW 2650':
                        # '693/695 George Downe, Kulnura NSW 2250':
                        # '46-48 Hickory Street, DORRIGO NSW 2453':
                        # '289 Canberra Avenue, Fyshwick ACT 2609':
                        # '519-521 Carrington Rd, Londonderry NSW 2753':
                        # '1 St Georges Road, St Georges Basin NSW 2540':
                        # '70 Vales Road, Mannering Park NSW 2259':
                        # '191 Lyons Road, DRUMMOYNE NSW 2047':
                        # '1, Main Street, Young NSW 2594':
                        # '20 Lachlan Street, Condobolin NSW 2877':
                        # '1 Main St, GEROGERY NSW 2642':
                        # '120-128 Forrester Road, ST MARYS NSW 2760':
                        # 'Mann River Caravan Park 4467 Gwydir Hwy, JACKADGERY NSW 2460':
                        # '23-25 Cardigan St, Tullamore NSW 2874':
                        # '2-24 Rawson Pl, HAYMARKET NSW 2000':
                        # '139 ? 145 maitland St., Muswellbrook NSW 2533':
                        # '85 Beach Street, Harrington NSW 2427':
                        # '94 Sturt Highway, BALRANALD NSW 2715': 
                        # '82 Mayne Street, Gulgong NSW 2852':
                        # '1 Molong Street, Stuart town NSW 2820':
                        # '57 Urana Street, Lockhart NSW 2656':
                        # '1 Horatio Street, Mudgee NSW 2850':
                        # '60-64 Princes Hwy, NAROOMA NSW 2546':
                        # '111 Berowra Waters Rd, Berowra NSW 2081':
                        # '2-24 Rawson Place, HAYMARKET NSW 2000':
                        # '20-22 Neeld Street, WYALONG NSW 2671':
                        # '73-79 New South Head Road, EDGECLIFF NSW 2027':
                        # '6 Cadonia Rd, Tuggerawong NSW 2259':
                        # '56 Finch Street, Bingara NSW 2404':
                        # '52 Mitchell St., Eden NSW 2551':
                        # '105 Wyee Rd, WYEE NSW 2259':
                        # '831 New Canterbury Rd, Dulwich Hill NSW 2193':
                        # '928 Hume Highway, Bass Hill NSW 2197':
                        # '14319 Pacific Hwy, Nabiac NSW 2312':
                        # '42- 50 Sydney Street, Muswellbrook NSW 2333':
                        # '55-59 Ring Street, Inverell NSW 2360':
                        # '63 Marsden St, BOOROWA NSW 2586':
                        # '68 Duri Road, TAMWORTH NSW 2340':
                        # '464- 468 New England Highway, Nemingha NSW 2340': 
                        # '21 Caigan Street, DUNEDOO NSW 2844':
                        # '15 Murray Dwyer Court, Mayfield West NSW 2304':
                        # '36 Wilson St, Collarenebri NSW 2833':
                        # '43 Ferguson Street, CANOWINDRA NSW 2804':
                        # '1 Law Close, GUNNEDAH NSW 2380':
                        # '158-162 Gregory Street, South West Rocks NSW 2431':
                        # '30 Stockton Ave, MOOREBANK NSW 2170':
                        # '4 Bent Street, Gerogery NSW 2642':
                        # '30 Stockton Ave, Moorebank NSW 2170':
                        # '18-20 Zara Street, Goolgowi NSW 2652':
                        # '21 Fitzroy St, Binalong NSW 2584':
                        # '7717 Bruxner Hwy, DRAKE VILLAGE NSW 2469':
                        # '171 Manilla Road, Tamworth NSW 2340':
                        # '2a Beach Road, BATEMANS BAY NSW 2536':
                        # '2 Kable Avenue, TAMWORTH NSW 2340':
                    #   }

website_data_updated['loc_latitude'] = website_data_updated['loc_latitude'].fillna(website_data_updated['address'].apply(lambda x: coordinates_lookup[x][0] if x in coordinates_lookup else np.nan))
website_data_updated['loc_longitude'] = website_data_updated['loc_longitude'].fillna(website_data_updated['address'].apply(lambda x: coordinates_lookup[x][1] if x in coordinates_lookup else np.nan))

# Check amount of missing data
missing = website_data_updated[website_data_updated['loc_latitude'].isnull()]
print(len(missing))

# Merge data
combined = pd.concat([website_data_updated, server_data], sort=False)
combined = combined[['name', 'address', 'brand', 'fuel_type', 'price', 'last_updated', 'station_code', 'loc_latitude', 'loc_longitude']]
combined = combined.drop_duplicates()
combined.to_csv('data/interim/all_data_cleaned.csv', index=False)

# Get holidays data
holidays = pd.read_csv('data/interim/holidays_data.csv')
holidays['NSW'] = holidays['Jurisdiction'].apply(lambda x: 'nsw' in x.lower())
holidays.to_csv('data/interim/holidays_cleaned.csv', index=False)