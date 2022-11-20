package services.impl;

import org.springframework.stereotype.Service;
import services.DataService;
import tables.dto.OfferDto;

import java.util.List;
import java.util.Map;

@Service
public class DataServiceImpl implements DataService {
    @Override
    public void putNewData(List<OfferDto> offerDtos) {

    }

    @Override
    public boolean isCardPresent(String cardName) {
        return false;
    }

    @Override
    public List<OfferDto> getPriceForCard(String cardName) {
        return null;
    }

    @Override
    public List<OfferDto> getPriceForVendor(String cardName, String vendorName) {
        return null;
    }

    @Override
    public List<OfferDto> getPriceForShop(String cardName, String shopName) {
        return null;
    }

    @Override
    public Map<String, Map<Integer, OfferDto>> getPopularityForVendor(String vendorName) {
        return null;
    }

    @Override
    public Map<Integer, OfferDto> getPopularityForShop(String shopName) {
        return null;
    }
}
