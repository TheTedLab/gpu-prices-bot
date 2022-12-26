package com.gr3530904_90104.table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.util.Date;

@
Table(name = "offers")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
public class Offer {
    @Id
    @Column(name = "offer_id")
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "offers_offer_id_seq")
    @SequenceGenerator(name = "offers_offer_id_seq", sequenceName = "offers_offer_id_seq", allocationSize = 1)
    Integer id;

    @Column(name = "gpu_id")
    Integer cardId;

    @Column(name = "shop_id")
    Integer shopId;

    @Column(name = "vendor_id")
    Integer vendorId;

    @Column(name = "price")
    Integer cardPrice;

    @Column(name = "popularity_place")
    Integer cardPopularity;

    @Column(name = "aggregate_date")
    Date date;
}
