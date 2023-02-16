package com.gr3530904_90104.table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Table(name = "architectures")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
public class Architecture {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "architectures_id_seq")
    @SequenceGenerator(name = "architectures_id_seq", sequenceName = "architectures_id_seq", allocationSize = 1)
    Integer id;

    @Column(name = "architecture_name")
    String name;
}
