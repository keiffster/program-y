# MetOffice Service

This service provides access to the MetOffice Weather API. Its use MetOffer 1.x Python library and currently supports 
the following AIML Grammars

```
    METOFFICE HELP
    METOFFICE WEATHER POSTCODE *
    METOFFICE OBSERVATION LAT SIGN * DEC * FRAC * LNG SIGN * DEC * FRAC *
    METOFFICE FORECAST LAT SIGN * DEC * FRAC * LNG SIGN * DEC * FRAC * HOURS *
    METOFFICE FORECAST LAT SIGN * DEC * FRAC * LNG SIGN * DEC * FRAC * DAYS *
```

##### METOFFICE HELP
Displays the above list of available grammars

##### METOFFICE WEATHER POSTCODE *
Gets the weather observation for the supplied post code. 
    
##### METOFFICE OBSERVATION LAT SIGN * DEC * FRAC * LNG SIGN * DEC * FRAC *
Get the weather observation for the supplied latitude and longitude

##### METOFFICE FORECAST LAT SIGN * DEC * FRAC * LNG SIGN * DEC * FRAC * HOURS *
Get the weather forecast for the supplied latitude and longitude, up to 24 hours into the future. 
The forecast is at a 3 hour granularity
    
##### METOFFICE FORECAST LAT SIGN * DEC * FRAC * LNG SIGN * DEC * FRAC * DAYS *
Get the weather forecast for the supplied latitude and longitude, up to 5 days into the future
The forecast is at 24 hour granularity

For more information on the response parameters see metoffice.aiml which is packaged along with the actual service code


## Configuration
The configuration file for MetOffice service is as follows. Format is Yaml

```yaml
service:
    type: library
    name: metoffice
    category: weather
    service_class: programy.services.library.metoffice.service.MetOfficeService
    success_prefix: METOFFICE RESULT
    default_response: METOFFICE SERVICE ERROR
```

* type - Type of service, library ( this one ) or rest if it is a REST HTTP(S) call
* name - Name of the service. This is used in the `sraix` call
* category - Category of the service, used by coordinators when there is more than one service of the same category
* service_class - The Python class implementing the service
* success_prefix - The string to prepend the result with
* default_response - String to re