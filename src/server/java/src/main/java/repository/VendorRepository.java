package repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import table.Vendor;

import java.util.Optional;

@Repository
public interface VendorRepository extends JpaRepository<Vendor, Integer> {
    public Optional<Vendor> findVendorById(Integer id);
    public Optional<Vendor> findVendorByName(String name);
}
