package repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import table.Shop;

import java.util.Optional;

@Repository
public interface ShopRepository extends JpaRepository<Shop, Integer> {
    public Optional<Shop> findShopById(Integer id);
    public Optional<Shop> findShopByName(String name);
}
