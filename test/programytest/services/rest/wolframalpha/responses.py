
simple_success_response = """{
    "queryresult": {
        "success": true,
        "error": false,
        "numpods": 15,
        "datatypes": "AdministrativeDivision,City,MetropolitanArea,NuclearReactor,Person,WeatherStation",
        "timedout": "",
        "timedoutpods": "",
        "timing": 5.467,
        "parsetiming": 0.194,
        "parsetimedout": false,
        "recalculate": "",
        "id": "MSP105471d4ehfe4d621c4ae00004b8di1c69i279i6f",
        "host": "https://www4c.wolframalpha.com",
        "server": "22",
        "related": "https://www4c.wolframalpha.com/api/v1/relatedQueries.jsp?id=MSPa105481d4ehfe4d621c4ae00001710f8b738fbi7g57057743846044200396",
        "version": "2.6",
        "pods": [
            {
                "title": "Input interpretation",
                "scanner": "Identity",
                "id": "Input",
                "position": 100,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "plaintext": "Edinburgh, Edinburgh"
                    }
                ],
                "expressiontypes": {
                    "name": "Default"
                }
            },
            {
                "title": "Populations",
                "scanner": "Data",
                "id": "Population:CityData",
                "position": 200,
                "error": false,
                "numsubpods": 1,
                "primary": true,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": [
                                "CityData",
                                "MetropolitanAreaData",
                                "USCensusData"
                            ]
                        },
                        "plaintext": "city population | 446110 people (country rank: 11th) (2006 estimate) metro area population | 710469 people (Edinburgh metro area) (2007 estimate)"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                },
                "states": [
                    {
                        "name": "Show history",
                        "input": "Population:CityData__Show history"
                    }
                ]
            },
            {
                "title": "Location",
                "scanner": "Data",
                "id": "Location:CityData",
                "position": 300,
                "error": false,
                "numsubpods": 2,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": [
                                "AdministrativeDivisionData",
                                "CityData"
                            ]
                        },
                        "plaintext": "Edinburgh, Scotland, United Kingdom"
                    },
                    {
                        "title": "",
                        "microsources": {
                            "microsource": [
                                "AdministrativeDivisionData",
                                "CityData",
                                "CountryData"
                            ]
                        },
                        "datasources": {
                            "datasource": "CIAFactbook"
                        },
                        "plaintext": ""
                    }
                ],
                "expressiontypes": [
                    {
                        "name": "Default"
                    },
                    {
                        "name": "Default"
                    }
                ],
                "states": [
                    {
                        "name": "World map",
                        "input": "Location:CityData__World map"
                    },
                    {
                        "name": "Show coordinates",
                        "input": "Location:CityData__Show coordinates"
                    }
                ],
                "infos": {
                    "links": {
                        "url": "http://maps.google.com?ie=UTF8&z=12&t=k&ll=55.95%2C-3.2&q=55.95%20N%2C%203.2%20W",
                        "text": "Satellite image"
                    }
                }
            },
            {
                "title": "Local map",
                "scanner": "Data",
                "id": "Map:CityData",
                "position": 400,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": [
                                "CityData",
                                "OpenStreetMap"
                            ]
                        },
                        "plaintext": ""
                    }
                ],
                "expressiontypes": {
                    "name": "Default"
                },
                "states": [
                    {
                        "count": 13,
                        "value": "30 miles across",
                        "delimiters": "",
                        "states": [
                            {
                                "name": "4 miles across",
                                "input": "Map:CityData__4 miles across"
                            },
                            {
                                "name": "7 miles across",
                                "input": "Map:CityData__7 miles across"
                            },
                            {
                                "name": "10 miles across",
                                "input": "Map:CityData__10 miles across"
                            },
                            {
                                "name": "30 miles across",
                                "input": "Map:CityData__30 miles across"
                            },
                            {
                                "name": "60 miles across",
                                "input": "Map:CityData__60 miles across"
                            },
                            {
                                "name": "120 miles across",
                                "input": "Map:CityData__120 miles across"
                            },
                            {
                                "name": "240 miles across",
                                "input": "Map:CityData__240 miles across"
                            },
                            {
                                "name": "480 miles across",
                                "input": "Map:CityData__480 miles across"
                            },
                            {
                                "name": "950 miles across",
                                "input": "Map:CityData__950 miles across"
                            },
                            {
                                "name": "1900 miles across",
                                "input": "Map:CityData__1900 miles across"
                            },
                            {
                                "name": "3600 miles across",
                                "input": "Map:CityData__3600 miles across"
                            },
                            {
                                "name": "5700 miles across",
                                "input": "Map:CityData__5700 miles across"
                            },
                            {
                                "name": "11000 miles across",
                                "input": "Map:CityData__11000 miles across"
                            }
                        ]
                    },
                    {
                        "name": "Metric",
                        "input": "Map:CityData__Metric"
                    }
                ],
                "infos": {
                    "links": {
                        "url": "http://maps.google.com?ie=UTF8&z=12&t=k&ll=55.95%2C-3.2&q=55.95%20N%2C%203.2%20W",
                        "text": "Satellite image"
                    }
                }
            },
            {
                "title": "Administrative regions",
                "scanner": "Data",
                "id": "AdministrativeRegions:CityData",
                "position": 500,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": "CityData"
                        },
                        "plaintext": "region | Edinburgh country | United Kingdom"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                }
            },
            {
                "title": "Current local time",
                "scanner": "Data",
                "id": "CurrentTime:CityData",
                "position": 600,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": "CityData"
                        },
                        "plaintext": "7:49 am GMT | Wednesday, February 19, 2020"
                    }
                ],
                "expressiontypes": {
                    "name": "Default"
                }
            },
            {
                "title": "Current weather",
                "scanner": "Data",
                "id": "WeatherPod:CityData",
                "position": 700,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": [
                                "CityData",
                                "WeatherData"
                            ]
                        },
                        "plaintext": "2 °C (wind chill: -3 °C) | relative humidity: 93% | wind: 22 mph"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                },
                "states": [
                    {
                        "name": "Show history",
                        "input": "WeatherPod:CityData__Show history"
                    },
                    {
                        "count": 3,
                        "value": "British units",
                        "delimiters": "",
                        "states": [
                            {
                                "name": "British units",
                                "input": "WeatherPod:CityData__British units"
                            },
                            {
                                "name": "Metric units",
                                "input": "WeatherPod:CityData__Metric units"
                            },
                            {
                                "name": "Non-metric units",
                                "input": "WeatherPod:CityData__Non-metric units"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Nearby cities",
                "scanner": "Data",
                "id": "CityHierarchyInfo:CityData",
                "position": 800,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": "CityData"
                        },
                        "plaintext": "Dundee | 39 miles north-northeast | 144528 people Glasgow | 42 miles west | 634680 people Newcastle upon Tyne | 91 miles southeast | 280177 people (straight-line distances between city centers)"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                },
                "states": [
                    {
                        "name": "Show metric",
                        "input": "CityHierarchyInfo:CityData__Show metric"
                    },
                    {
                        "name": "More",
                        "input": "CityHierarchyInfo:CityData__More"
                    }
                ]
            },
            {
                "title": "Nearby airport",
                "scanner": "Data",
                "id": "AirportHierarchyInfo:CityData",
                "position": 900,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": "CityData"
                        },
                        "plaintext": "Edinburgh Airport | 7 miles west (straight-line distances between city center and airport)"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                },
                "states": [
                    {
                        "name": "Show metric",
                        "input": "AirportHierarchyInfo:CityData__Show metric"
                    },
                    {
                        "name": "More",
                        "input": "AirportHierarchyInfo:CityData__More"
                    }
                ]
            },
            {
                "title": "Notable company headquarters",
                "scanner": "Data",
                "id": "CompaniesInCity:CityData",
                "position": 1000,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": "CityData"
                        },
                        "datasources": {
                            "datasource": [
                                "ForbesAmericasLargestPrivateCompanies",
                                "CrunchBase"
                            ]
                        },
                        "plaintext": "Royal Bank of Scotland | 71200 employees (Quarter 4 2017) | $16.51 billion per year (Quarter 4 2017)"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                }
            },
            {
                "title": "Geographic properties",
                "scanner": "Data",
                "id": "GeographicProperties:CityData",
                "position": 1100,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": "CityData"
                        },
                        "plaintext": "elevation | 282 ft"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                },
                "states": [
                    {
                        "name": "Show metric",
                        "input": "GeographicProperties:CityData__Show metric"
                    }
                ],
                "infos": {
                    "units": {
                        "short": "ft",
                        "long": "feet"
                    }
                }
            },
            {
                "title": "Nearby features",
                "scanner": "Data",
                "id": "FeaturesHierarchyInfo:CityData",
                "position": 1200,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": [
                                "CityData",
                                "NuclearReactorData"
                            ]
                        },
                        "datasources": {
                            "datasource": "IAEAPowerReactorInformationSystem"
                        },
                        "plaintext": "nuclear power site | Torness | 31 miles east waterfall | An Steall Ban Waterfall (394 feet) | 89 miles northwest waterfall | Cauldron Falls (400 feet) | 97 miles south-southeast (straight-line distances between city center and feature coordinates)"
                    }
                ],
                "expressiontypes": {
                    "name": "Grid"
                },
                "states": [
                    {
                        "name": "Show metric",
                        "input": "FeaturesHierarchyInfo:CityData__Show metric"
                    }
                ]
            },
            {
                "title": "Nearest sea",
                "scanner": "Data",
                "id": "OceansHierarchyInfo:CityData",
                "position": 1300,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": "CityData"
                        },
                        "plaintext": "North Sea (<3 miles)  (straight-line distance between city center and shore)"
                    }
                ],
                "expressiontypes": {
                    "name": "Default"
                },
                "states": [
                    {
                        "name": "Show metric",
                        "input": "OceansHierarchyInfo:CityData__Show metric"
                    }
                ]
            },
            {
                "title": "Notable people born in Edinburgh",
                "scanner": "Data",
                "id": "NotablePeople:CityData",
                "position": 1400,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "microsources": {
                            "microsource": [
                                "CityData",
                                "PeopleData"
                            ]
                        },
                        "plaintext": "Sean Connery (actor) (1930) King James I (royalty) (1566) Alexander Graham Bell (inventor) (1847) Tony Blair (politician) (1953) Arthur Conan Doyle (novelist) (1859) Robert Louis Stevenson (author) (1850) David Hume (philosopher) (1711) Grum (electronic musician) (1986) James Clerk Maxwell (physicist) (1831) Shirley Manson (musician) (1966) ..."
                    }
                ],
                "expressiontypes": {
                    "name": "Default"
                },
                "states": [
                    {
                        "name": "More",
                        "input": "NotablePeople:CityData__More"
                    },
                    {
                        "name": "Show dates",
                        "input": "NotablePeople:CityData__Show dates"
                    },
                    {
                        "name": "Show deaths",
                        "input": "NotablePeople:CityData__Show deaths"
                    }
                ]
            },
            {
                "title": "Wikipedia page hits history",
                "scanner": "Data",
                "id": "PopularityPod:WikipediaStatsData",
                "position": 1500,
                "error": false,
                "numsubpods": 1,
                "subpods": [
                    {
                        "title": "",
                        "plaintext": ""
                    }
                ],
                "expressiontypes": {
                    "name": "TimeSeriesPlot"
                },
                "states": [
                    {
                        "name": "Log scale",
                        "input": "PopularityPod:WikipediaStatsData__Log scale"
                    }
                ]
            }
        ],
        "assumptions": {
            "type": "Clash",
            "word": "EDINBURGH UK",
            "template": "Assuming '${word}' is ${desc1}. Use as ${desc2} instead",
            "count": 2,
            "values": [
                {
                    "name": "City",
                    "desc": "a city",
                    "input": "*C.EDINBURGH+UK-_*City-"
                },
                {
                    "name": "AdministrativeDivision",
                    "desc": "an administrative division",
                    "input": "*C.EDINBURGH+UK-_*AdministrativeDivision-"
                }
            ]
        },
        "userinfoused": {
            "name": "Country"
        },
        "sources": [
            {
                "url": "https://www4c.wolframalpha.com/sources/AdministrativeDivisionDataSourceInformationNotes.html",
                "text": "Administrative division data"
            },
            {
                "url": "https://www4c.wolframalpha.com/sources/CityDataSourceInformationNotes.html",
                "text": "City data"
            },
            {
                "url": "https://www4c.wolframalpha.com/sources/MetropolitanAreaDataSourceInformationNotes.html",
                "text": "Metropolitan area data"
            },
            {
                "url": "https://www4c.wolframalpha.com/sources/NuclearReactorDataSourceInformationNotes.html",
                "text": "Nuclear reactor data"
            },
            {
                "url": "https://www4c.wolframalpha.com/sources/OpenStreetMapSourceInformationNotes.html",
                "text": "Open street map"
            },
            {
                "url": "https://www4c.wolframalpha.com/sources/PeopleDataSourceInformationNotes.html",
                "text": "People data"
            },
            {
                "url": "https://www4c.wolframalpha.com/sources/USCensusDataSourceInformationNotes.html",
                "text": "US census data"
            },
            {
                "url": "https://www4c.wolframalpha.com/sources/WeatherDataSourceInformationNotes.html",
                "text": "Weather data"
            }
        ]
    }
}"""

short_success_response = "about 2464 miles"
