package table;

import lombok.Data;

import javax.persistence.Id;
import javax.persistence.Table;

@Table
@Data
public class Vendor {
    @Id
    Integer id;
    String name;
}
