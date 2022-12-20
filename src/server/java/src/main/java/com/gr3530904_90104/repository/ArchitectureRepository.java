package com.gr3530904_90104.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.gr3530904_90104.table.Architecture;

import java.util.Optional;

@Repository
public interface ArchitectureRepository extends JpaRepository<Architecture, Integer> {
    Optional<Architecture> findArchitectureById(Integer id);
    Optional<Architecture> findArchitectureByName(String name);
}
