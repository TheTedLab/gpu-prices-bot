package com.gr3530904_90104.controller;

import com.gr3530904_90104.service.DataService;
import com.gr3530904_90104.service.impl.DataServiceImpl;
import com.gr3530904_90104.table.dto.OfferDto;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.mockito.Mockito;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

public class RequestControllerTest {
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
    private static final Date AGGREGATE_DATE = Date.from(LocalDate.parse("2022-11-20").atStartOfDay().atZone(ZoneId.systemDefault()).toInstant());
    private static final OfferDto OFFER_DTO1 = new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE);
    private static final OfferDto OFFER_DTO2 = new OfferDto(CARD_NAME2, ARCHITECTURE_NAME2, CARD_SERIES2, SHOP_NAME1, VENDOR_NAME2, PRICE2, POPULARITY2, AGGREGATE_DATE);

    private DataService dataService;
    private RequestController requestController;

    @BeforeEach
    public void init() {
        this.dataService = Mockito.mock(DataServiceImpl.class);
        this.requestController = new RequestController(dataService);
    }

    @Test
    public void testPutNewData() {
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.CREATED), requestController.putNewData(Map.of()));
    }

    @Test
    public void testPutNewDataCatchError() {
        Mockito.doThrow(new IllegalArgumentException()).when(dataService).putNewData(Mockito.anyList());
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR), requestController.putNewData(Map.of("", List.of())));
    }

    @ParameterizedTest
    @MethodSource("testIsCardPresentSource")
    public void testIsCardPresent(String cardName, ResponseEntity<?> expectedResult) {
        Mockito.when(dataService.isCardPresent(Mockito.eq(CARD_NAME1))).thenReturn(true);
        Mockito.when(dataService.isCardPresent(Mockito.eq(CARD_NAME2))).thenReturn(false);
        Assertions.assertEquals(expectedResult, requestController.getIsCardPresent(cardName));
    }

    @Test
    public void testIsCardPresentCatchError() {
        Mockito.doThrow(new IllegalArgumentException()).when(dataService).isCardPresent(Mockito.any());
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR), requestController.getIsCardPresent(CARD_NAME1));
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForCardSource")
    public void testGetPriceForCard(String cardName, ResponseEntity<?> expectedResult) {
        Mockito.when(dataService.getPriceForCard(Mockito.eq(CARD_NAME1))).thenReturn(List.of(
                new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE)
        ));
        Mockito.when(dataService.getPriceForCard(Mockito.eq(CARD_NAME2))).thenReturn(List.of());
        Assertions.assertEquals(expectedResult, requestController.getPriceForCard(cardName));
    }

    @Test
    public void testGetPriceForCardCatchError() {
        Mockito.doThrow(new IllegalArgumentException()).when(dataService).getPriceForCard(Mockito.any());
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR), requestController.getPriceForCard(CARD_NAME1));
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForShop")
    public void testGetPriceForShop(String seriesName, String shopName, ResponseEntity<?> expectedResult) {
        Mockito.when(dataService.getPriceForShop(Mockito.eq(CARD_SERIES1), Mockito.eq(SHOP_NAME1))).thenReturn(List.of(
                new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE)
        ));
        Mockito.when(dataService.getPriceForShop(Mockito.eq(CARD_SERIES1), Mockito.eq(SHOP_NAME2))).thenReturn(List.of());
        Mockito.when(dataService.getPriceForShop(Mockito.eq(CARD_SERIES2), Mockito.eq(SHOP_NAME1))).thenReturn(List.of());
        Mockito.when(dataService.getPriceForShop(Mockito.eq(CARD_SERIES2), Mockito.eq(SHOP_NAME2))).thenReturn(List.of());
        Assertions.assertEquals(expectedResult, requestController.getPriceForShop(seriesName, shopName));
    }

    @Test
    public void testGetPriceForShopCatchError() {
        Mockito.doThrow(new IllegalArgumentException()).when(dataService).getPriceForShop(Mockito.any(), Mockito.any());
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR), requestController.getPriceForShop(CARD_SERIES1, SHOP_NAME1));
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForVendor")
    public void testGetPriceForVendor(String seriesName, String vendorName, ResponseEntity<?> expectedResult) {
        Mockito.when(dataService.getPriceForVendor(Mockito.eq(CARD_SERIES1), Mockito.eq(VENDOR_NAME1))).thenReturn(List.of(
                new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE)
        ));
        Mockito.when(dataService.getPriceForVendor(Mockito.eq(CARD_SERIES1), Mockito.eq(VENDOR_NAME2))).thenReturn(List.of());
        Mockito.when(dataService.getPriceForVendor(Mockito.eq(CARD_SERIES2), Mockito.eq(VENDOR_NAME1))).thenReturn(List.of());
        Mockito.when(dataService.getPriceForVendor(Mockito.eq(CARD_SERIES2), Mockito.eq(VENDOR_NAME2))).thenReturn(List.of());
        Assertions.assertEquals(expectedResult, requestController.getPriceForVendor(seriesName, vendorName));
    }

    @Test
    public void testGetPriceForVendorCatchError() {
        Mockito.doThrow(new IllegalArgumentException()).when(dataService).getPriceForVendor(Mockito.any(), Mockito.any());
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR), requestController.getPriceForVendor(CARD_SERIES1, SHOP_NAME1));
    }

    @ParameterizedTest
    @MethodSource("testGetPopularityForShop")
    public void testGetPopularityForShop(String shopName, List<Map<Integer, OfferDto>> list, ResponseEntity<?> expectedResult) {
        Mockito.when(dataService.getPopularityForShop(Mockito.eq(shopName))).thenReturn(list);
        Assertions.assertEquals(expectedResult, requestController.getPopularityForShop(shopName));
    }

    @Test
    public void testGetPopularityForShopCatchError() {
        Mockito.doThrow(new IllegalArgumentException()).when(dataService).getPopularityForShop(Mockito.any());
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR), requestController.getPopularityForShop(SHOP_NAME1));
    }

    @ParameterizedTest
    @MethodSource("testGetPopularityForVendorSource")
    public void testGetPopularityForVendor(String vendorName, Map<String, Map<Integer, OfferDto>> map, ResponseEntity<?> expectedResult) {
        Mockito.when(dataService.getPopularityForVendor(Mockito.eq(vendorName))).thenReturn(map);
        Assertions.assertEquals(expectedResult, requestController.getPopularityForVendor(vendorName));
    }

    @Test
    public void testGetPopularityForVendorCatchError() {
        Mockito.doThrow(new IllegalArgumentException()).when(dataService).getPopularityForVendor(Mockito.any());
        Assertions.assertEquals(new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR), requestController.getPopularityForVendor(VENDOR_NAME1));
    }


    public static Stream<Arguments> testIsCardPresentSource() {
        return Stream.of(
                Arguments.of(CARD_NAME1, new ResponseEntity<>(true, HttpStatus.OK)),
                Arguments.of(CARD_NAME2, new ResponseEntity<>(false, HttpStatus.NOT_FOUND))
        );
    }

    public static Stream<Arguments> testGetPriceForCardSource() {
        return Stream.of(
                Arguments.of(CARD_NAME1, new ResponseEntity<>(List.of(new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE)), HttpStatus.OK)),
                Arguments.of(CARD_NAME2, new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND))
        );
    }

    public static Stream<Arguments> testGetPriceForShop() {
        return Stream.of(
                Arguments.of(CARD_SERIES1, SHOP_NAME1, new ResponseEntity<>(List.of(new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE)), HttpStatus.OK)),
                Arguments.of(CARD_SERIES1, SHOP_NAME2, new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND)),
                Arguments.of(CARD_SERIES2, SHOP_NAME1, new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND)),
                Arguments.of(CARD_SERIES2, SHOP_NAME2, new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND))
        );
    }

    public static Stream<Arguments> testGetPriceForVendor() {
        return Stream.of(
                Arguments.of(CARD_SERIES1, VENDOR_NAME1, new ResponseEntity<>(List.of(new OfferDto(CARD_NAME1, ARCHITECTURE_NAME1, CARD_SERIES1, SHOP_NAME1, VENDOR_NAME1, PRICE1, POPULARITY1, AGGREGATE_DATE)), HttpStatus.OK)),
                Arguments.of(CARD_SERIES1, VENDOR_NAME2, new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND)),
                Arguments.of(CARD_SERIES2, VENDOR_NAME1, new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND)),
                Arguments.of(CARD_SERIES2, VENDOR_NAME2, new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND))
        );
    }

    public static Stream<Arguments> testGetPopularityForShop() {
        Map<Integer, OfferDto> map = Map.of(1, OFFER_DTO1, 2, OFFER_DTO2);
        List<Map<Integer, OfferDto>> list = new ArrayList<>();
        for (int i = 0; i <= 90; i++) {
            list.add(map);
        }
        return Stream.of(
                Arguments.of(SHOP_NAME1, list, new ResponseEntity<>(list, HttpStatus.OK)),
                Arguments.of(SHOP_NAME2, List.of(), new ResponseEntity<>(List.of(), HttpStatus.NOT_FOUND))
        );
    }

    public static Stream<Arguments> testGetPopularityForVendorSource() {
        Map<Integer, OfferDto> map = Map.of(1, OFFER_DTO1, 2, OFFER_DTO2);
        return Stream.of(
                Arguments.of(VENDOR_NAME1, Map.of(SHOP_NAME1, map), new ResponseEntity<>(Map.of(SHOP_NAME1, map), HttpStatus.OK)),
                Arguments.of(VENDOR_NAME2, Map.of(), new ResponseEntity<>(Map.of(), HttpStatus.NOT_FOUND))
        );
    }
}
