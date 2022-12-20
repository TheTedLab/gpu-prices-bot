package com.gr3530904_90104.table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Table(name = "shops")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
public class Shop {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "shops_id_seq")
    @SequenceGenerator(name = "shops_id_seq", sequenceName = "shops_id_seq", allocationSize = 1)
    Integer id;

    @Column(name = "shop_name")
    String name;
}
