[out:json][timeout:300];
area["ISO3166-1"="AU"][admin_level=2]->.au;
(
  node["amenity"="charging_station"](area.au);
  way["amenity"="charging_station"](area.au);
  relation["amenity"="charging_station"](area.au);
);
out center tags;
