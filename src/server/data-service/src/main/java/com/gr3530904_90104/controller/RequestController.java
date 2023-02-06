package com.gr3530904_90104.controller;

import com.gr3530904_90104.service.DataService;
import com.gr3530904_90104.table.dto.OfferDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@Slf4j
public class RequestController {

    @Autowired
    private DataService dataService;

    @PostMapping("/insert-new-data")
    public ResponseEntity<?> putNewData(@RequestBody Map<String, List<OfferDto>> map) {
        try {
            log.info("POST /insert-new-data");
            map.forEach((key, list) -> dataService.putNewData(list));
            log.info("POST /insert-new-data success");
            return new ResponseEntity<>(HttpStatus.CREATED);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/is-card-present")
    public ResponseEntity<Boolean> getIsCardPresent(@RequestParam("cardName") String cardName) {
        try {
            log.info("GET /is-card-present/{}", cardName);
            boolean response = dataService.isCardPresent(cardName);
            log.debug("response: {}", response);
            return new ResponseEntity<>(response, response ? HttpStatus.OK : HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            log.error("Error in /is-card-present: {}", e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/price")
    public ResponseEntity<List<OfferDto>> getPriceForCard(@RequestParam("cardName") String cardName) {
        try {
            log.info("GET /price?cardName={}", cardName);
            List<OfferDto> response = dataService.getPriceForCard(cardName);
            log.debug("response: {}", response);
            return new ResponseEntity<>(response, !response.isEmpty() ? HttpStatus.OK : HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            log.error("Error in /price?cardName={}: {}", cardName, e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/price/for-shop")
    public ResponseEntity<List<OfferDto>> getPriceForShop(@RequestParam("seriesName") String seriesName, @RequestParam("shopName") String shopName) {
        try {
            log.info("GET /price?seriesName={}&shopName={}", seriesName, shopName);
            List<OfferDto> response = dataService.getPriceForShop(seriesName, shopName);
            log.debug("response: {}", response);
            return new ResponseEntity<>(response, !response.isEmpty() ? HttpStatus.OK : HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            log.error("Error in /price?seriesName={}&shopName={}: {}", seriesName, shopName, e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/price/for-vendor")
    public ResponseEntity<List<OfferDto>> getPriceForVendor(@RequestParam("seriesName") String seriesName, @RequestParam("vendorName") String vendorName) {
        try {
            log.info("GET /price?seriesName={}&vendorName={}", seriesName, vendorName);
            List<OfferDto> response = dataService.getPriceForVendor(seriesName, vendorName);
            log.debug("response: {}", response);
            return new ResponseEntity<>(response, !response.isEmpty() ? HttpStatus.OK : HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            log.error("Error in /price?seriesName={}&vendorName={}: {}", seriesName, vendorName, e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/popularity/for-shop")
    public ResponseEntity<List<Map<Integer, OfferDto>>> getPopularityForShop(@RequestParam("shopName") String shopName) {
        try {
            log.info("GET /popularity/for-shop?shopName={}", shopName);
            List<Map<Integer, OfferDto>> response = dataService.getPopularityForShop(shopName);
            log.debug("response: {}", response);
            return new ResponseEntity<>(response, !response.isEmpty() ? HttpStatus.OK : HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            log.error("Error in /popularity/for-shop?shopName={}: {}", shopName, e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/popularity/for-vendor")
    public ResponseEntity<Map<String, Map<Integer, OfferDto>>> getPopularityForVendor(@RequestParam("vendorName") String vendorName) {
        try {
            log.info("GET /popularity/for-vendor?vendorName={}", vendorName);
            Map<String, Map<Integer, OfferDto>> response = dataService.getPopularityForVendor(vendorName);
            log.debug("response: {}", response);
            return new ResponseEntity<>(response, !response.isEmpty() ? HttpStatus.OK : HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            log.error("Error in /popularity/for-vendor?vendorName={}: {}", vendorName, e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
