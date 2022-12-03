package table;

import lombok.Data;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table
@Data
public class Card {
    @Id
    Integer id;
    String name;
    Integer architectureId;
    String cardSeries;
}
