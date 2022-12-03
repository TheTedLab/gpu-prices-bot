package repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import table.Offer;

@Repository
public interface OfferRepository extends JpaRepository<Offer, Integer> {

}
