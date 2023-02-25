package com.gr3530904_90104.service.impl;

import com.gr3530904_90104.repository.*;
import com.gr3530904_90104.service.DataService;
import com.gr3530904_90104.table.*;
import com.gr3530904_90104.table.dto.OfferDto;
import com.gr3530904_90104.table.dto.OfferDtoMapper;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.mockito.Mockito;
import org.springframework.data.domain.PageImpl;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.*;
import java.util.stream.Stream;

public class DataServiceImplTest {
    private ArchitectureRepository architectureRepository;
    private CardRepository cardRepository;
    private OfferRepository offerRepository;
    private ShopRepository shopRepository;
    private VendorRepository vendorRepository;
    private DataService dataService;

    private static final String CARD_NAME1 = "GEFORCE RTX 3060 TI GAMING X 8GB";
    private static final String CARD_NAME2 = "RADEON RX 6700-XT-MECH-2X";
    private static final String CARD_SERIES1 = "GEFORCE RTX 3060 TI";
    private static final String CARD_SERIES2 = "RADEON RX 6700 XT";
    private static final String ARCHITECTURE_NAME1 = "NVIDIA";
    private static final String ARCHITECTURE_NAME2 = "AMD";
    private static final String SHOP_NAME1 = "MVIDEO";
    private static final String SHOP_NAME2 = "DNS";
    private static final String VENDOR_NAME1 = "MSI";
    private static final String VENDOR_NAME2 = "GIGABYTE";
    private static final Integer PRICE1 = 41999;
    private static final Integer PRICE2 = 62999;
    private static final Integer POPULARITY1 = 1;
    private static final Integer POPULARITY2 = 2;
    private static final Integer ARCHITECTURE_ID1 = 1;
    private static final Integer ARCHITECTURE_ID2 = 2;
    private static final Integer CARD_ID1 = 1;
    private static final Integer CARD_ID2 = 2;
    private static final Integer SHOP_ID1 = 1;
    private static final Integer SHOP_ID2 = 2;
    private static final Integer VENDOR_ID1 = 1;
    private static final Integer VENDOR_ID2 = 2;
    private static final Integer OFFER_ID1 = 1;
    private static final Integer OFFER_ID2 = 2;
    private static final Date AGGREGATE_DATE = Date.from(LocalDate.parse("2022-11-20").atStartOfDay().atZone(ZoneId.systemDefault()).toInstant());
    private static final OfferDto OFFER_DTO1 = new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE);
    private static final OfferDto OFFER_DTO2 = new OfferDto(CARD_NAME2, ARCHITECTURE_NAME2, CARD_SERIES2, SHOP_NAME1, VENDOR_NAME2, PRICE2, POPULARITY2, AGGREGATE_DATE);
    private static final Offer OFFER1 = new Offer(OFFER_ID1, CARD_ID1, SHOP_ID1, VENDOR_ID1, PRICE1, POPULARITY1, AGGREGATE_DATE);
    private static final Offer OFFER2 = new Offer(OFFER_ID2, CARD_ID2, SHOP_ID1, VENDOR_ID2, PRICE2, POPULARITY2, AGGREGATE_DATE);

    @BeforeEach
    public void init() {
        architectureRepository = Mockito.mock(ArchitectureRepository.class);
        cardRepository = Mockito.mock(CardRepository.class);
        offerRepository = Mockito.mock(OfferRepository.class);
        shopRepository = Mockito.mock(ShopRepository.class);
        vendorRepository = Mockito.mock(VendorRepository.class);
        OfferDtoMapper offerDtoMapper = new OfferDtoMapper(architectureRepository, cardRepository, shopRepository, vendorRepository);
        dataService = new DataServiceImpl(architectureRepository, cardRepository, offerRepository, shopRepository, vendorRepository, offerDtoMapper);
    }

    @Test
    public void testPutNewData() {
        Mockito.when(architectureRepository.findArchitectureByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(cardRepository.findCardByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(shopRepository.findShopByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(vendorRepository.findVendorByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(architectureRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Architecture(ARCHITECTURE_ID1, ARCHITECTURE_NAME1));
        Mockito.when(cardRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1));
        Mockito.when(shopRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Shop(SHOP_ID1, SHOP_NAME1));
        Mockito.when(vendorRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Vendor(VENDOR_ID1, VENDOR_NAME1));
        Mockito.when(offerRepository.saveAll(Mockito.any()))
                .thenReturn(List.of(OFFER1));
        Mockito.when(offerRepository.findById(Mockito.eq(OFFER_ID1)))
                .thenReturn(Optional.of(OFFER1));

        dataService.putNewData(List.of(OFFER_DTO1));
        Assertions.assertEquals(OFFER1, offerRepository.findById(OFFER1.getId()).get());
    }

    @Test
    public void testPutNewDataWithEmptyData() {
        Mockito.when(architectureRepository.findArchitectureByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(cardRepository.findCardByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(shopRepository.findShopByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(vendorRepository.findVendorByName(Mockito.any())).thenReturn(Optional.empty());
        Mockito.when(architectureRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Architecture(ARCHITECTURE_ID1, ARCHITECTURE_NAME1));
        Mockito.when(cardRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1));
        Mockito.when(shopRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Shop(SHOP_ID1, SHOP_NAME1));
        Mockito.when(vendorRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Vendor(VENDOR_ID1, VENDOR_NAME1));
        Mockito.when(offerRepository.saveAll(Mockito.any()))
                .thenReturn(List.of());
        Mockito.when(offerRepository.findById(Mockito.eq(OFFER_ID1)))
                .thenReturn(Optional.empty());

        dataService.putNewData(List.of());
        Assertions.assertTrue(offerRepository.findById(OFFER1.getId()).isEmpty());
    }

    @ParameterizedTest
    @MethodSource("testIsCardPresentSource")
    public void testIsCardPresent(String cardName, boolean expectedValue) {
        Mockito.when(cardRepository.findCardByName(Mockito.eq(CARD_NAME1)))
                .thenReturn(Optional.of(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1)));
        Mockito.when(cardRepository.findCardByName(Mockito.eq(CARD_NAME2)))
                .thenReturn(Optional.empty());

        Assertions.assertEquals(expectedValue, dataService.isCardPresent(cardName));
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForCardSource")
    public void testGetPriceForCard(String cardName, List<OfferDto> expectedValue) {
        Mockito.when(cardRepository.findCardByName(Mockito.eq(CARD_NAME1)))
                .thenReturn(Optional.of(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1)));
        Mockito.when(cardRepository.findCardByName(Mockito.eq(CARD_NAME2)))
                .thenReturn(Optional.empty());
        Mockito.when(offerRepository.findByCardIdAndDateBetween(Mockito.any(), Mockito.any(), Mockito.any()))
                        .thenReturn(List.of(OFFER1));
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID1)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID1, ARCHITECTURE_NAME1)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID1)))
                .thenReturn(Optional.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID1)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID1, VENDOR_NAME1)));

        Assertions.assertEquals(expectedValue, dataService.getPriceForCard(cardName));
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForVendorSource")
    public void testGetPriceForVendor(String cardSeries, String vendorName, List<OfferDto> expectedValue) {
        Mockito.when(cardRepository.findCardsByCardSeries(Mockito.eq(CARD_SERIES1)))
                .thenReturn(List.of(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1)));
        Mockito.when(cardRepository.findCardsByCardSeries(Mockito.eq(CARD_SERIES2)))
                .thenReturn(List.of());
        Mockito.when(vendorRepository.findVendorByName(Mockito.eq(VENDOR_NAME1)))
                        .thenReturn(Optional.of(new Vendor(VENDOR_ID1, VENDOR_NAME1)));
        Mockito.when(vendorRepository.findVendorByName(Mockito.eq(VENDOR_NAME2)))
                .thenReturn(Optional.empty());
        Mockito.when(offerRepository.findByCardIdInAndVendorIdAndDateBetween(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any()))
                .thenReturn(List.of(OFFER1));
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID1)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID1, ARCHITECTURE_NAME1)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID1)))
                .thenReturn(Optional.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID1)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID1, VENDOR_NAME1)));

        Assertions.assertEquals(expectedValue, dataService.getPriceForVendor(cardSeries, vendorName));
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForShopSource")
    public void testGetPriceForShop(String cardSeries, String shopName, List<OfferDto> expectedValue) {
        Mockito.when(cardRepository.findCardsByCardSeries(Mockito.eq(CARD_SERIES1)))
                .thenReturn(List.of(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1)));
        Mockito.when(cardRepository.findCardsByCardSeries(Mockito.eq(CARD_SERIES2)))
                .thenReturn(List.of());
        Mockito.when(shopRepository.findShopByName(SHOP_NAME1))
                        .thenReturn(Optional.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(shopRepository.findShopByName(SHOP_NAME2))
                .thenReturn(Optional.empty());
        Mockito.when(offerRepository.findByCardIdInAndShopIdAndDateBetween(
                        Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any()))
                .thenReturn(List.of(OFFER1));
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID1)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID1, ARCHITECTURE_NAME1)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID1)))
                .thenReturn(Optional.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID1)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID1, VENDOR_NAME1)));

        Assertions.assertEquals(expectedValue, dataService.getPriceForShop(cardSeries, shopName));
    }

    @ParameterizedTest
    @MethodSource("testGetPopularityForShopSource")
    public void testGetPopularityForShop(String shopName, List<Map<Integer, OfferDto>> expectedValue) {
        Mockito.when(shopRepository.findShopByName(SHOP_NAME1))
                .thenReturn(Optional.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(shopRepository.findShopByName(SHOP_NAME2))
                .thenReturn(Optional.empty());

        Mockito.when(offerRepository.findByShopIdAndDateOrderByCardPopularityAsc(
                        Mockito.any(), Mockito.any(), Mockito.any()))
                .thenReturn(new PageImpl<>(List.of(OFFER1, OFFER2)));

        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID1)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID1, ARCHITECTURE_NAME1)));
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID2)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID2, ARCHITECTURE_NAME2)));
        Mockito.when(cardRepository.findCardById(Mockito.eq(CARD_ID1)))
                .thenReturn(Optional.of(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1)));
        Mockito.when(cardRepository.findCardById(Mockito.eq(CARD_ID2)))
                .thenReturn(Optional.of(new Card(CARD_ID2, CARD_NAME2, ARCHITECTURE_ID2, CARD_SERIES2)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID1)))
                .thenReturn(Optional.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID1)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID1, VENDOR_NAME1)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID2)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID2, VENDOR_NAME2)));

        Assertions.assertEquals(expectedValue, dataService.getPopularityForShop(shopName));
    }

    @ParameterizedTest
    @MethodSource("testGetPopularityForVendorSource")
    public void testGetPopularityForVendor(String vendorName, Map<String, Map<Integer, OfferDto>> expectedValue) {
        Mockito.when(vendorRepository.findVendorByName(VENDOR_NAME1))
                        .thenReturn(Optional.of(new Vendor(VENDOR_ID1, VENDOR_NAME1)));
        Mockito.when(vendorRepository.findVendorByName(VENDOR_NAME2))
                .thenReturn(Optional.empty());

        Mockito.when(shopRepository.findAll()).thenReturn(List.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(offerRepository.findByShopIdAndVendorIdAndDateOrderByCardPopularityAsc(
                        Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any()))
                .thenReturn(new PageImpl<>(List.of(OFFER1, OFFER2)));

        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID1)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID1, ARCHITECTURE_NAME1)));
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID2)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID2, ARCHITECTURE_NAME2)));
        Mockito.when(cardRepository.findCardById(Mockito.eq(CARD_ID1)))
                .thenReturn(Optional.of(new Card(CARD_ID1, CARD_NAME1, ARCHITECTURE_ID1, CARD_SERIES1)));
        Mockito.when(cardRepository.findCardById(Mockito.eq(CARD_ID2)))
                .thenReturn(Optional.of(new Card(CARD_ID2, CARD_NAME2, ARCHITECTURE_ID2, CARD_SERIES2)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID1)))
                .thenReturn(Optional.of(new Shop(SHOP_ID1, SHOP_NAME1)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID1)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID1, VENDOR_NAME1)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID2)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID2, VENDOR_NAME2)));

        Assertions.assertEquals(expectedValue, dataService.getPopularityForVendor(vendorName));
    }



    public static Stream<Arguments> testIsCardPresentSource() {
        return Stream.of(
                Arguments.of(CARD_NAME1, true),
                Arguments.of(CARD_NAME2, false)
        );
    }

    public static Stream<Arguments> testGetPriceForCardSource() {
        return Stream.of(
                Arguments.of(CARD_NAME1, List.of(OFFER_DTO1)),
                Arguments.of(CARD_NAME2, List.of())
        );
    }

    public static Stream<Arguments> testGetPriceForVendorSource() {
        return Stream.of(
                Arguments.of(CARD_SERIES1, VENDOR_NAME1, List.of(OFFER_DTO1)),
                Arguments.of(CARD_SERIES1, VENDOR_NAME2, List.of()),
                Arguments.of(CARD_SERIES2, VENDOR_NAME1, List.of()),
                Arguments.of(CARD_SERIES2, VENDOR_NAME2, List.of())
        );
    }

    public static Stream<Arguments> testGetPriceForShopSource() {
        return Stream.of(
                Arguments.of(CARD_SERIES1, SHOP_NAME1, List.of(OFFER_DTO1)),
                Arguments.of(CARD_SERIES1, SHOP_NAME2, List.of()),
                Arguments.of(CARD_SERIES2, SHOP_NAME1, List.of()),
                Arguments.of(CARD_SERIES2, SHOP_NAME2, List.of())
        );
    }

    public static Stream<Arguments> testGetPopularityForShopSource() {
        Map<Integer, OfferDto> map = Map.of(1, OFFER_DTO1, 2, OFFER_DTO2);
        List<Map<Integer, OfferDto>> list = new ArrayList<>();
        for (int i = 0; i <= 90; i++) {
            list.add(map);
        }
        return Stream.of(
                Arguments.of(SHOP_NAME1, list),
                Arguments.of(SHOP_NAME2, List.of())
        );
    }

    public static Stream<Arguments> testGetPopularityForVendorSource() {
        Map<Integer, OfferDto> map = Map.of(1, OFFER_DTO1, 2, OFFER_DTO2);
        return Stream.of(
                Arguments.of(VENDOR_NAME1, Map.of(SHOP_NAME1, map)),
                Arguments.of(VENDOR_NAME2, Map.of())
        );
    }
}
