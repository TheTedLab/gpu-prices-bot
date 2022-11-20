package tables.dto;

import lombok.Data;

import java.util.Date;

@Data
public class OfferDto {
    String cardName;
    String cardArchitecture;
    String cardSeries;
    String shopName;
    String vendorName;
    int cardPrice;
    int cardPopularity;
    Date date;
}
