package com.gr3530904_90104.repository;

import com.gr3530904_90104.table.Shop;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ShopRepository extends JpaRepository<Shop, Integer> {
    Optional<Shop> findShopById(Integer id);
    Optional<Shop> findShopByName(String name);
}
