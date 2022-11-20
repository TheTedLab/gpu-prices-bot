package controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import services.DataService;
import tables.dto.OfferDto;

import java.util.List;
import java.util.Map;

public class RequestController {

    @Autowired
    private DataService dataService;

    @PostMapping("/insert-new-data")
    public ResponseEntity<?> putNewData(@RequestBody List<OfferDto> offerDtos) {
        try {
            dataService.putNewData(offerDtos);
            return new ResponseEntity<>(HttpStatus.CREATED);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/is-card-present")
    public ResponseEntity<Boolean> getIsCardPresent(@RequestParam("cardName") String cardName) {
        try {
            return new ResponseEntity<>(dataService.isCardPresent(cardName), HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/price")
    public ResponseEntity<List<OfferDto>> getPriceForCard(@RequestParam("cardName") String cardName) {
        try {
            return new ResponseEntity<>(dataService.getPriceForCard(cardName), HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/price/for-shop")
    public ResponseEntity<List<OfferDto>> getPriceForShop(@RequestParam("cardName") String cardName, @RequestParam("shopName") String shopName) {
        try {
            return new ResponseEntity<>(dataService.getPriceForShop(cardName, shopName), HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/price/for-vendor")
    public ResponseEntity<List<OfferDto>> getPriceForVendor(@RequestParam("cardName") String cardName, @RequestParam("vendorName") String vendorName) {
        try {
            return new ResponseEntity<>(dataService.getPriceForVendor(cardName, vendorName), HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/popularity/for-shop")
    public ResponseEntity<Map<Integer, OfferDto>> getPopularityForShop(@RequestParam("shopName") String shopName) {
        try {
            return new ResponseEntity<>(dataService.getPopularityForShop(shopName), HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/popularity/for-shop")
    public ResponseEntity<Map<String, Map<Integer, OfferDto>>> getPopularityForVendor(@RequestParam("vendorName") String vendorName) {
        try {
            return new ResponseEntity<>(dataService.getPopularityForVendor(vendorName), HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
