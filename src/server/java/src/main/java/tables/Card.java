package tables;

import lombok.Data;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table
@Data
public class Card {
    @Id
    int id;
    String name;
    int architectureId;
    String cardSeries;
}
