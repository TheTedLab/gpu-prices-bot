package com.gr3530904_90104.table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Table(name = "vendors")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
public class Vendor {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "vendors_id_seq")
    @SequenceGenerator(name = "vendors_id_seq", sequenceName = "vendors_id_seq", allocationSize = 1)
    Integer id;

    @Column(name = "vendors_name")
    String name;
}
