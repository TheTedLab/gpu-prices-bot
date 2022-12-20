package com.gr3530904_90104.service.impl;

import com.gr3530904_90104.repository.*;
import com.gr3530904_90104.service.DataService;
import com.gr3530904_90104.table.*;
import com.gr3530904_90104.table.dto.OfferDto;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
@Getter
public class DataServiceImpl implements DataService {
    private static final long NINETY_DAYS = 90L * 24 * 60 * 60 * 1000; // days-hours-minutes-seconds-milliseconds

    private ArchitectureRepository architectureRepository;
    private CardRepository cardRepository;
    private OfferRepository offerRepository;
    private ShopRepository shopRepository;
    private VendorRepository vendorRepository;

    @Override
    public void putNewData(List<OfferDto> offerDtos) {
        List<Offer> offers = offerDtos.stream().map(this::mapOfferDtoToOffer).collect(Collectors.toList());
        offerRepository.saveAll(offers);
    }

    @Override
    public boolean isCardPresent(String cardName) {
        return cardRepository.findCardByName(cardName).isPresent();
    }

    @Override
    public List<OfferDto> getPriceForCard(String cardName) {
        Date endDate = new Date();
        Date startDate = new Date(endDate.getTime() - NINETY_DAYS);
        Optional<Card> card = cardRepository.findCardByName(cardName);
        if (card.isPresent()) {
            List<Offer> offers = offerRepository.findByCardIdAndDateBetween(card.get().getId(), startDate, endDate);
            return offers.stream().map((o) -> mapOfferToOfferDto(o, card.get())).collect(Collectors.toList());
        }
        return new ArrayList<>();
    }

    @Override
    public List<OfferDto> getPriceForVendor(String cardName, String vendorName) {
        Date endDate = new Date();
        Date startDate = new Date(endDate.getTime() - NINETY_DAYS);
        Optional<Card> card = cardRepository.findCardByName(cardName);
        Optional<Vendor> vendor = vendorRepository.findVendorByName(vendorName);
        if (card.isPresent() && vendor.isPresent()) {
            List<Offer> offers = offerRepository.findByCardIdAndVendorIdAndDateBetween(card.get().getId(),
                    vendor.get().getId(), startDate, endDate);
            return offers.stream().map((o) -> mapOfferToOfferDto(o, card.get(), vendor.get()))
                    .collect(Collectors.toList());
        }
        return new ArrayList<>();
    }

    @Override
    public List<OfferDto> getPriceForShop(String cardName, String shopName) {
        Date endDate = new Date();
        Date startDate = new Date(endDate.getTime() - NINETY_DAYS);
        Optional<Card> card = cardRepository.findCardByName(cardName);
        Optional<Shop> shop = shopRepository.findShopByName(shopName);
        if (card.isPresent() && shop.isPresent()) {
            List<Offer> offers = offerRepository.findByCardIdAndShopIdAndDateBetween(card.get().getId(),
                    shop.get().getId(), startDate, endDate);
            return offers.stream().map((o) -> mapOfferToOfferDto(o, card.get(), shop.get()))
                    .collect(Collectors.toList());
        }
        return new ArrayList<>();
    }

    @Override
    public Map<String, Map<Integer, OfferDto>> getPopularityForVendor(String vendorName) {
        Optional<Vendor> vendor = vendorRepository.findVendorByName(vendorName);
        if (vendor.isPresent()) {
            List<Shop> shops = shopRepository.findAll();
            Map<String, Map<Integer, OfferDto>> map = new HashMap<>();
            for (Shop shop: shops) {
                Map<Integer, OfferDto> temp = new HashMap<>();
                PageRequest pageRequest = PageRequest.of(0, 10);
                Page<Offer> offers = offerRepository.findByShopIdAndVendorIdOrderByCardPopularityAsc(shop.getId(),
                        vendor.get().getId(), pageRequest);
                final Integer[] popularity = {1};
                offers.forEach((o) -> temp.put(popularity[0]++, mapOfferToOfferDto(o)));
                map.put(shop.getName(), temp);
            }
            return map;
        }
        return new HashMap<>();
    }

    @Override
    public Map<Integer, OfferDto> getPopularityForShop(String shopName) {
        Optional<Shop> shop = shopRepository.findShopByName(shopName);
        if (shop.isPresent()) {
            PageRequest pageRequest = PageRequest.of(0, 10);
            Page<Offer> offers = offerRepository.findByShopIdOrderByCardPopularityAsc(shop.get().getId(), pageRequest);
            Map<Integer, OfferDto> map = new HashMap<>();
            offers.forEach((o) -> map.put(o.getCardPopularity(), mapOfferToOfferDto(o)));
            return map;
        }
        return new HashMap<>();
    }

    private Offer mapOfferDtoToOffer(OfferDto offerDto) {
        Optional<Architecture> architecture = architectureRepository.findArchitectureByName(offerDto.getCardArchitecture());
        if (!architecture.isPresent()) {
            Architecture a = Architecture.builder().name(offerDto.getCardArchitecture()).build();
            architectureRepository.saveAndFlush(a);
            architecture = architectureRepository.findArchitectureByName(offerDto.getCardArchitecture());
        }

        Optional<Card> card = cardRepository.findCardByName(offerDto.getCardName());
        if (!card.isPresent()) {
            Card c = Card.builder().name(offerDto.getCardName()).cardSeries(offerDto.getCardSeries()).architectureId(architecture.get().getId()).build();
            cardRepository.saveAndFlush(c);
            card = cardRepository.findCardByName(offerDto.getCardName());
        }

        Optional<Shop> shop = shopRepository.findShopByName(offerDto.getShopName());
        if (!shop.isPresent()) {
            Shop s = Shop.builder().name(offerDto.getShopName()).build();
            shopRepository.saveAndFlush(s);
            shop = shopRepository.findShopByName(offerDto.getShopName());
        }

        Optional<Vendor> vendor = vendorRepository.findVendorByName(offerDto.getVendorName());
        if (!vendor.isPresent()) {
            Vendor v = Vendor.builder().name(offerDto.getVendorName()).build();
            vendorRepository.saveAndFlush(v);
            vendor = vendorRepository.findVendorByName(offerDto.getVendorName());
        }

        return Offer.builder()
                .cardId(card.get().getId())
                .shopId(shop.get().getId())
                .vendorId(vendor.get().getId())
                .cardPrice(offerDto.getCardPrice())
                .date(new Date())
                .cardPopularity(offerDto.getCardPopularity())
                .build();
    }

    private OfferDto mapOfferToOfferDto(Offer offer) {
        Optional<Card> card = cardRepository.findCardById(offer.getCardId());
        Optional<Architecture> architecture = architectureRepository.findArchitectureById(card.get().getArchitectureId());
        Optional<Shop> shop = shopRepository.findShopById(offer.getShopId());
        Optional<Vendor> vendor = vendorRepository.findVendorById(offer.getVendorId());

        return OfferDto.builder()
                .cardName(card.get().getName())
                .cardArchitecture(architecture.get().getName())
                .cardSeries(card.get().getCardSeries())
                .shopName(shop.get().getName())
                .vendorName(vendor.get().getName())
                .cardPrice(offer.getCardPrice())
                .cardPopularity(offer.getCardPopularity())
                .date(offer.getDate())
                .build();
    }

    private OfferDto mapOfferToOfferDto(Offer offer, Card card) {
        Optional<Architecture> architecture = architectureRepository.findArchitectureById(card.getArchitectureId());
        Optional<Shop> shop = shopRepository.findShopById(offer.getShopId());
        Optional<Vendor> vendor = vendorRepository.findVendorById(offer.getVendorId());

        return OfferDto.builder()
                .cardName(card.getName())
                .cardArchitecture(architecture.get().getName())
                .cardSeries(card.getCardSeries())
                .shopName(shop.get().getName())
                .vendorName(vendor.get().getName())
                .cardPrice(offer.getCardPrice())
                .cardPopularity(offer.getCardPopularity())
                .date(offer.getDate())
                .build();
    }

    private OfferDto mapOfferToOfferDto(Offer offer, Card card, Vendor vendor) {
        Optional<Architecture> architecture = architectureRepository.findArchitectureById(card.getArchitectureId());
        Optional<Shop> shop = shopRepository.findShopById(offer.getShopId());

        return OfferDto.builder()
                .cardName(card.getName())
                .cardArchitecture(architecture.get().getName())
                .cardSeries(card.getCardSeries())
                .shopName(shop.get().getName())
                .vendorName(vendor.getName())
                .cardPrice(offer.getCardPrice())
                .cardPopularity(offer.getCardPopularity())
                .date(offer.getDate())
                .build();
    }

    private OfferDto mapOfferToOfferDto(Offer offer, Card card, Shop shop) {
        Optional<Architecture> architecture = architectureRepository.findArchitectureById(card.getArchitectureId());
        Optional<Vendor> vendor = vendorRepository.findVendorById(offer.getVendorId());

        return OfferDto.builder()
                .cardName(card.getName())
                .cardArchitecture(architecture.get().getName())
                .cardSeries(card.getCardSeries())
                .shopName(shop.getName())
                .vendorName(vendor.get().getName())
                .cardPrice(offer.getCardPrice())
                .cardPopularity(offer.getCardPopularity())
                .date(offer.getDate())
                .build();
    }
}
