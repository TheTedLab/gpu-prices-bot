package com.gr3530904_90104.table.dto;

import com.gr3530904_90104.repository.ArchitectureRepository;
import com.gr3530904_90104.repository.CardRepository;
import com.gr3530904_90104.repository.ShopRepository;
import com.gr3530904_90104.repository.VendorRepository;
import com.gr3530904_90104.table.*;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.mockito.Mockito;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

public class OfferDtoMapperTest {

    private ArchitectureRepository architectureRepository;
    private CardRepository cardRepository;
    private ShopRepository shopRepository;
    private VendorRepository vendorRepository;
    private OfferDtoMapper offerDtoMapper;

    private static final String CARD_NAME = "GEFORCE RTX 3060 TI GAMING X 8GB";
    private static final String CARD_SERIES = "GEFORCE RTX 3060 TI";
    private static final String ARCHITECTURE_NAME = "NVIDIA";
    private static final String SHOP_NAME = "MVIDEO";
    private static final String VENDOR_NAME = "MSI";
    private static final Integer PRICE = 41999;
    private static final Integer POPULARITY = 1;
    private static final Integer ARCHITECTURE_ID = 1;
    private static final Integer CARD_ID = 1;
    private static final Integer SHOP_ID = 1;
    private static final Integer VENDOR_ID = 1;
    private static final Date AGGREGATE_DATE = Date.from(LocalDate.parse("2022-11-20").atStartOfDay().atZone(ZoneId.systemDefault()).toInstant());
    private static final OfferDto OFFER_DTO = new OfferDto(CARD_NAME, ARCHITECTURE_NAME, CARD_SERIES, SHOP_NAME, VENDOR_NAME, PRICE, POPULARITY, AGGREGATE_DATE);
    private static final Offer OFFER = new Offer(null, CARD_ID, SHOP_ID, VENDOR_ID, PRICE, POPULARITY, AGGREGATE_DATE);

    @BeforeEach
    public void init() {
        architectureRepository = Mockito.mock(ArchitectureRepository.class);
        cardRepository = Mockito.mock(CardRepository.class);
        shopRepository = Mockito.mock(ShopRepository.class);
        vendorRepository = Mockito.mock(VendorRepository.class);
        offerDtoMapper = new OfferDtoMapper(architectureRepository, cardRepository, shopRepository, vendorRepository);
    }

    @Test
    public void testMapOfferDtoToOfferThrowsException() {
        Assertions.assertThrows(IllegalArgumentException.class, () -> offerDtoMapper.mapOfferDtoToOffer(null));
    }

    @Test
    public void testMapOfferDtoToOfferWithEmptyDataBase() {
        Mockito.when(architectureRepository.findArchitectureByName(Mockito.eq(ARCHITECTURE_NAME))).thenReturn(Optional.empty());
        Mockito.when(cardRepository.findCardByName(Mockito.eq(CARD_NAME))).thenReturn(Optional.empty());
        Mockito.when(shopRepository.findShopByName(Mockito.eq(SHOP_NAME))).thenReturn(Optional.empty());
        Mockito.when(vendorRepository.findVendorByName(Mockito.eq(VENDOR_NAME))).thenReturn(Optional.empty());
        Mockito.when(architectureRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Architecture(ARCHITECTURE_ID, ARCHITECTURE_NAME));
        Mockito.when(cardRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES));
        Mockito.when(shopRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Shop(SHOP_ID, SHOP_NAME));
        Mockito.when(vendorRepository.saveAndFlush(Mockito.any()))
                .thenReturn(new Vendor(VENDOR_ID, VENDOR_NAME));

        Assertions.assertEquals(offerDtoMapper.mapOfferDtoToOffer(OFFER_DTO), OFFER);
    }

    @Test
    public void testMapOfferDtoToOfferWithNotEmptyDataBase() {
        Mockito.when(architectureRepository.findArchitectureByName(Mockito.eq(ARCHITECTURE_NAME)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID, ARCHITECTURE_NAME)));
        Mockito.when(cardRepository.findCardByName(Mockito.eq(CARD_NAME)))
                .thenReturn(Optional.of(new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES)));
        Mockito.when(shopRepository.findShopByName(Mockito.eq(SHOP_NAME)))
                .thenReturn(Optional.of(new Shop(SHOP_ID, SHOP_NAME)));
        Mockito.when(vendorRepository.findVendorByName(Mockito.eq(VENDOR_NAME)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID, VENDOR_NAME)));

        Assertions.assertEquals(offerDtoMapper.mapOfferDtoToOffer(OFFER_DTO), OFFER);
    }

    @Test
    public void testMapOfferToOfferDtoThrowsException() {
        Assertions.assertThrows(IllegalArgumentException.class, () -> offerDtoMapper.mapOfferToOfferDto(null));
    }

    @Test
    public void testMapOfferToOfferDto() {
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID, ARCHITECTURE_NAME)));
        Mockito.when(cardRepository.findCardById(Mockito.eq(CARD_ID)))
                .thenReturn(Optional.of(new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID)))
                .thenReturn(Optional.of(new Shop(SHOP_ID, SHOP_NAME)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID, VENDOR_NAME)));

        Assertions.assertEquals(offerDtoMapper.mapOfferToOfferDto(OFFER), OFFER_DTO);
    }

    @ParameterizedTest
    @MethodSource("testMapOfferToOfferDtoWithCardThrowsExceptionSource")
    public void testMapOfferToOfferDtoWithCardThrowsException(Offer offer, Card card) {
        Assertions.assertThrows(IllegalArgumentException.class, () -> offerDtoMapper.mapOfferToOfferDto(offer, card));
    }

    @Test
    public void testMapOfferToOfferDtoWithCard() {
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID, ARCHITECTURE_NAME)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID)))
                .thenReturn(Optional.of(new Shop(SHOP_ID, SHOP_NAME)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID, VENDOR_NAME)));

        Card card = new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES);
        Assertions.assertEquals(offerDtoMapper.mapOfferToOfferDto(OFFER, card), OFFER_DTO);
    }

    @ParameterizedTest
    @MethodSource("testMapOfferToOfferDtoWithCardsAndVendorThrowsExceptionSource")
    public void testMapOfferToOfferDtoWithCardsAndVendorThrowsException(Offer offer, List<Card> cards, Vendor vendor) {
        Assertions.assertThrows(IllegalArgumentException.class, () -> offerDtoMapper.mapOfferToOfferDto(offer, cards, vendor));
    }

    @Test
    public void testMapOfferToOfferDtoWithCardsAndVendor() {
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID, ARCHITECTURE_NAME)));
        Mockito.when(shopRepository.findShopById(Mockito.eq(SHOP_ID)))
                .thenReturn(Optional.of(new Shop(SHOP_ID, SHOP_NAME)));

        Card cardGood = new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES);
        Card cardBad = new Card(CARD_ID + 1, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES);
        List<Card> cards = List.of(cardBad, cardGood);
        Vendor vendor = new Vendor(VENDOR_ID, VENDOR_NAME);
        Assertions.assertEquals(offerDtoMapper.mapOfferToOfferDto(OFFER, cards, vendor), OFFER_DTO);
    }

    @ParameterizedTest
    @MethodSource("testMapOfferToOfferDtoWithCardsAndShopThrowsExceptionSource")
    public void testMapOfferToOfferDtoWithCardsAndShopThrowsException(Offer offer, List<Card> cards, Shop shop) {
        Assertions.assertThrows(IllegalArgumentException.class, () -> offerDtoMapper.mapOfferToOfferDto(offer, cards, shop));
    }

    @Test
    public void testMapOfferToOfferDtoWithCardsAndShop() {
        Mockito.when(architectureRepository.findArchitectureById(Mockito.eq(ARCHITECTURE_ID)))
                .thenReturn(Optional.of(new Architecture(ARCHITECTURE_ID, ARCHITECTURE_NAME)));
        Mockito.when(vendorRepository.findVendorById(Mockito.eq(VENDOR_ID)))
                .thenReturn(Optional.of(new Vendor(VENDOR_ID, VENDOR_NAME)));

        Card cardGood = new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES);
        Card cardBad = new Card(CARD_ID + 1, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES);
        List<Card> cards = List.of(cardBad, cardGood);
        Shop shop = new Shop(SHOP_ID, SHOP_NAME);
        Assertions.assertEquals(offerDtoMapper.mapOfferToOfferDto(OFFER, cards, shop), OFFER_DTO);
    }

    public static Stream<Arguments> testMapOfferToOfferDtoWithCardThrowsExceptionSource() {
        return Stream.of(
                Arguments.of(null, new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES)),
                Arguments.of(OFFER, null)
        );
    }

    public static Stream<Arguments> testMapOfferToOfferDtoWithCardsAndVendorThrowsExceptionSource() {
        return Stream.of(
                Arguments.of(null, List.of(new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES)), new Vendor(VENDOR_ID, VENDOR_NAME)),
                Arguments.of(OFFER, List.of(), new Vendor(VENDOR_ID, VENDOR_NAME)),
                Arguments.of(OFFER, List.of(new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES)), null)
        );
    }

    public static Stream<Arguments> testMapOfferToOfferDtoWithCardsAndShopThrowsExceptionSource() {
        return Stream.of(
                Arguments.of(null, List.of(new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES)), new Shop(SHOP_ID, SHOP_NAME)),
                Arguments.of(OFFER, List.of(), new Shop(SHOP_ID, SHOP_NAME)),
                Arguments.of(OFFER, List.of(new Card(CARD_ID, CARD_NAME, ARCHITECTURE_ID, CARD_SERIES)), null)
        );
    }
}
