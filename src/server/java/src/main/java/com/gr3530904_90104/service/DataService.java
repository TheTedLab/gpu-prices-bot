package com.gr3530904_90104.service;

import com.gr3530904_90104.table.dto.OfferDto;

import java.util.List;
import java.util.Map;

public interface DataService {
    void putNewData(List<OfferDto> offerDtos);
    boolean isCardPresent(String cardName);
    List<OfferDto> getPriceForCard(String cardName);
    List<OfferDto> getPriceForVendor(String cardName, String vendorName);
    List<OfferDto> getPriceForShop(String cardName, String shopName);
    Map<String, Map<Integer, OfferDto>> getPopularityForVendor(String vendorName);
    Map<Integer, OfferDto> getPopularityForShop(String shopName);
}
