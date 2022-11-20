package services;

import tables.dto.OfferDto;

import java.util.List;
import java.util.Map;

public interface DataService {
    public void putNewData(List<OfferDto> offerDtos);
    public boolean isCardPresent(String cardName);
    public List<OfferDto> getPriceForCard(String cardName);
    public List<OfferDto> getPriceForVendor(String cardName, String vendorName);
    public List<OfferDto> getPriceForShop(String cardName, String shopName);
    public Map<String, Map<Integer, OfferDto>> getPopularityForVendor(String vendorName);
    public Map<Integer, OfferDto> getPopularityForShop(String shopName);
}
