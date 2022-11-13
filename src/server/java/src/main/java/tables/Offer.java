package tables;

import lombok.Data;

import javax.persistence.Id;
import javax.persistence.Table;
import java.util.Date;

@Table
@Data
public class Offer {
    @Id
    int id;
    int cardId;
    int shopId;
    String cardSeries;
    int vendorId;
    int cardPrice;
    int cardPopularity;
    Date date;
}
