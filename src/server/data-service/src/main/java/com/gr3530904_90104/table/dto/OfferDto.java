package com.gr3530904_90104.table.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
@AllArgsConstructor
public class OfferDto {
    String cardName;
    String cardArchitecture;
    String cardSeries;
    String shopName;
    String vendorName;
    Integer cardPrice;
    Integer cardPopularity;
    Date date;
}
