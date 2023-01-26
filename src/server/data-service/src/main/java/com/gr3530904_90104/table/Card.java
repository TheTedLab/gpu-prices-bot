package com.gr3530904_90104.table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Table(name = "gpus")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
public class Card {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "gpus_id_seq")
    @SequenceGenerator(name = "gpus_id_seq", sequenceName = "gpus_id_seq", allocationSize = 1)
    Integer id;

    @Column(name = "gpu_name")
    String name;

    @Column(name = "architecture_id")
    Integer architectureId;

    @Column(name = "gpu_series")
    String cardSeries;
}
