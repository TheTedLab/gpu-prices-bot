package tables;

import lombok.Data;

import javax.persistence.Id;
import javax.persistence.Table;

@Table
@Data
public class Shop {
    @Id
    int id;
    String name;
}
