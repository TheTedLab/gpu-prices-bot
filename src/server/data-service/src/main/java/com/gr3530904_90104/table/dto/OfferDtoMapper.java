package com.gr3530904_90104.table.dto;

import com.gr3530904_90104.repository.*;
import com.gr3530904_90104.table.*;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

@Component
@AllArgsConstructor
@Slf4j
public class OfferDtoMapper {
    private ArchitectureRepository architectureRepository;
    private CardRepository cardRepository;
    private ShopRepository shopRepository;
    private VendorRepository vendorRepository;

    public Offer mapOfferDtoToOffer(OfferDto offerDto) {
        if (offerDto == null) {
            throw new IllegalArgumentException("OfferDto must be not null");
        }

        Optional<Architecture> architecture = architectureRepository.findArchitectureByName(offerDto.getCardArchitecture());
        if (architecture.isEmpty()) {
            Architecture a = Architecture.builder().name(offerDto.getCardArchitecture()).build();
            architecture = Optional.of(architectureRepository.saveAndFlush(a));
        }

        Optional<Card> card = cardRepository.findCardByName(offerDto.getCardName());
        if (card.isEmpty()) {
            Card c = Card.builder().name(offerDto.getCardName()).cardSeries(offerDto.getCardSeries()).architectureId(architecture.get().getId()).build();
            card = Optional.of(cardRepository.saveAndFlush(c));
        }

        Optional<Shop> shop = shopRepository.findShopByName(offerDto.getShopName());
        if (shop.isEmpty()) {
            Shop s = Shop.builder().name(offerDto.getShopName()).build();
            shop = Optional.of(shopRepository.saveAndFlush(s));
        }

        Optional<Vendor> vendor = vendorRepository.findVendorByName(offerDto.getVendorName());
        if (vendor.isEmpty()) {
            Vendor v = Vendor.builder().name(offerDto.getVendorName()).build();
            vendor = Optional.of(vendorRepository.saveAndFlush(v));
        }

        return Offer.builder()
                .cardId(card.get().getId())
                .shopId(shop.get().getId())
                .vendorId(vendor.get().getId())
                .cardPrice(offerDto.getCardPrice())
                .date(offerDto.getDate())
                .cardPopularity(offerDto.getCardPopularity())
                .build();
    }

    public OfferDto mapOfferToOfferDto(Offer offer) {
        if (offer == null) {
            throw new IllegalArgumentException("Offer must be not null");
        }

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

    public OfferDto mapOfferToOfferDto(Offer offer, Card card) {
        if (offer == null) {
            throw new IllegalArgumentException("Offer must be not null");
        }
        if (card == null) {
            throw new IllegalArgumentException("Card must be not null");
        }

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

    public OfferDto mapOfferToOfferDto(Offer offer, List<Card> cards, Vendor vendor) {
        if (offer == null) {
            throw new IllegalArgumentException("Offer must be not null");
        }
        if (cards.isEmpty()) {
            throw new IllegalArgumentException("Cards must be not empty");
        }
        if (vendor == null) {
            throw new IllegalArgumentException("Vendor must be not null");
        }

        Card card = cards.stream().filter(c -> c.getId().equals(offer.getCardId())).findFirst().get();
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

    public OfferDto mapOfferToOfferDto(Offer offer, List<Card> cards, Shop shop) {
        if (offer == null) {
            throw new IllegalArgumentException("Offer must be not null");
        }
        if (cards.isEmpty()) {
            throw new IllegalArgumentException("Cards must be not empty");
        }
        if (shop == null) {
            throw new IllegalArgumentException("Shop must be not null");
        }

        Card card = cards.stream().filter(c -> c.getId().equals(offer.getCardId())).findFirst().get();
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
