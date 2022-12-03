package table;

import lombok.Data;

import javax.persistence.Id;
import javax.persistence.Table;
import java.util.Date;

@Table
@Data
public class Offer {
    @Id
    Integer id;
    Integer cardId;
    Integer shopId;
    String cardSeries;
    Integer vendorId;
    Integer cardPrice;
    Integer cardPopularity;
    Date date;
}
