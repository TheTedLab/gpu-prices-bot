package com.gr3530904_90104.service.impl;

import com.gr3530904_90104.repository.*;
import com.gr3530904_90104.service.DataService;
import com.gr3530904_90104.table.Card;
import com.gr3530904_90104.table.Offer;
import com.gr3530904_90104.table.Shop;
import com.gr3530904_90104.table.Vendor;
import com.gr3530904_90104.table.dto.OfferDto;
import com.gr3530904_90104.table.dto.OfferDtoMapper;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
@Slf4j
public class DataServiceImpl implements DataService {
    private static final long ONE_DAY = 24L * 60 * 60 * 1000; // hours-minutes-seconds-milliseconds
    private static final long NINETY_DAYS = 90L * ONE_DAY; // days * hours-minutes-seconds-milliseconds

    private ArchitectureRepository architectureRepository;
    private CardRepository cardRepository;
    private OfferRepository offerRepository;
    private ShopRepository shopRepository;
    private VendorRepository vendorRepository;
    private OfferDtoMapper offerDtoMapper;

    @Override
    public void putNewData(List<OfferDto> offerDtos) {
        log.info("putNewData of {} offers", offerDtos.size());
        List<Offer> offers = offerDtos.stream().map(offerDtoMapper::mapOfferDtoToOffer).collect(Collectors.toList());
        offers = offerRepository.saveAll(offers);
        log.info("putNewData: {} of {} offers saved successfully", offers.size(), offerDtos.size());
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
            log.info("Found {} offers", offers.size());
            return offers.stream().map((o) -> offerDtoMapper.mapOfferToOfferDto(o, card.get())).collect(Collectors.toList());
        }
        log.info("No offers found");
        return new ArrayList<>();
    }

    @Override
    public List<OfferDto> getPriceForVendor(String cardSeries, String vendorName) {
        Date endDate = new Date();
        Date startDate = new Date(endDate.getTime() - NINETY_DAYS);
        List<Card> cards = cardRepository.findCardsByCardSeries(cardSeries);
        Optional<Vendor> vendor = vendorRepository.findVendorByName(vendorName);
        if (!cards.isEmpty() && vendor.isPresent()) {
            List<Integer> cardIds = cards.stream().map(Card::getId).toList();
            List<Offer> offers = offerRepository.findByCardIdInAndVendorIdAndDateBetween(cardIds,
                    vendor.get().getId(), startDate, endDate);
            log.info("Found {} offers", offers.size());
            return offers.stream().map((o) -> offerDtoMapper.mapOfferToOfferDto(o, cards, vendor.get()))
                    .collect(Collectors.toList());
        }
        log.info("No offers found");
        return new ArrayList<>();
    }

    @Override
    public List<OfferDto> getPriceForShop(String cardSeries, String shopName) {
        Date endDate = new Date();
        Date startDate = new Date(endDate.getTime() - NINETY_DAYS);
        List<Card> cards = cardRepository.findCardsByCardSeries(cardSeries);
        Optional<Shop> shop = shopRepository.findShopByName(shopName);
        if (!cards.isEmpty() && shop.isPresent()) {
            List<Integer> cardIds = cards.stream().map(Card::getId).toList();
            List<Offer> offers = offerRepository.findByCardIdInAndShopIdAndDateBetween(cardIds,
                    shop.get().getId(), startDate, endDate);
            log.info("Found {} offers", offers.size());
            return offers.stream().map((o) -> offerDtoMapper.mapOfferToOfferDto(o, cards, shop.get()))
                    .collect(Collectors.toList());
        }
        log.info("No offers found");
        return new ArrayList<>();
    }

    @Override
    public Map<String, Map<Integer, OfferDto>> getPopularityForVendor(String vendorName) {
        Optional<Vendor> vendor = vendorRepository.findVendorByName(vendorName);
        if (vendor.isPresent()) {
            int total = 0;
            List<Shop> shops = shopRepository.findAll();
            Map<String, Map<Integer, OfferDto>> map = new HashMap<>();
            for (Shop shop: shops) {
                Map<Integer, OfferDto> temp = new HashMap<>();
                PageRequest pageRequest = PageRequest.of(0, 10);
                Page<Offer> offers = offerRepository.findByShopIdAndVendorIdAndDateOrderByCardPopularityAsc(shop.getId(),
                        vendor.get().getId(), new Date(), pageRequest);
                final Integer[] popularity = {1};
                offers.forEach((o) -> temp.put(popularity[0]++, offerDtoMapper.mapOfferToOfferDto(o)));
                map.put(shop.getName(), temp);
                total += map.get(shop.getName()).size();
                log.info("Found {} offers for shop {}", map.get(shop.getName()).size(), shop.getName());
            }
            if (total > 0) {
                return map;
            }
        }
        log.info("No offers found");
        return new HashMap<>();
    }

    @Override
    public List<Map<Integer, OfferDto>> getPopularityForShop(String shopName) {
        Optional<Shop> shop = shopRepository.findShopByName(shopName);
        Date endDate = new Date();
        Date startDate = new Date(endDate.getTime() - NINETY_DAYS);
        List<Map<Integer, OfferDto>> result = new ArrayList<>();
        if (shop.isPresent()) {
            int total = 0;
            while (startDate.compareTo(endDate) <= 0) {
                PageRequest pageRequest = PageRequest.of(0, 10);
                Page<Offer> offers = offerRepository.findByShopIdAndDateOrderByCardPopularityAsc(shop.get().getId(),
                        startDate, pageRequest);
                Map<Integer, OfferDto> map = new HashMap<>();
                offers.forEach((o) -> map.put(o.getCardPopularity(), offerDtoMapper.mapOfferToOfferDto(o)));
                log.info("Found {} offers of 10", map.size());
                total += map.size();
                result.add(map);
                startDate.setTime(startDate.getTime() + ONE_DAY);
            }
            if (total > 0) {
                return result;
            }
        }
        log.info("No offers found");
        return new ArrayList<>();
    }
}
