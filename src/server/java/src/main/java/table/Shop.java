package table;

import lombok.Data;

import javax.persistence.Id;
import javax.persistence.Table;

@Table
@Data
public class Shop {
    @Id
    Integer id;
    String name;
}
