package com.gr3530904_90104.controller.data;

import java.time.LocalDate;
import java.time.LocalDateTime;

public class RequestControllerIntegrationTestDataSupplier {
    public static String testPutNewDataWithEmptyDataBaseJsonData() {
        return """
                {
                    "MVIDEO": [
                        {
                            "cardName": "GEFORCE RTX 4080 EAGLE OC 16GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4080",
                            "shopName": "MVIDEO",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 111899,
                            "cardPopularity": 1,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE GTX 1650 OC 4GB 128-BIT GAMING",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE GTX 1650",
                            "shopName": "MVIDEO",
                            "vendorName": "ZOTAC",
                            "cardPrice": 14999,
                            "cardPopularity": 2,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3070 VENTUS 3X 8G 256B",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070",
                            "shopName": "MVIDEO",
                            "vendorName": "MSI",
                            "cardPrice": 65999,
                            "cardPopularity": 3,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3070 TI TRINITY OC 8GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070 TI",
                            "shopName": "MVIDEO",
                            "vendorName": "ZOTAC",
                            "cardPrice": 63999,
                            "cardPopularity": 4,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "RADEON RX 6600 XT SPEEDSTER SWIFT 210 8GB",
                            "cardArchitecture": "AMD",
                            "cardSeries": "RADEON RX 6600 XT",
                            "shopName": "MVIDEO",
                            "vendorName": "XFX",
                            "cardPrice": 36999,
                            "cardPopularity": 5,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 4080 GAMING OC 16GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4080",
                            "shopName": "MVIDEO",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 116899,
                            "cardPopularity": 6,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 2060 GAMING AMP 6GB 192BIT",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 2060",
                            "shopName": "MVIDEO",
                            "vendorName": "ZOTAC",
                            "cardPrice": 29999,
                            "cardPopularity": 7,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 12GB 192-BIT ATX",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "MVIDEO",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 43999,
                            "cardPopularity": 8,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 4090 GAMEROCK 24GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4090",
                            "shopName": "MVIDEO",
                            "vendorName": "PALIT",
                            "cardPrice": 146999,
                            "cardPopularity": 9,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 4090 TRINITY OC 24GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4090",
                            "shopName": "MVIDEO",
                            "vendorName": "ZOTAC",
                            "cardPrice": 169999,
                            "cardPopularity": 10,
                            "date": "2023-01-10"
                        }
                    ],
                    "CITILINK": [
                        {
                            "cardName": "GEFORCE RTX 2060 SUPER PA-RTX2060 DUAL 8G NO LED",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 2060 SUPER",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 32990,
                            "cardPopularity": 1,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3050 PA-RTX3050 DUAL",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 29990,
                            "cardPopularity": 2,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G V1",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 43990,
                            "cardPopularity": 3,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 TI PA-RTX3060 DUAL OC 8G V1",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 42990,
                            "cardPopularity": 4,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 RTX3060 DUAL OC 12G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 37990,
                            "cardPopularity": 5,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 42990,
                            "cardPopularity": 6,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3050 PA-RTX3050 DUAL OC",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 28990,
                            "cardPopularity": 7,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3050 GAMING X 8G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "CITILINK",
                            "vendorName": "MSI",
                            "cardPrice": 31890,
                            "cardPopularity": 8,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE GTX 1660 SUPER PA-GTX1660 GP OC 6G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE GTX 1660 SUPER",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 23790,
                            "cardPopularity": 9,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GEFORCE RTX 3070 TI PA-RTX3070 GAMINGPRO 8G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070 TI",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 57990,
                            "cardPopularity": 10,
                            "date": "2023-01-10"
                        }
                    ],
                    "DNS": [
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3070 GAMING OC (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 51999,
                            "cardPopularity": 1,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "KFA2 GEFORCE RTX 3060 X BLACK (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "DNS",
                            "vendorName": "KFA2",
                            "cardPrice": 37499,
                            "cardPopularity": 2,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "PALIT GEFORCE GTX 1660 SUPER GAMING PRO",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE GTX 1660 SUPER",
                            "shopName": "DNS",
                            "vendorName": "PALIT",
                            "cardPrice": 24999,
                            "cardPopularity": 3,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "PALIT GEFORCE RTX 3070 TI GAMINGPRO",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070 TI",
                            "shopName": "DNS",
                            "vendorName": "PALIT",
                            "cardPrice": 55999,
                            "cardPopularity": 4,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "KFA2 GEFORCE RTX 3060 TI X BLACK (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "DNS",
                            "vendorName": "KFA2",
                            "cardPrice": 41999,
                            "cardPopularity": 5,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3060 TI GAMING OC (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 43999,
                            "cardPopularity": 6,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3060 TI EAGLE OC (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 40999,
                            "cardPopularity": 7,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3050 GAMING OC",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 31999,
                            "cardPopularity": 8,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "KFA2 GEFORCE RTX 3050 X BLACK",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "DNS",
                            "vendorName": "KFA2",
                            "cardPrice": 26999,
                            "cardPopularity": 9,
                            "date": "2023-01-10"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3060 GAMING OC (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 38999,
                            "cardPopularity": 10,
                            "date": "2023-01-10"
                        }
                    ]
                }
                """;
    }

    public static String testPutNewDataWithNotEmptyDataBaseJsonData() {
        return """
                {
                    "MVIDEO": [
                        {
                            "cardName": "GEFORCE GTX 1650 OC 4GB 128-BIT GAMING",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE GTX 1650",
                            "shopName": "MVIDEO",
                            "vendorName": "ZOTAC",
                            "cardPrice": 14999,
                            "cardPopularity": 1,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3070 VENTUS 3X 8G 256B",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070",
                            "shopName": "MVIDEO",
                            "vendorName": "MSI",
                            "cardPrice": 65999,
                            "cardPopularity": 2,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3070 TI TRINITY OC 8GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070 TI",
                            "shopName": "MVIDEO",
                            "vendorName": "ZOTAC",
                            "cardPrice": 63999,
                            "cardPopularity": 3,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 4080 GAMING OC 16GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4080",
                            "shopName": "MVIDEO",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 116899,
                            "cardPopularity": 4,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "RADEON RX 6600 XT SPEEDSTER SWIFT 210 8GB",
                            "cardArchitecture": "AMD",
                            "cardSeries": "RADEON RX 6600 XT",
                            "shopName": "MVIDEO",
                            "vendorName": "XFX",
                            "cardPrice": 36999,
                            "cardPopularity": 5,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 4080 EAGLE OC 16GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4080",
                            "shopName": "MVIDEO",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 111899,
                            "cardPopularity": 6,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 12GB 192-BIT ATX",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "MVIDEO",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 43999,
                            "cardPopularity": 7,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE N730K-2GD3/LP",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE GT 730",
                            "shopName": "MVIDEO",
                            "vendorName": "MSI",
                            "cardPrice": 5999,
                            "cardPopularity": 8,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3070 8GB DUAL FAN",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070",
                            "shopName": "MVIDEO",
                            "vendorName": "PNY",
                            "cardPrice": 53999,
                            "cardPopularity": 9,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 4080 GAMEROCK 16GB",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4080",
                            "shopName": "MVIDEO",
                            "vendorName": "PALIT",
                            "cardPrice": 105499,
                            "cardPopularity": 10,
                            "date": "2023-01-02"
                        }
                    ],
                    "CITILINK": [
                        {
                            "cardName": "GEFORCE RTX 2060 SUPER PA-RTX2060 DUAL 8G NO LED",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 2060 SUPER",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 32990,
                            "cardPopularity": 1,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3050 PA-RTX3050 DUAL",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 29990,
                            "cardPopularity": 2,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G V1",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 43990,
                            "cardPopularity": 3,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 TI PA-RTX3060 DUAL OC 8G V1",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 42990,
                            "cardPopularity": 4,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 PA-RTX3060 DUAL 12G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 34590,
                            "cardPopularity": 5,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 RTX3060 DUAL OC 12G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 37990,
                            "cardPopularity": 6,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 42990,
                            "cardPopularity": 7,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3050 PA-RTX3050 DUAL OC",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 28990,
                            "cardPopularity": 8,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE RTX 3050 GAMING X 8G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "CITILINK",
                            "vendorName": "MSI",
                            "cardPrice": 31890,
                            "cardPopularity": 9,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GEFORCE GTX 1660 SUPER PA-GTX1660 GP OC 6G",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE GTX 1660 SUPER",
                            "shopName": "CITILINK",
                            "vendorName": "PALIT",
                            "cardPrice": 23790,
                            "cardPopularity": 10,
                            "date": "2023-01-02"
                        }
                    ],
                    "DNS": [
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3070 GAMING OC (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 49999,
                            "cardPopularity": 1,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 4090 GAMING OC",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 4090",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 149999,
                            "cardPopularity": 2,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "KFA2 GEFORCE RTX 3060 X BLACK (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060",
                            "shopName": "DNS",
                            "vendorName": "KFA2",
                            "cardPrice": 37499,
                            "cardPopularity": 3,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "PALIT GEFORCE GTX 1660 SUPER GAMING PRO",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE GTX 1660 SUPER",
                            "shopName": "DNS",
                            "vendorName": "PALIT",
                            "cardPrice": 24999,
                            "cardPopularity": 4,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "PALIT GEFORCE RTX 3070 TI GAMINGPRO",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070 TI",
                            "shopName": "DNS",
                            "vendorName": "PALIT",
                            "cardPrice": 55999,
                            "cardPopularity": 5,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3060 TI GAMING OC (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 43999,
                            "cardPopularity": 6,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "KFA2 GEFORCE RTX 3060 TI X BLACK (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "DNS",
                            "vendorName": "KFA2",
                            "cardPrice": 41999,
                            "cardPopularity": 7,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3070 TI GAMING OC",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3070 TI",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 57999,
                            "cardPopularity": 8,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3060 TI EAGLE OC (LHR)",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3060 TI",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 39999,
                            "cardPopularity": 9,
                            "date": "2023-01-02"
                        },
                        {
                            "cardName": "GIGABYTE GEFORCE RTX 3050 GAMING OC",
                            "cardArchitecture": "NVIDIA",
                            "cardSeries": "GEFORCE RTX 3050",
                            "shopName": "DNS",
                            "vendorName": "GIGABYTE",
                            "cardPrice": 31999,
                            "cardPopularity": 10,
                            "date": "2023-01-02"
                        }
                    ]
                }
                """;
    }

    public static String defaultDataBasePrepareOldData() {
        return """
                insert into architectures (architecture_name) values
                ('NVIDIA'), ('AMD');
                insert into shops (shop_name) values
                ('MVIDEO'), ('CITILINK'), ('DNS');
                insert into vendors (vendors_name) values
                ('GIGABYTE'), ('ZOTAC'), ('MSI'), ('XFX'), ('PALIT'), ('KFA2');
                insert into gpus (gpu_name, architecture_id, gpu_series) values
                ('GEFORCE RTX 4080 EAGLE OC 16GB', 1, 'GEFORCE RTX 4080'),
                ('GEFORCE GTX 1650 OC 4GB 128-BIT GAMING', 1, 'GEFORCE GTX 1650'),
                ('GEFORCE RTX 3070 VENTUS 3X 8G 256B', 1, 'GEFORCE RTX 3070'),
                ('GEFORCE RTX 3070 TI TRINITY OC 8GB', 1, 'GEFORCE RTX 3070 TI'),
                ('RADEON RX 6600 XT SPEEDSTER SWIFT 210 8GB', 2, 'RADEON RX 6600 XT'),
                ('GEFORCE RTX 4080 GAMING OC 16GB', 1, 'GEFORCE RTX 4080'),
                ('GEFORCE RTX 2060 GAMING AMP 6GB 192BIT', 1, 'GEFORCE RTX 2060'),
                ('GEFORCE RTX 3060 12GB 192-BIT ATX', 1, 'GEFORCE RTX 3060'),
                ('GEFORCE RTX 4090 GAMEROCK 24GB', 1, 'GEFORCE RTX 4090'),
                ('GEFORCE RTX 4090 TRINITY OC 24GB', 1, 'GEFORCE RTX 4090'),
                ('GEFORCE RTX 2060 SUPER PA-RTX2060 DUAL 8G NO LED', 1, 'GEFORCE RTX 2060 SUPER'),
                ('GEFORCE RTX 3050 PA-RTX3050 DUAL', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G V1', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL OC 8G V1', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3060 RTX3060 DUAL OC 12G', 1, 'GEFORCE RTX 3060'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3050 PA-RTX3050 DUAL OC', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE RTX 3050 GAMING X 8G', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE GTX 1660 SUPER PA-GTX1660 GP OC 6G', 1, 'GEFORCE GTX 1660 SUPER'),
                ('GEFORCE RTX 3070 TI PA-RTX3070 GAMINGPRO 8G', 1, 'GEFORCE RTX 3070 TI'),
                ('GIGABYTE GEFORCE RTX 3070 GAMING OC (LHR)', 1, 'GEFORCE RTX 3070'),
                ('KFA2 GEFORCE RTX 3060 X BLACK (LHR)', 1, 'GEFORCE RTX 3060'),
                ('PALIT GEFORCE GTX 1660 SUPER GAMING PRO', 1, 'GEFORCE GTX 1660 SUPER'),
                ('PALIT GEFORCE RTX 3070 TI GAMINGPRO', 1, 'GEFORCE RTX 3070 TI'),
                ('KFA2 GEFORCE RTX 3060 TI X BLACK (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3060 TI GAMING OC (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3060 TI EAGLE OC (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3050 GAMING OC', 1, 'GEFORCE RTX 3050'),
                ('KFA2 GEFORCE RTX 3050 X BLACK', 1, 'KFA2 GEFORCE RTX 3050 X BLACK'),
                ('GIGABYTE GEFORCE RTX 3060 GAMING OC (LHR)', 1, 'GEFORCE RTX 3060');
                insert into offers (gpu_id, shop_id, vendor_id, price, aggregate_date, popularity_place) values
                (1,1,1,111899,'2022-01-10 00:00:00.0',1),
                (2,1,2,14999,'2022-01-10 00:00:00.0',2),
                (3,1,3,65999,'2022-01-10 00:00:00.0',3),
                (4,1,2,63999,'2022-01-10 00:00:00.0',4),
                (5,1,4,36999,'2022-01-10 00:00:00.0',5),
                (6,1,1,116899,'2022-01-10 00:00:00.0',6),
                (7,1,2,29999,'2022-01-10 00:00:00.0',7),
                (8,1,1,43999,'2022-01-10 00:00:00.0',8),
                (9,1,5,146999,'2022-01-10 00:00:00.0',9),
                (10,1,2,169999,'2022-01-10 00:00:00.0',10),
                (11,2,5,32990,'2022-01-10 00:00:00.0',1),
                (12,2,5,29990,'2022-01-10 00:00:00.0',2),
                (13,2,5,43990,'2022-01-10 00:00:00.0',3),
                (14,2,5,42990,'2022-01-10 00:00:00.0',4),
                (15,2,5,37990,'2022-01-10 00:00:00.0',5),
                (16,2,5,42990,'2022-01-10 00:00:00.0',6),
                (17,2,5,28990,'2022-01-10 00:00:00.0',7),
                (18,2,3,31890,'2022-01-10 00:00:00.0',8),
                (19,2,5,23790,'2022-01-10 00:00:00.0',9),
                (20,2,5,57990,'2022-01-10 00:00:00.0',10),
                (21,3,1,51999,'2022-01-10 00:00:00.0',1),
                (22,3,6,37499,'2022-01-10 00:00:00.0',2),
                (23,3,5,24999,'2022-01-10 00:00:00.0',3),
                (24,3,5,55999,'2022-01-10 00:00:00.0',4),
                (25,3,6,41999,'2022-01-10 00:00:00.0',5),
                (26,3,1,43999,'2022-01-10 00:00:00.0',6),
                (27,3,1,40999,'2022-01-10 00:00:00.0',7),
                (28,3,1,31999,'2022-01-10 00:00:00.0',8),
                (29,3,6,26999,'2022-01-10 00:00:00.0',9),
                (30,3,1,38999,'2022-01-10 00:00:00.0',10);
                """;
    }

    public static String defaultDataBasePrepareData() {
        return """
                insert into architectures (architecture_name) values
                ('NVIDIA'), ('AMD');
                insert into shops (shop_name) values
                ('MVIDEO'), ('CITILINK'), ('DNS');
                insert into vendors (vendors_name) values
                ('GIGABYTE'), ('ZOTAC'), ('MSI'), ('XFX'), ('PALIT'), ('KFA2');
                insert into gpus (gpu_name, architecture_id, gpu_series) values
                ('GEFORCE RTX 4080 EAGLE OC 16GB', 1, 'GEFORCE RTX 4080'),
                ('GEFORCE GTX 1650 OC 4GB 128-BIT GAMING', 1, 'GEFORCE GTX 1650'),
                ('GEFORCE RTX 3070 VENTUS 3X 8G 256B', 1, 'GEFORCE RTX 3070'),
                ('GEFORCE RTX 3070 TI TRINITY OC 8GB', 1, 'GEFORCE RTX 3070 TI'),
                ('RADEON RX 6600 XT SPEEDSTER SWIFT 210 8GB', 2, 'RADEON RX 6600 XT'),
                ('GEFORCE RTX 4080 GAMING OC 16GB', 1, 'GEFORCE RTX 4080'),
                ('GEFORCE RTX 2060 GAMING AMP 6GB 192BIT', 1, 'GEFORCE RTX 2060'),
                ('GEFORCE RTX 3060 12GB 192-BIT ATX', 1, 'GEFORCE RTX 3060'),
                ('GEFORCE RTX 4090 GAMEROCK 24GB', 1, 'GEFORCE RTX 4090'),
                ('GEFORCE RTX 4090 TRINITY OC 24GB', 1, 'GEFORCE RTX 4090'),
                ('GEFORCE RTX 2060 SUPER PA-RTX2060 DUAL 8G NO LED', 1, 'GEFORCE RTX 2060 SUPER'),
                ('GEFORCE RTX 3050 PA-RTX3050 DUAL', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G V1', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL OC 8G V1', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3060 RTX3060 DUAL OC 12G', 1, 'GEFORCE RTX 3060'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3050 PA-RTX3050 DUAL OC', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE RTX 3050 GAMING X 8G', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE GTX 1660 SUPER PA-GTX1660 GP OC 6G', 1, 'GEFORCE GTX 1660 SUPER'),
                ('GEFORCE RTX 3070 TI PA-RTX3070 GAMINGPRO 8G', 1, 'GEFORCE RTX 3070 TI'),
                ('GIGABYTE GEFORCE RTX 3070 GAMING OC (LHR)', 1, 'GEFORCE RTX 3070'),
                ('KFA2 GEFORCE RTX 3060 X BLACK (LHR)', 1, 'GEFORCE RTX 3060'),
                ('PALIT GEFORCE GTX 1660 SUPER GAMING PRO', 1, 'GEFORCE GTX 1660 SUPER'),
                ('PALIT GEFORCE RTX 3070 TI GAMINGPRO', 1, 'GEFORCE RTX 3070 TI'),
                ('KFA2 GEFORCE RTX 3060 TI X BLACK (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3060 TI GAMING OC (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3060 TI EAGLE OC (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3050 GAMING OC', 1, 'GEFORCE RTX 3050'),
                ('KFA2 GEFORCE RTX 3050 X BLACK', 1, 'KFA2 GEFORCE RTX 3050 X BLACK'),
                ('GIGABYTE GEFORCE RTX 3060 GAMING OC (LHR)', 1, 'GEFORCE RTX 3060');
                insert into offers (gpu_id, shop_id, vendor_id, price, aggregate_date, popularity_place) values
                (1,1,1,111899,'2023-03-01 12:00:00.0',1),
                (2,1,2,14999,'2023-03-01 12:00:00.0',2),
                (3,1,3,65999,'2023-03-01 12:00:00.0',3),
                (4,1,2,63999,'2023-03-01 12:00:00.0',4),
                (5,1,4,36999,'2023-03-01 12:00:00.0',5),
                (6,1,1,116899,'2023-03-01 12:00:00.0',6),
                (7,1,2,29999,'2023-03-01 12:00:00.0',7),
                (8,1,1,43999,'2023-03-01 12:00:00.0',8),
                (9,1,5,146999,'2023-03-01 12:00:00.0',9),
                (10,1,2,169999,'2023-03-01 12:00:00.0',10),
                (11,2,5,32990,'2023-03-01 12:00:00.0',1),
                (12,2,5,29990,'2023-03-01 12:00:00.0',2),
                (13,2,5,43990,'2023-03-01 12:00:00.0',3),
                (14,2,5,42990,'2023-03-01 12:00:00.0',4),
                (15,2,5,37990,'2023-03-01 12:00:00.0',5),
                (16,2,5,42990,'2023-03-01 12:00:00.0',6),
                (17,2,5,28990,'2023-03-01 12:00:00.0',7),
                (18,2,3,31890,'2023-03-01 12:00:00.0',8),
                (19,2,5,23790,'2023-03-01 12:00:00.0',9),
                (20,2,5,57990,'2023-03-01 12:00:00.0',10),
                (21,3,1,51999,'2023-03-01 12:00:00.0',1),
                (22,3,6,37499,'2023-03-01 12:00:00.0',2),
                (23,3,5,24999,'2023-03-01 12:00:00.0',3),
                (24,3,5,55999,'2023-03-01 12:00:00.0',4),
                (25,3,6,41999,'2023-03-01 12:00:00.0',5),
                (26,3,1,43999,'2023-03-01 12:00:00.0',6),
                (27,3,1,40999,'2023-03-01 12:00:00.0',7),
                (28,3,1,31999,'2023-03-01 12:00:00.0',8),
                (29,3,6,26999,'2023-03-01 12:00:00.0',9),
                (30,3,1,38999,'2023-03-01 12:00:00.0',10);
                """;
    }

    public static String popularityDataBasePrepareData() {
        return """
                insert into architectures (architecture_name) values
                ('NVIDIA'), ('AMD');
                insert into shops (shop_name) values
                ('MVIDEO'), ('CITILINK'), ('DNS');
                insert into vendors (vendors_name) values
                ('GIGABYTE'), ('ZOTAC'), ('MSI'), ('XFX'), ('PALIT'), ('KFA2');
                insert into gpus (gpu_name, architecture_id, gpu_series) values
                ('GEFORCE RTX 4080 EAGLE OC 16GB', 1, 'GEFORCE RTX 4080'),
                ('GEFORCE GTX 1650 OC 4GB 128-BIT GAMING', 1, 'GEFORCE GTX 1650'),
                ('GEFORCE RTX 3070 VENTUS 3X 8G 256B', 1, 'GEFORCE RTX 3070'),
                ('GEFORCE RTX 3070 TI TRINITY OC 8GB', 1, 'GEFORCE RTX 3070 TI'),
                ('RADEON RX 6600 XT SPEEDSTER SWIFT 210 8GB', 2, 'RADEON RX 6600 XT'),
                ('GEFORCE RTX 4080 GAMING OC 16GB', 1, 'GEFORCE RTX 4080'),
                ('GEFORCE RTX 2060 GAMING AMP 6GB 192BIT', 1, 'GEFORCE RTX 2060'),
                ('GEFORCE RTX 3060 12GB 192-BIT ATX', 1, 'GEFORCE RTX 3060'),
                ('GEFORCE RTX 4090 GAMEROCK 24GB', 1, 'GEFORCE RTX 4090'),
                ('GEFORCE RTX 4090 TRINITY OC 24GB', 1, 'GEFORCE RTX 4090'),
                ('GEFORCE RTX 2060 SUPER PA-RTX2060 DUAL 8G NO LED', 1, 'GEFORCE RTX 2060 SUPER'),
                ('GEFORCE RTX 3050 PA-RTX3050 DUAL', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G V1', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL OC 8G V1', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3060 RTX3060 DUAL OC 12G', 1, 'GEFORCE RTX 3060'),
                ('GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G', 1, 'GEFORCE RTX 3060 TI'),
                ('GEFORCE RTX 3050 PA-RTX3050 DUAL OC', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE RTX 3050 GAMING X 8G', 1, 'GEFORCE RTX 3050'),
                ('GEFORCE GTX 1660 SUPER PA-GTX1660 GP OC 6G', 1, 'GEFORCE GTX 1660 SUPER'),
                ('GEFORCE RTX 3070 TI PA-RTX3070 GAMINGPRO 8G', 1, 'GEFORCE RTX 3070 TI'),
                ('GIGABYTE GEFORCE RTX 3070 GAMING OC (LHR)', 1, 'GEFORCE RTX 3070'),
                ('KFA2 GEFORCE RTX 3060 X BLACK (LHR)', 1, 'GEFORCE RTX 3060'),
                ('PALIT GEFORCE GTX 1660 SUPER GAMING PRO', 1, 'GEFORCE GTX 1660 SUPER'),
                ('PALIT GEFORCE RTX 3070 TI GAMINGPRO', 1, 'GEFORCE RTX 3070 TI'),
                ('KFA2 GEFORCE RTX 3060 TI X BLACK (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3060 TI GAMING OC (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3060 TI EAGLE OC (LHR)', 1, 'GEFORCE RTX 3060 TI'),
                ('GIGABYTE GEFORCE RTX 3050 GAMING OC', 1, 'GEFORCE RTX 3050'),
                ('KFA2 GEFORCE RTX 3050 X BLACK', 1, 'KFA2 GEFORCE RTX 3050 X BLACK'),
                ('GIGABYTE GEFORCE RTX 3060 GAMING OC (LHR)', 1, 'GEFORCE RTX 3060');
                insert into offers (gpu_id, shop_id, vendor_id, price, aggregate_date, popularity_place) values
                (1,1,1,111899,now(),1),
                (2,1,2,14999,now(),2),
                (3,1,3,65999,now(),3),
                (4,1,2,63999,now(),4),
                (5,1,4,36999,now(),5),
                (6,1,1,116899,now(),6),
                (7,1,2,29999,now(),7),
                (8,1,1,43999,now(),8),
                (9,1,5,146999,now(),9),
                (10,1,2,169999,now(),10),
                (11,2,5,32990,now(),1),
                (12,2,5,29990,now(),2),
                (13,2,5,43990,now(),3),
                (14,2,5,42990,now(),4),
                (15,2,5,37990,now(),5),
                (16,2,5,42990,now(),6),
                (17,2,5,28990,now(),7),
                (18,2,3,31890,now(),8),
                (19,2,5,23790,now(),9),
                (20,2,5,57990,now(),10),
                (21,3,1,51999,now(),1),
                (22,3,6,37499,now(),2),
                (23,3,5,24999,now(),3),
                (24,3,5,55999,now(),4),
                (25,3,6,41999,now(),5),
                (26,3,1,43999,now(),6),
                (27,3,1,40999,now(),7),
                (28,3,1,31999,now(),8),
                (29,3,6,26999,now(),9),
                (30,3,1,38999,now(),10);
                """;
    }

    public static String testGetPriceForCardFoundExpectedData() {
        return """
                [{"cardName":"GEFORCE RTX 4080 EAGLE OC 16GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4080","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":111899,\
                "cardPopularity":1,"date":"2023-02-28T21:00:00.000+00:00"}]""";
    }

    public static String testGetPriceForVendorFoundExpectedData() {
        return """
                [{"cardName":"GEFORCE RTX 4080 EAGLE OC 16GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4080","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":111899,\
                "cardPopularity":1,"date":"2023-02-28T21:00:00.000+00:00"},\
                {"cardName":"GEFORCE RTX 4080 GAMING OC 16GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4080","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":116899,\
                "cardPopularity":6,"date":"2023-02-28T21:00:00.000+00:00"}]""";
    }

    public static String testGetPriceForShopFoundExpectedData() {
        return """
                [{"cardName":"GEFORCE RTX 4080 EAGLE OC 16GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4080","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":111899,\
                "cardPopularity":1,"date":"2023-02-28T21:00:00.000+00:00"},\
                {"cardName":"GEFORCE RTX 4080 GAMING OC 16GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4080","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":116899,\
                "cardPopularity":6,"date":"2023-02-28T21:00:00.000+00:00"}]""";
    }

    public static String testGetPopularityForShopFoundExpectedData() {
        LocalDateTime date = LocalDate.now().atStartOfDay().minusHours(3);
        return """
                [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},\
                {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},\
                {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},\
                {"1":{"cardName":"GEFORCE RTX 4080 EAGLE OC 16GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4080","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":111899,\
                "cardPopularity":1,"date":"to_replace"},\
                "2":{"cardName":"GEFORCE GTX 1650 OC 4GB 128-BIT GAMING","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE GTX 1650","shopName":"MVIDEO","vendorName":"ZOTAC","cardPrice":14999,\
                "cardPopularity":2,"date":"to_replace"},\
                "3":{"cardName":"GEFORCE RTX 3070 VENTUS 3X 8G 256B","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 3070","shopName":"MVIDEO","vendorName":"MSI","cardPrice":65999,\
                "cardPopularity":3,"date":"to_replace"},\
                "4":{"cardName":"GEFORCE RTX 3070 TI TRINITY OC 8GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 3070 TI","shopName":"MVIDEO","vendorName":"ZOTAC","cardPrice":63999,\
                "cardPopularity":4,"date":"to_replace"},\
                "5":{"cardName":"RADEON RX 6600 XT SPEEDSTER SWIFT 210 8GB",\
                "cardArchitecture":"AMD","cardSeries":"RADEON RX 6600 XT","shopName":"MVIDEO","vendorName":"XFX",\
                "cardPrice":36999,"cardPopularity":5,"date":"to_replace"},\
                "6":{"cardName":"GEFORCE RTX 4080 GAMING OC 16GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4080","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":116899,\
                "cardPopularity":6,"date":"to_replace"},\
                "7":{"cardName":"GEFORCE RTX 2060 GAMING AMP 6GB 192BIT","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 2060","shopName":"MVIDEO","vendorName":"ZOTAC","cardPrice":29999,\
                "cardPopularity":7,"date":"to_replace"},\
                "8":{"cardName":"GEFORCE RTX 3060 12GB 192-BIT ATX","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 3060","shopName":"MVIDEO","vendorName":"GIGABYTE","cardPrice":43999,\
                "cardPopularity":8,"date":"to_replace"},\
                "9":{"cardName":"GEFORCE RTX 4090 GAMEROCK 24GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4090","shopName":"MVIDEO","vendorName":"PALIT","cardPrice":146999,\
                "cardPopularity":9,"date":"to_replace"},\
                "10":{"cardName":"GEFORCE RTX 4090 TRINITY OC 24GB","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 4090","shopName":"MVIDEO","vendorName":"ZOTAC","cardPrice":169999,\
                "cardPopularity":10,"date":"to_replace"}}]"""
                .replaceAll("to_replace", "%d-%s-%dT21:00:00.000+00:00"
                        .formatted(date.getYear(), date.getMonth().getValue() <= 9 ?
                                "0%d".formatted(date.getMonth().getValue()) :
                                        String.valueOf(date.getMonth().getValue()), date.getDayOfMonth()));
    }

    public static String testGetPopularityForVendorFoundExpectedData() {
        LocalDateTime date = LocalDate.now().atStartOfDay().minusHours(3);
        return """
                {"CITILINK":{"1":{"cardName":"GEFORCE RTX 3050 GAMING X 8G","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 3050","shopName":"CITILINK","vendorName":"MSI","cardPrice":31890,\
                "cardPopularity":8,"date":"to_replace"}},"DNS":{},\
                "MVIDEO":{"1":{"cardName":"GEFORCE RTX 3070 VENTUS 3X 8G 256B","cardArchitecture":"NVIDIA",\
                "cardSeries":"GEFORCE RTX 3070","shopName":"MVIDEO","vendorName":"MSI","cardPrice":65999,\
                "cardPopularity":3,"date":"to_replace"}}}"""
                .replaceAll("to_replace", "%d-%s-%dT21:00:00.000+00:00"
                        .formatted(date.getYear(), date.getMonth().getValue() <= 9 ?
                                "0%d".formatted(date.getMonth().getValue()) :
                                String.valueOf(date.getMonth().getValue()), date.getDayOfMonth()));
    }
}
