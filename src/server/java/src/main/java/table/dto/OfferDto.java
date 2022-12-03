package table.dto;

import lombok.Data;

import java.util.Date;

@Data
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
