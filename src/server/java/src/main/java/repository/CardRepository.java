package repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import table.Card;

import java.util.Optional;

@Repository
public interface CardRepository extends JpaRepository<Card, Integer> {
    public Optional<Card> findCardById(Integer id);
    public Optional<Card> findCardByName(String name);
}
