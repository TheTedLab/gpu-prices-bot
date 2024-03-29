package com.gr3530904_90104.repository;

import com.gr3530904_90104.table.Vendor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface VendorRepository extends JpaRepository<Vendor, Integer> {
    Optional<Vendor> findVendorById(Integer id);
    Optional<Vendor> findVendorByName(String name);
}
